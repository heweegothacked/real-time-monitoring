# Deploy to Railway

This guide shows how to deploy the Real-Time Monitoring System to Railway in minutes.

## Why Railway?

- **Free tier** - Deploy for free with automatic scaling
- **GitHub integration** - Auto-deploy on push
- **Environment variables** - Easy configuration management
- **Custom domains** - Get a public URL for your app
- **Database support** - Optional PostgreSQL integration

---

## Step-by-Step Deployment

### 1. Create Railway Account

Go to [railway.app](https://railway.app) and sign up with GitHub.

### 2. Create New Project

1. Click **"Create a new project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub account
4. Select the `real-time-monitoring` repository

### 3. Configure Environment

Railway will auto-detect `Dockerfile` and use it. Settings:

- **Builder**: Docker
- **Port**: 8501 (Streamlit default)

### 4. Deploy

Railway will automatically:
- Build Docker image from `Dockerfile`
- Deploy container
- Assign public URL (e.g., `https://realtime-monitoring-production.up.railway.app`)

### 5. Access Your App

Once deployment completes (~2 minutes):

```
Your app is live at: https://realtime-monitoring-production.up.railway.app
```

Click the URL or add it to your portfolio!

---

## Optional: Custom Domain

Railway allows custom domains on Pro plans. For the free tier, you get a Railway subdomain.

---

## Redeployment

Any push to your `main` branch triggers automatic redeployment. To redeploy:

```bash
git add .
git commit -m "enhancement: add feature"
git push origin main
```

Railway will rebuild and redeploy automatically.

---

## Environment Variables (Optional)

If you need environment variables (e.g., API keys), add them in Railway dashboard:

1. Go to **Project > Variables**
2. Add key-value pairs
3. These are available to your app as `os.environ['KEY_NAME']`

---

## Monitoring

Railway dashboard shows:

- **Deployment logs** - See build/runtime output
- **Resource usage** - CPU, memory, storage
- **Health status** - Running, error, crashed, etc.

---

## Troubleshooting

**App crashes on startup?**
- Check logs in Railway dashboard
- Ensure `requirements.txt` has all dependencies
- Verify `Dockerfile` exposes port 8501

**Port 8501 not accessible?**
- Streamlit requires `--server.headless=true` in Docker
- Our `Dockerfile` includes this via `config.toml`

**Database persists between deploys?**
- SQLite file (`data/sensor_data.db`) is in container filesystem
- Add volume mounts if you want persistent storage across restarts

---

## Next Steps

- 📊 **Monitor live**: Visit your public URL and watch real-time data
- 🎯 **Add to portfolio**: Share the link with "Deployed on Railway"
- 🔄 **Iterate**: Make changes locally, push to GitHub, auto-deploys!

---

## Resume Impact

Add to your resume:

> **Deployed**  
> Deployed Real-Time Monitoring System to Railway cloud platform with automatic CI/CD pipeline. Application receives real-time sensor data processing and serves interactive dashboard to production.

Provide link: `https://realtime-monitoring-production.up.railway.app` (or your custom URL)
