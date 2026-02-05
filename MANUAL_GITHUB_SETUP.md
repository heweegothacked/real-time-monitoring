# Manual GitHub Repository Setup

Since GitHub CLI authentication requires interactive setup, here's how to push manually:

## Option 1: Push to existing GitHub repo (recommended)
1. **Create the repo on GitHub.com**
   - Go to https://github.com/new
   - Repository name: `real-time-monitoring`
   - Description: "Real-time monitoring system with AI-powered anomaly detection and trend prediction"
   - Choose: **Public**
   - Click **Create repository**

2. **Copy the HTTPS URL** from GitHub (looks like: `https://github.com/YOUR_USERNAME/real-time-monitoring.git`)

3. **Push from your local repo**
   ```powershell
   & "C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/YOUR_USERNAME/real-time-monitoring.git
   & "C:\Program Files\Git\cmd\git.exe" branch -M main
   & "C:\Program Files\Git\cmd\git.exe" push -u origin main
   ```
   When prompted, enter your GitHub username and a **Personal Access Token** (from GitHub → Settings → Developer settings → Personal access tokens).

## Option 2: Use SSH (if already configured)
```powershell
& "C:\Program Files\Git\cmd\git.exe" remote add origin git@github.com:YOUR_USERNAME/real-time-monitoring.git
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```

## Option 3: GitHub Desktop
- Download GitHub Desktop from https://desktop.github.com
- Open the Project1 folder
- Publish to GitHub (simple UI)

---

Once pushed, the CI workflow will run automatically and validate all tests pass! ✅
