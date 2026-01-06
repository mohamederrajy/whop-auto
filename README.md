# Whop Payment Automation Platform 🚀

A modern web-based platform to automate payment creation for your Whop business. Instead of running the script directly, you can now use a beautiful dashboard to manage all your payment processing.

## Features ✨

- **Modern Dashboard UI** - Beautiful gradient design with real-time statistics
- **Secure Configuration Input** - Enter your API credentials safely
- **Live Processing Logs** - Watch payments being created in real-time
- **Progress Tracking** - See members found, successes, and failures
- **Status Monitoring** - Real-time status updates during processing
- **Responsive Design** - Works on desktop, tablet, and mobile

## Setup Instructions 📋

### 1. Install Dependencies

```bash
cd /Users/aziz/Documents/rebiil-whop
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on: **http://localhost:5001**

### 3. Using the Dashboard

1. **Enter Configuration:**
   - API Key: Your Whop API key (starts with `apik_`)
   - Company ID: Your company ID (starts with `biz_`)
   - Plan ID: Your plan ID (starts with `plan_`)

2. **Start Processing:**
   - Click "Start Processing" button
   - Watch real-time logs as payments are created
   - View statistics updating in the dashboard

3. **Monitor Results:**
   - Members Found: Total members processed
   - Success: Number of successful payments
   - Failed: Number of failed attempts

## Project Structure 📁

```
rebiil-whop/
├── app.py              # Flask backend server
├── script.py           # Original Python script
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Dashboard UI
└── README.md          # This file
```

## How It Works 🔧

1. **Frontend (HTML/CSS/JavaScript)**
   - Collects user credentials
   - Displays real-time updates
   - Shows beautiful dashboard with stats

2. **Backend (Flask Python)**
   - Receives credentials from dashboard
   - Runs payment processing in background thread
   - Streams logs back to frontend
   - Manages session data

3. **Payment Processing**
   - Fetches all company members
   - Gets payment methods for each member
   - Creates payments for each method
   - Logs success/failure for each attempt

## Security Notes 🔒

- Never commit your actual API credentials to version control
- API key is sent securely over HTTPS in production
- Consider using environment variables for credentials

## Troubleshooting 🐛

**Connection refused on localhost:5001?**
- Make sure Flask is running: `python3 app.py`
- Check port 5001 isn't in use: `lsof -i :5001`

**API authentication errors?**
- Verify your API key is correct
- Check if your company ID is valid
- Ensure plan ID exists in your company

**Processing seems stuck?**
- Check browser console for errors
- Monitor Flask server logs
- Large member lists may take time

## Future Enhancements 🚀

- [ ] Database to store processing history
- [ ] User authentication
- [ ] Scheduled automation
- [ ] Webhook support for status updates
- [ ] Export reports (CSV/PDF)
- [ ] Payment retry logic
- [ ] Email notifications

---

Made with ❤️ for Whop Business Automation

