# How to push this project to GitHub (step-by-step)

## 1) Install Git (if not installed)
- Download: https://git-scm.com/download/win
- Follow the installer and keep defaults

## 2) Configure Git (one-time)
```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 3) Initialize (if needed), add, and commit
```powershell
# Initialize only if this isn't already a git repo
# git init

# Add all files
git add -A

git commit -m "chore: initial project files — real-time monitoring with AI predictions"
```

## 4) Create a GitHub repo
Option A (recommended if you have GitHub CLI):
```powershell
# Install GitHub CLI: https://cli.github.com/
gh auth login
gh repo create YOUR_USERNAME/real-time-monitoring --public --source=. --remote=origin --push
```

Option B (web UI):
1. Go to https://github.com/new
2. Create repo name (e.g., `real-time-monitoring`) and click Create
3. Follow the instructions under "…or push an existing repository from the command line":

```powershell
git remote add origin https://github.com/YOUR_USERNAME/real-time-monitoring.git
git branch -M main
git push -u origin main
```

## 5) Verify GitHub Actions
- The workflow `.github/workflows/ci.yml` is already included.
- Once you push, the Actions tab will show the CI run.

## Notes
- If your repo uses a different branch name, adjust commands accordingly.
- If you want the repository to be private, choose that option on GitHub when creating.
