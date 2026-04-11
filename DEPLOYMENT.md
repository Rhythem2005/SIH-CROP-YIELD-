# 🚀 Production Deployment Guide

## Overview
This guide covers deploying:
- **Backend**: FastAPI on Render (https://render.com)
- **Frontend**: React on Vercel (https://vercel.com)
- **Database**: MongoDB Atlas (https://www.mongodb.com/cloud/atlas)

---

## 📋 Pre-Deployment Checklist

- [ ] Update `.env.example` files (✅ Done)
- [ ] Install latest dependencies: `pip install -r requirements.txt` (backend)
- [ ] Install latest dependencies: `npm install` (frontend)
- [ ] Test locally: `npm run dev` (frontend) + `uvicorn app:app --reload` (backend)
- [ ] Create MongoDB Atlas cluster
- [ ] Get Gemini API key from https://ai.google.dev/api-keys
- [ ] Verify all API endpoints work: `/api/chat`, `/predict_yield`, `/analyze_crop_image`

---

## 🔧 Backend Deployment (Render)

### Step 1: Prepare Backend for Production

1. **Ensure `Procfile` exists** (already created):
   ```
   web: uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

2. **Ensure `requirements.txt` has pinned versions** (already done)

3. **Ensure `.env.example` is in root** (already created)

### Step 2: Deploy to Render

1. Push code to GitHub
2. Go to https://render.com/dashboard
3. Click **"+ New Web Service"**
4. Connect your GitHub repository
5. Use these settings:

   | Setting | Value |
   |---------|-------|
   | **Name** | `crop-yield-api` (or any name) |
   | **Environment** | Python |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
   | **Python Version** | 3.11 |

6. Click **"Create Web Service"**

### Step 3: Set Environment Variables on Render

After deployment, go to **Settings** → **Environment**:

```
MONGO_URL=<your-mongodb-atlas-url>
DB_NAME=crop_db
GEMINI_KEY=<your-gemini-api-key>
ALLOWED_ORIGINS=https://your-frontend-vercel-url.vercel.app,http://localhost:5174
```

⚠️ **Important**: 
- Get MongoDB URL from MongoDB Atlas (Connection String)
- Get Gemini key from https://ai.google.dev/api-keys
- Replace `https://your-frontend-vercel-url.vercel.app` with actual Vercel URL (get it after step in Frontend)

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

No changes needed—already configured to detect environment:
- Development: Uses `http://localhost:8000`
- Production: Uses environment variable `VITE_API_BASE_URL`

### Step 2: Deploy to Vercel

1. Push code to GitHub
2. Go to https://vercel.com/dashboard
3. Click **"Add New..."** → **"Project"**
4. Import your GitHub repository
5. Vercel auto-detects Vite setup (no manual config needed)

### Step 3: Set Environment Variables on Vercel

In **Settings** → **Environment Variables**:

```
VITE_API_BASE_URL=https://your-rendered-backend-url.onrender.com
```

Example: `https://crop-yield-api.onrender.com`

### Step 4: Deploy

Click **"Deploy"** and wait ~3-5 minutes for build to complete.

---

## ✅ Post-Deployment Verification

### Test Backend

```bash
# Test API health
curl https://your-backend.onrender.com/docs

# Test chat endpoint
curl -X POST https://your-backend.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How to grow rice?"}'
```

### Test Frontend

1. Navigate to `https://your-frontend.vercel.app`
2. Test each feature:
   - ✅ Dashboard loads
   - ✅ Chatbot works (bottom-right corner)
   - ✅ Input data form submits
   - ✅ Photo upload works

### Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| **API calls fail (CORS error)** | Update `ALLOWED_ORIGINS` on Render to include Vercel URL |
| **Chatbot returns 503** | Check Gemini API key on Render is set correctly |
| **Images won't upload** | Ensure backend has proper error handling |
| **Database connection fails** | Verify MongoDB URL in Render doesn't have special characters |

---

## 🔐 Security Checklist

- [ ] NO hardcoded API keys in frontend
- [ ] `.env` files are in `.gitignore` (not committed to GitHub)
- [ ] CORS restricted to frontend URL only
- [ ] API keys stored only in deployment platform environment
- [ ] All sensitive data passed via environment variables
- [ ] No localhost references in production code

---

## 📱 MongoDB Atlas Setup (Quick Guide)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create cluster (M0 free tier is fine)
4. Go to **Network Access** → Add `0.0.0.0/0` (allow all, for Render)
5. Go to **Database Users** → Create user (username/password)
6. Click **Connect** → Copy **Connection String**
7. Replace `<password>` with your user password
8. Paste into Render `MONGO_URL` environment variable

---

## 🔄 Updating After Deployment

### Backend (Render)

1. Make changes locally
2. `git push` to main branch
3. Render auto-deploys within 1-2 minutes
4. Check deployment logs in Render dashboard

### Frontend (Vercel)

1. Make changes locally
2. `git push` to main branch
3. Vercel auto-deploys within 2-3 minutes
4. Check deployment logs in Vercel dashboard

---

## 📊 Monitoring

### Render
- **Logs**: Dashboard → "Logs" tab
- **Status**: Check for errors or timeout issues

### Vercel
- **Logs**: Deployments → Click deploy → "Logs" tab
- **Analytics**: Check in Real-time Analytics

---

## 💰 Cost Estimates

| Service | Plan | Cost |
|---------|------|------|
| Render (Backend) | Free → Paid | $7-20/month |
| Vercel (Frontend) | Free | $0/month |
| MongoDB Atlas | Free tier | $0/month |
| Gemini API | Free tier | $0 (with limits) |

**Total**: ~$7-20/month for production

---

## 🆘 Support

If deployment fails:
1. Check Render/Vercel logs for error messages
2. Verify all environment variables are set
3. Test locally first: `npm run dev` + `uvicorn app:app --reload`
4. Make sure Python 3.11+ and Node 18+ are installed locally

