# GitHub Repository Setup Guide

## 🚀 YOUR SETUP (Owner - main branch)

### Step 1: Initialize Repository
```bash
cd /c/Users/chait/Downloads/ml_projects_sample

# Check current status
git status
```

### Step 2: Configure Git with Your Details
```bash
git config --global user.name "chaitanyacharan07"
git config --global user.email "chaitanyacharan07@gmail.com"

# Verify configuration
git config --list
```

### Step 3: Rename Current Branch to main
```bash
git branch -M main
```

### Step 4: Add Remote Repository
```bash
git remote add origin https://github.com/pardeep1916P/ml-microservices.git
```

### Step 5: Push to main Branch
```bash
git push -u origin main
```

### Step 6: Create master Branch for Friend
```bash
# Create master branch locally
git branch master

# Push master branch to remote
git push -u origin master

# Verify branches
git branch -a
```

---

## 📋 Complete Commands for You (Copy & Paste)

```bash
# Navigate to project
cd /c/Users/chait/Downloads/ml_projects_sample

# Configure git
git config --global user.name "chaitanyacharan07"
git config --global user.email "chaitanyacharan07@gmail.com"

# Rename to main
git branch -M main

# Add remote
git remote add origin https://github.com/pardeep1916P/ml-microservices.git

# Push main branch
git push -u origin main

# Create and push master branch
git branch master
git push -u origin master

# Verify
git branch -a
```

---

## 🔧 After Initial Push

Once you've pushed both branches to GitHub:

### Add Your Friend as Collaborator
1. Go to GitHub repo: `https://github.com/pardeep1916P/ml-microservices`
2. Click **Settings** → **Collaborators**
3. Click **Add people**
4. Search for your friend's GitHub username
5. Select and send invitation

---

## 👥 YOUR FRIEND'S SETUP (Collaborator - master branch)

### Step 1: Configure Git
```bash
git config --global user.name "ahamad abdul"
git config --global user.email "ahamadabdul433@gmail.com"
```

### Step 2: Clone Repository
```bash
cd ~/Projects  # Or any desired location
git clone https://github.com/pardeep1916P/ml-microservices.git
cd ml-microservices
```

### Step 3: Switch to master Branch
```bash
# List all branches
git branch -a

# Switch to master branch
git checkout master

# Or create local tracking branch
git checkout -b master origin/master
```

### Step 4: Verify Setup
```bash
# Check current branch
git branch

# Check branch tracking
git branch -v

# Check remote
git remote -v
```

---

## 📝 Complete Commands for Friend (Copy & Paste)

```bash
# Configure git
git config --global user.name "ahamad abdul"
git config --global user.email "ahamadabdul433@gmail.com"

# Clone repository
git clone https://github.com/pardeep1916P/ml-microservices.git
cd ml-microservices

# Switch to master branch
git checkout master

# Verify setup
git branch -v
```

---

## 🔄 Branch Strategy

```
Repository: ml-microservices
├── main          (Your branch - Owner)
│   ├── You work here
│   ├── You merge tested code
│   └── Production ready
│
└── master        (Friend's branch - Collaborator)
    ├── Friend works here
    ├── Friend pushes changes
    └── Independent development
```

---

## 💬 Collaboration Workflow

### You (Owner on main)
```bash
# Make changes
git add .
git commit -m "Add new feature"
git push origin main

# If you want to see friend's work
git fetch origin
git checkout master
```

### Your Friend (Collaborator on master)
```bash
# Make changes
git add .
git commit -m "Add new feature"
git push origin master

# If they want to see your work
git fetch origin
git checkout main
```

---

## 🔗 Merging Branches (Optional)

If you want to merge one branch into another:

### You Merge Friend's Work into main
```bash
git checkout main
git pull origin main
git merge master
git push origin main
```

### Friend Merges Your Work into master
```bash
git checkout master
git pull origin master
git merge main
git push origin master
```

---

## 🚨 Important Notes

✅ **DO:**
- Pull before starting work
- Commit frequently
- Push regularly
- Use clear commit messages
- Update your branch regularly

❌ **DON'T:**
- Force push (`--force`) without permission
- Commit `.env` files (protected by .gitignore)
- Merge without testing
- Push directly without reviewing changes

---

## 📊 Useful Commands

```bash
# See all commits
git log --oneline

# See who changed what
git log --oneline --all --graph

# Check status
git status

# See differences
git diff

# Undo last commit (if not pushed)
git reset HEAD~1

# Sync with remote
git fetch origin
git pull origin [branch-name]
```

---

## 🆘 Troubleshooting

### Issue: "Permission denied (publickey)"
**Solution**: Set up SSH keys on GitHub

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub: Settings → SSH Keys → New SSH Key
```

### Issue: "Your branch is behind origin"
```bash
git pull origin [branch-name]
```

### Issue: Merge conflicts
1. Open conflicted files
2. Resolve conflicts manually
3. `git add .`
4. `git commit -m "Resolved conflicts"`
5. `git push`

### Issue: Wrong branch tracking
```bash
# Set upstream branch
git branch --set-upstream-to=origin/master master
```

---

## 📞 Verification Steps

After your friend clones:

### Friend's Verification
```bash
# Should show: On branch master
git status

# Should show both branches
git branch -a

# Should show your commits
git log --oneline

# Should show both remotes if needed
git remote -v
```

---

## ✅ Final Checklist

- [ ] You've configured git with your email
- [ ] Repository created on GitHub
- [ ] You pushed `main` branch
- [ ] You created and pushed `master` branch
- [ ] Friend is added as collaborator
- [ ] Friend has configured git with their email
- [ ] Friend cloned the repository
- [ ] Friend switched to `master` branch
- [ ] Both can see each other's branch

---

**Setup Date**: November 25, 2025  
**Repository**: ml-microservices  
**Owner**: chaitanyacharan07  
**Collaborator**: ahamadabdul433
