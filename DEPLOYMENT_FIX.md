# 🔧 Deployment Fix Guide

## ✅ Fixed Issue: whop_sdk Version

### Problem
```
ERROR: Could not find a version that satisfies the requirement whop_sdk==0.1.0
```

### Solution
Updated `requirements.txt` to use the latest available version of `whop_sdk`:

**Changed from:**
```
whop_sdk==0.1.0
```

**Changed to:**
```
whop_sdk==0.0.20
```

---

## 🚀 How to Fix Your Server Installation

If you've already started the installation on your server, follow these steps:

### Step 1: Update requirements.txt

```bash
# SSH to your server
ssh root@5.161.116.77
cd /home/whopcharge

# Pull the latest code from GitHub
git pull origin main
```

### Step 2: Reinstall Python packages

```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall with correct versions
pip install --upgrade -r requirements.txt
```

### Step 3: Restart the application

```bash
# Restart systemd service
systemctl restart whopcharge

# Check status
systemctl status whopcharge

# View logs to verify it's working
journalctl -u whopcharge -f
```

---

## 📋 Correct requirements.txt (Current)

```
Flask==2.3.3
Flask-CORS==4.0.0
whop_sdk==0.0.20    ← FIXED (was 0.1.0)
python-dotenv==1.0.0
gunicorn==21.2.0
```

---

## ✅ Available whop_sdk Versions

The whop_sdk package has these available versions:
- 0.0.1 through 0.0.20 ✅ (latest)

We're now using `0.0.20` which is the newest available version.

---

## 🎯 Deployment Instructions (Fresh Start)

If starting fresh on your server:

```bash
# 1. SSH to server
ssh root@5.161.116.77

# 2. Create directory
mkdir -p /home/whopcharge
cd /home/whopcharge

# 3. Clone the fixed repository
git clone https://github.com/mohamederrajy/whop-auto.git .

# 4. Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies (with CORRECTED versions)
pip install --upgrade pip
pip install -r requirements.txt

# 6. Test installation
python3 -c "from flask import Flask; from whop_sdk import Whop; print('✅ All dependencies installed correctly')"

# 7. Run the app
python3 app.py

# Should output: Running on http://127.0.0.1:5001
```

---

## 📊 Git Commits

| Commit | Message |
|--------|---------|
| ed10f31 | Initial commit: Whop Charge automation platform |
| 2eb5304 | Fix: Update whop_sdk to version 0.0.20 (latest available) |

✅ Latest commit is now on GitHub

---

## 🔍 Verify Installation

After installation, test with:

```bash
# Activate environment
source venv/bin/activate

# Check installed packages
pip list

# Expected output should include:
# Flask               2.3.3
# Flask-Cors          4.0.0
# whop-sdk            0.0.20
# python-dotenv       1.0.0
# gunicorn            21.2.0
```

---

## 🚨 If You Still Get Errors

### Error: "ModuleNotFoundError: No module named 'whop_sdk'"

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall
pip install whop_sdk==0.0.20

# Verify
python3 -c "from whop_sdk import Whop; print('✅ whop_sdk imported successfully')"
```

### Error: "Systemd service failed to start"

```bash
# Check what went wrong
journalctl -u whopcharge -n 50

# If it's a Python error, check the logs
systemctl status whopcharge

# Reinstall packages
source venv/bin/activate
pip install -r requirements.txt --force-reinstall

# Restart service
systemctl restart whopcharge
```

---

## ✅ Deployment Checklist (Updated)

- [x] Fixed whop_sdk version in requirements.txt
- [x] Updated GitHub repository with correct version
- [x] All dependencies now available
- [ ] Pull latest code on server: `git pull origin main`
- [ ] Reinstall packages: `pip install -r requirements.txt`
- [ ] Restart service: `systemctl restart whopcharge`
- [ ] Verify running: `systemctl status whopcharge`
- [ ] Access at: https://whopcharge.com

---

**Status:** ✅ Fixed and Ready for Deployment  
**Latest Commit:** 2eb5304 (Fix: Update whop_sdk to version 0.0.20)  
**Date:** January 7, 2026

