from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from whop_sdk import Whop
import threading
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store active sessions and results
sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-members', methods=['POST'])
def get_members():
    """Get all members from Whop"""
    try:
        data = request.json
        api_key = data.get('api_key')
        company_id = data.get('company_id')
        
        if not api_key or not company_id:
            return jsonify({'error': 'Missing required fields'}), 400
        
        client = Whop(api_key=api_key)
        members = []
        
        page = client.members.list(company_id=company_id)
        
        while True:
            for member in page.data:
                # Log member object to understand structure (remove in production)
                print(f"Member object: {member}")
                print(f"Member attributes: {dir(member)}")
                
                # Extract member details - try to get all possible attributes
                member_name = None
                member_email = None
                
                # Convert to dict if possible
                try:
                    if hasattr(member, '__dict__'):
                        member_dict = member.__dict__
                        member_name = member_dict.get('name') or member_dict.get('username')
                        member_email = member_dict.get('email')
                except:
                    pass
                
                # If still not found, try getattr with common names
                if not member_name:
                    for name_attr in ['name', 'username', 'display_name', 'user_name', 'full_name']:
                        try:
                            val = getattr(member, name_attr, None)
                            if val:
                                member_name = val
                                break
                        except:
                            pass
                
                if not member_email:
                    for email_attr in ['email', 'email_address', 'user_email', 'contact_email']:
                        try:
                            val = getattr(member, email_attr, None)
                            if val:
                                member_email = val
                                break
                        except:
                            pass
                
                # Fallback: use member ID
                if not member_name:
                    member_name = member.id if hasattr(member, 'id') else 'Member'
                
                if not member_email:
                    member_email = 'N/A'
                
                members.append({
                    'id': str(member.id) if hasattr(member, 'id') else str(member),
                    'name': str(member_name).strip() if member_name else 'Unknown Member',
                    'email': str(member_email).strip() if member_email else 'N/A'
                })
            
            if not page.page_info.has_next_page:
                break
            
            page = client.members.list(
                company_id=company_id,
                cursor=page.page_info.end_cursor
            )
        
        return jsonify({
            'success': True,
            'members': members,
            'total': len(members)
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-payments', methods=['POST'])
def process_payments():
    """Process payments with credentials from request"""
    try:
        data = request.json
        api_key = data.get('api_key')
        company_id = data.get('company_id')
        plan_id = data.get('plan_id')
        session_id = data.get('session_id')
        selected_member_ids = data.get('selected_members', [])
        
        if not all([api_key, company_id, plan_id, session_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Initialize session tracking
        sessions[session_id] = {
            'status': 'processing',
            'members_found': 0,
            'payments_created': 0,
            'payments_failed': 0,
            'logs': [],
            'start_time': datetime.now().isoformat()
        }
        
        # Run processing in background
        thread = threading.Thread(
            target=run_payment_processing,
            args=(api_key, company_id, plan_id, session_id, selected_member_ids)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'session_id': session_id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<session_id>')
def get_session(session_id):
    """Get session status and logs"""
    if session_id in sessions:
        return jsonify(sessions[session_id])
    return jsonify({'error': 'Session not found'}), 404

def run_payment_processing(api_key, company_id, plan_id, session_id, selected_member_ids=None):
    """Run the payment processing logic"""
    try:
        client = Whop(api_key=api_key)
        session = sessions[session_id]
        
        # Step 1: Get selected members (or all if not specified)
        add_log(session_id, "🔍 Preparing members...", "info")
        
        # Use selected members if provided, otherwise get all
        if selected_member_ids:
            members = selected_member_ids
            add_log(session_id, f"👥 Processing {len(members)} selected members", "success")
        else:
            members = []
            page = client.members.list(company_id=company_id)
            
            while True:
                for member in page.data:
                    members.append(member.id)
                
                if not page.page_info.has_next_page:
                    break
                
                page = client.members.list(
                    company_id=company_id,
                    cursor=page.page_info.end_cursor
                )
            
            add_log(session_id, f"👥 Found {len(members)} members", "success")
        
        session['members_found'] = len(members)
        
        # Step 2: Create payments
        add_log(session_id, "💳 Creating payments...", "info")
        
        for member_id in members:
            pm_page = client.payment_methods.list(member_id=member_id)
            
            while True:
                for pm in pm_page.data:
                    try:
                        payment = client.payments.create(
                            company_id=company_id,
                            member_id=member_id,
                            payment_method_id=pm.id,
                            plan_id=plan_id
                        )
                        
                        session['payments_created'] += 1
                        add_log(
                            session_id,
                            f"✅ SUCCESS | {member_id} | {pm.id} | Payment: {payment.id}",
                            "success"
                        )
                    
                    except Exception as e:
                        session['payments_failed'] += 1
                        add_log(
                            session_id,
                            f"❌ FAILED | {member_id} | {pm.id} | {str(e)}",
                            "error"
                        )
                
                if not pm_page.page_info.has_next_page:
                    break
                
                pm_page = client.payment_methods.list(
                    member_id=member_id,
                    cursor=pm_page.page_info.end_cursor
                )
        
        session['status'] = 'completed'
        add_log(session_id, "✨ Processing complete!", "success")
    
    except Exception as e:
        session['status'] = 'error'
        add_log(session_id, f"💥 Error: {str(e)}", "error")

def add_log(session_id, message, log_type='info'):
    """Add log message to session"""
    if session_id in sessions:
        sessions[session_id]['logs'].append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'type': log_type
        })

if __name__ == '__main__':
    app.run(debug=True, port=5001)

