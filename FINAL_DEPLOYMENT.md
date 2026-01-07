# 🌐 FINAL DEPLOYMENT GUIDE
## Deploy to whopcharge.com (5.161.116.77)

---

## 📋 QUICK DEPLOYMENT (Copy & Paste)

### **Step 1: SSH to Your Server**
```bash
ssh root@5.161.116.77
```

### **Step 2: Run Complete Deployment Script**

Copy and paste this entire command:

```bash
#!/bin/bash
set -e

echo "🚀 Deploying Whop Charge to whopcharge.com..."
echo ""

# Update system
echo "[1/10] Updating system..."
apt update && apt upgrade -y

# Install dependencies
echo "[2/10] Installing dependencies..."
apt install -y python3 python3-pip python3-venv nginx curl certbot python3-certbot-nginx git

# Create application directory
echo "[3/10] Creating application directory..."
mkdir -p /home/whopcharge
cd /home/whopcharge

# Clone from GitHub
echo "[4/10] Cloning application from GitHub..."
git clone https://github.com/mohamederrajy/whop-auto.git . 2>/dev/null || git pull origin main

# Setup Python virtual environment
echo "[5/10] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service
echo "[6/10] Creating systemd service..."
cat > /etc/systemd/system/whopcharge.service << 'EOF'
[Unit]
Description=Whop Charge Automation Platform
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/whopcharge
Environment="PATH=/home/whopcharge/venv/bin"
ExecStart=/home/whopcharge/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5001 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable whopcharge
systemctl start whopcharge

# Configure Nginx
echo "[7/10] Configuring Nginx..."
cat > /etc/nginx/sites-available/whopcharge << 'EOF'
server {
    listen 80;
    server_name whopcharge.com www.whopcharge.com;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
EOF

ln -sf /etc/nginx/sites-available/whopcharge /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# Setup SSL Certificate
echo "[8/10] Installing SSL certificate..."
certbot --nginx -d whopcharge.com -d www.whopcharge.com --agree-tos --non-interactive --email admin@whopcharge.com

# Setup firewall
echo "[9/10] Configuring firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Fix permissions
echo "[10/10] Fixing permissions..."
chown -R www-data:www-data /home/whopcharge
chmod -R 755 /home/whopcharge

# Verify deployment
echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "🌐 Your application is running at:"
echo "   https://whopcharge.com"
echo ""
echo "📧 Login Credentials:"
echo "   Email: admin@whopcharge.com"
echo "   Password: SecureWhop2024!@#"
echo ""
echo "⚠️  CHANGE PASSWORD IMMEDIATELY!"
echo ""
echo "📋 Useful Commands:"
echo "   View logs: journalctl -u whopcharge -f"
echo "   Restart: systemctl restart whopcharge"
echo "   Status: systemctl status whopcharge"
echo ""
```

**Save as script and run:**

```bash
cat > /home/deploy.sh << 'DEPLOYEOF'
#!/bin/bash
set -e

echo "🚀 Deploying Whop Charge to whopcharge.com..."
echo ""

# Update system
echo "[1/10] Updating system..."
apt update && apt upgrade -y

# Install dependencies
echo "[2/10] Installing dependencies..."
apt install -y python3 python3-pip python3-venv nginx curl certbot python3-certbot-nginx git

# Create application directory
echo "[3/10] Creating application directory..."
mkdir -p /home/whopcharge
cd /home/whopcharge

# Clone from GitHub
echo "[4/10] Cloning application from GitHub..."
git clone https://github.com/mohamederrajy/whop-auto.git . 2>/dev/null || git pull origin main

# Setup Python virtual environment
echo "[5/10] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service
echo "[6/10] Creating systemd service..."
cat > /etc/systemd/system/whopcharge.service << 'EOF'
[Unit]
Description=Whop Charge Automation Platform
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/whopcharge
Environment="PATH=/home/whopcharge/venv/bin"
ExecStart=/home/whopcharge/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5001 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable whopcharge
systemctl start whopcharge

# Configure Nginx
echo "[7/10] Configuring Nginx..."
cat > /etc/nginx/sites-available/whopcharge << 'EOF'
server {
    listen 80;
    server_name whopcharge.com www.whopcharge.com;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
EOF

ln -sf /etc/nginx/sites-available/whopcharge /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# Setup SSL Certificate
echo "[8/10] Installing SSL certificate..."
certbot --nginx -d whopcharge.com -d www.whopcharge.com --agree-tos --non-interactive --email admin@whopcharge.com

# Setup firewall
echo "[9/10] Configuring firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Fix permissions
echo "[10/10] Fixing permissions..."
chown -R www-data:www-data /home/whopcharge
chmod -R 755 /home/whopcharge

# Verify deployment
echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "🌐 Your application is running at:"
echo "   https://whopcharge.com"
echo ""
echo "📧 Login Credentials:"
echo "   Email: admin@whopcharge.com"
echo "   Password: SecureWhop2024!@#"
echo ""
echo "⚠️  CHANGE PASSWORD IMMEDIATELY!"
echo ""
echo "📋 Useful Commands:"
echo "   View logs: journalctl -u whopcharge -f"
echo "   Restart: systemctl restart whopcharge"
echo "   Status: systemctl status whopcharge"
echo ""
DEPLOYEOF

chmod +x /home/deploy.sh
bash /home/deploy.sh
```

---

## ✅ STEP-BY-STEP MANUAL DEPLOYMENT

If the automated script doesn't work, follow these steps:

### **Step 1: SSH to Server**
```bash
ssh root@5.161.116.77
```

### **Step 2: Update System**
```bash
apt update
apt upgrade -y
apt install -y python3 python3-pip python3-venv nginx curl certbot python3-certbot-nginx git
```

### **Step 3: Clone Application**
```bash
cd /home
rm -rf whopcharge  # If exists
git clone https://github.com/mohamederrajy/whop-auto.git whopcharge
cd whopcharge
```

### **Step 4: Setup Python Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### **Step 5: Test Application**
```bash
python3 app.py
# Should show: WARNING in app.run() is not recommended... Running on http://127.0.0.1:5001
# Press Ctrl+C to stop
```

### **Step 6: Create Systemd Service**
```bash
sudo tee /etc/systemd/system/whopcharge.service > /dev/null << 'EOF'
[Unit]
Description=Whop Charge Automation Platform
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/whopcharge
Environment="PATH=/home/whopcharge/venv/bin"
ExecStart=/home/whopcharge/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5001 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### **Step 7: Enable & Start Service**
```bash
systemctl daemon-reload
systemctl enable whopcharge
systemctl start whopcharge
systemctl status whopcharge
```

Should show: **active (running)**

### **Step 8: Configure Nginx**
```bash
sudo tee /etc/nginx/sites-available/whopcharge > /dev/null << 'EOF'
server {
    listen 80;
    server_name whopcharge.com www.whopcharge.com;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
EOF
```

### **Step 9: Enable Nginx Site**
```bash
ln -s /etc/nginx/sites-available/whopcharge /etc/nginx/sites-enabled/whopcharge
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

### **Step 10: Setup SSL Certificate**
```bash
certbot --nginx -d whopcharge.com -d www.whopcharge.com --agree-tos --non-interactive --email admin@whopcharge.com
```

### **Step 11: Setup Firewall**
```bash
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw status
```

### **Step 12: Fix Permissions**
```bash
chown -R www-data:www-data /home/whopcharge
chmod -R 755 /home/whopcharge
```

---

## 🔍 VERIFY DEPLOYMENT

After setup, verify everything works:

```bash
# Check Flask is running
curl http://127.0.0.1:5001

# Check service status
systemctl status whopcharge

# View logs
journalctl -u whopcharge -f

# Check Nginx
systemctl status nginx
nginx -t

# Verify SSL
curl -I https://whopcharge.com
```

---

## 🌐 ACCESS YOUR APPLICATION

Open your browser:

```
https://whopcharge.com
```

Login with:
- **Email:** admin@whopcharge.com
- **Password:** SecureWhop2024!@#

---

## 🔐 CHANGE ADMIN PASSWORD (IMPORTANT!)

Your credentials are hardcoded in the HTML file. Change them:

```bash
# Edit the HTML file
nano /home/whopcharge/templates/index.html

# Find line ~30:
# if (email === 'admin@whopcharge.com' && password === 'SecureWhop2024!@#')

# Change to your new password, save with Ctrl+O, Enter, Ctrl+X

# Restart application
systemctl restart whopcharge

# Verify with new password at https://whopcharge.com
```

---

## 📋 USEFUL COMMANDS

```bash
# View live logs
journalctl -u whopcharge -f

# View last 50 lines
journalctl -u whopcharge -n 50

# Restart application
systemctl restart whopcharge

# Stop application
systemctl stop whopcharge

# Start application
systemctl start whopcharge

# Check status
systemctl status whopcharge

# View Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Restart Nginx
systemctl restart nginx

# Check SSL certificate
certbot certificates

# Renew SSL (auto-renews, but you can force)
certbot renew
```

---

## 🚨 TROUBLESHOOTING

### Problem: "Connection refused"

```bash
# Check if Flask is running
curl http://127.0.0.1:5001

# Check service status
systemctl status whopcharge

# View detailed logs
journalctl -u whopcharge -n 100
```

### Problem: "Nginx proxy error"

```bash
# Test Nginx config
nginx -t

# Verify Flask is listening
netstat -tulpn | grep 5001

# Restart Nginx
systemctl restart nginx
```

### Problem: "Certificate installation failed"

```bash
# Check if certbot is working
certbot certificates

# Manual renewal
certbot renew --dry-run

# Full renewal
certbot renew
```

### Problem: "Port 5001 already in use"

```bash
lsof -i :5001
kill -9 <PID>
systemctl restart whopcharge
```

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] SSH'd into server: `ssh root@5.161.116.77`
- [ ] System updated: `apt update && apt upgrade -y`
- [ ] Dependencies installed
- [ ] Cloned from GitHub: `git clone https://github.com/mohamederrajy/whop-auto.git`
- [ ] Virtual environment created and activated
- [ ] Python packages installed: `pip install -r requirements.txt`
- [ ] Systemd service created and running
- [ ] Nginx configured and running
- [ ] SSL certificate installed
- [ ] Firewall enabled
- [ ] Permissions fixed
- [ ] Application accessible at https://whopcharge.com
- [ ] Login works with credentials
- [ ] **CHANGED admin password**
- [ ] Logs being monitored

---

## 🎉 DEPLOYMENT COMPLETE!

Your application is now live at:

```
🌐 https://whopcharge.com
```

**Status:** ✅ Running on 5.161.116.77  
**Domain:** whopcharge.com  
**SSL:** ✅ HTTPS Enabled  
**Service:** ✅ Auto-restart on failure  
**Firewall:** ✅ Enabled

---

**Created:** January 7, 2026  
**Repository:** https://github.com/mohamederrajy/whop-auto

