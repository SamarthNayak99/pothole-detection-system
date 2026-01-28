# 🚀 Railway Deployment Guide for Pothole Detection App

## **What is Railway?**
Railway is a modern cloud platform that makes deploying web applications super easy. It's perfect for your pothole detection app because:
- ✅ Supports Python backend (FastAPI)
- ✅ Free tier with $5 credit/month
- ✅ Automatic HTTPS
- ✅ Easy environment variable management
- ✅ One-click deployment from GitHub

---

## **📋 Prerequisites**

Before you start, make sure you have:
- [ ] GitHub account (create at github.com if you don't have one)
- [ ] Railway account (we'll create this together)
- [ ] Git installed on your computer
- [ ] Your project ready (we've already prepared the config files!)

---

## **Step 1: Create GitHub Account & Install Git**

### 1.1 Create GitHub Account (if you don't have one)
1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration process
4. Verify your email

### 1.2 Install Git
1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings (just keep clicking "Next")
4. Restart your computer after installation

### 1.3 Configure Git (First Time Only)
Open PowerShell and run:
```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

---

## **Step 2: Push Your Project to GitHub**

### 2.1 Initialize Git Repository
Open PowerShell in your project folder and run:

```powershell
cd "c:\Users\samar\Desktop\DTL\dtl el pothole-S"
git init
git add .
git commit -m "Initial commit - Pothole Detection App"
```

### 2.2 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `pothole-detection-app`
3. Description: "AI-powered pothole detection system with mobile web app"
4. Keep it **Public** (or Private if you prefer)
5. **DO NOT** check "Add README" or ".gitignore" (we already have these)
6. Click "Create repository"

### 2.3 Push to GitHub
After creating the repo, GitHub will show you commands. Run these in PowerShell:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/pothole-detection-app.git
git branch -M main
git push -u origin main
```

**Replace `YOUR-USERNAME` with your actual GitHub username!**

---

## **Step 3: Create Railway Account**

1. Go to https://railway.app
2. Click "Login" or "Start a New Project"
3. Sign up using your **GitHub account** (click "Login with GitHub")
4. Authorize Railway to access your GitHub
5. You'll get **$5 free credit per month** (no credit card required!)

---

## **Step 4: Deploy to Railway**

### 4.1 Create New Project
1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `pothole-detection-app`
4. Railway will automatically detect it's a Python app!

### 4.2 Configure Environment Variables
This is **CRITICAL** - your app won't work without these!

1. In Railway, click on your deployed service
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add these variables one by one:

```
EMAIL_SENDER=rvcedtl@gmail.com
EMAIL_PASSWORD=vznt ndxz ktmo orqf
EMAIL_RECEIVER=samnayak64@gmail.com
PORT=8000
```

**Important:** Click "Add" after each variable!

### 4.3 Wait for Deployment
- Railway will automatically build and deploy your app
- This takes 3-5 minutes (first time)
- You'll see logs in the "Deployments" tab
- Wait until you see "✅ Deployment successful"

### 4.4 Get Your Public URL
1. Go to **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**
4. Railway will give you a URL like: `https://your-app-name.up.railway.app`

**🎉 Your backend is now live!**

---

## **Step 5: Update Frontend to Use Production Backend**

Now you need to update your frontend to use the Railway URL instead of localhost.

### 5.1 Find Your Railway URL
Copy your Railway URL (e.g., `https://pothole-detection-production.up.railway.app`)

### 5.2 Update Frontend Files
You need to replace all instances of:
- `http://localhost:8000` 
- `http://192.168.x.x:8000`

With your Railway URL:
- `https://your-app-name.up.railway.app`

**Files to update:**
- `detection.html`
- `history.html`
- `map.html`
- `mobile-detect.html`
- Any other files that call the backend API

### 5.3 Search and Replace
In each HTML file, find lines like:
```javascript
const API_URL = 'http://localhost:8000';
```

Replace with:
```javascript
const API_URL = 'https://your-app-name.up.railway.app';
```

---

## **Step 6: Deploy Frontend**

You have two options for frontend deployment:

### **Option A: Deploy Frontend on Railway Too (Recommended)**

1. In Railway, click **"+ New"** → **"Empty Service"**
2. Link to the same GitHub repo
3. Go to Settings → Change "Root Directory" to `/` (leave empty)
4. Add a new file called `nixpacks.toml` in your project root:

```toml
[phases.setup]
nixPkgs = ['nodejs', 'npm']

[phases.install]
cmds = ['npm install']

[phases.build]
cmds = ['npm run build']

[start]
cmd = 'npx serve -s dist -p $PORT'
```

5. Push to GitHub:
```powershell
git add .
git commit -m "Add frontend deployment config"
git push
```

6. Railway will auto-deploy the frontend
7. Generate a domain for the frontend service too

### **Option B: Use Vercel for Frontend (Easier)**

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "New Project"
4. Select your `pothole-detection-app` repo
5. Vercel will auto-detect Vite
6. Click "Deploy"
7. Done! You'll get a URL like `https://pothole-detection.vercel.app`

---

## **Step 7: Test Your Deployed App**

### 7.1 Test Backend API
Open your browser and go to:
```
https://your-backend-url.up.railway.app/docs
```

You should see the FastAPI documentation page!

### 7.2 Test Frontend
1. Open your frontend URL (Railway or Vercel)
2. Try detecting a pothole
3. Check if it appears on the map
4. Verify email notifications work

---

## **Step 8: Important Notes**

### ⚠️ **Data Persistence Issue**
Railway's free tier has **ephemeral storage**, meaning:
- Your CSV file and images will be **deleted** when the app restarts
- This happens during redeployments or after 24 hours of inactivity

### **Solutions:**

**Option 1: Use Railway Volumes (Recommended)**
1. In Railway, go to your service
2. Click "Volumes" tab
3. Click "+ New Volume"
4. Mount path: `/app/backend/data`
5. Update your code to save CSV to `/app/backend/data/potholes.csv`

**Option 2: Upgrade to Paid Plan**
- $5/month for persistent storage
- Worth it for production use

**Option 3: Use Database (Best for Production)**
- Add PostgreSQL or MongoDB
- We can help you migrate from CSV to database later

---

## **Step 9: Monitoring & Maintenance**

### Check Logs
1. Go to Railway dashboard
2. Click on your service
3. View "Logs" tab to see real-time activity

### Update Your App
Whenever you make changes:
```powershell
git add .
git commit -m "Description of changes"
git push
```
Railway will automatically redeploy!

---

## **🎯 Quick Checklist**

- [ ] Git installed and configured
- [ ] Project pushed to GitHub
- [ ] Railway account created
- [ ] Backend deployed to Railway
- [ ] Environment variables added
- [ ] Railway domain generated
- [ ] Frontend updated with Railway URL
- [ ] Frontend deployed (Railway or Vercel)
- [ ] Tested detection on mobile device
- [ ] Email notifications working
- [ ] Map showing potholes

---

## **💰 Cost Breakdown**

**Free Tier (What you get for $0):**
- Backend hosting: FREE ($5 credit/month)
- Frontend hosting: FREE (Vercel)
- Custom subdomain: FREE
- HTTPS/SSL: FREE
- **Total: $0/month** ✅

**If you need more:**
- Railway Pro: $5/month (persistent storage)
- Custom domain: $10-15/year (optional)

---

## **🆘 Troubleshooting**

### "Build Failed" Error
- Check Railway logs for specific error
- Make sure `requirements.txt` is in the root folder
- Verify Python version in `runtime.txt`

### "Application Error" After Deployment
- Check environment variables are set correctly
- View logs for error messages
- Make sure PORT variable is set

### Images Not Loading
- Check CORS settings in `main.py`
- Verify image paths are correct
- Consider using Cloudinary for image storage

### Email Not Sending
- Verify EMAIL_* environment variables
- Check Gmail app password is correct
- Look at logs for SMTP errors

---

## **📞 Need Help?**

If you get stuck at any step, just ask! I can:
- Help you debug errors
- Update code for you
- Explain any step in more detail
- Help migrate to a database

---

## **🚀 You're Ready!**

Once deployed, your app will be accessible from **anywhere in the world**!

Share your Railway URL with:
- Friends for testing
- Professors for demo
- Anyone with internet access

**No more "connect to same WiFi" issues!** 🎉
