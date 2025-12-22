# Quick Start Guide

Get the Daily Python Report up and running in 5 minutes!

## Prerequisites

- GitHub account
- Git installed
- Python 3.9+ installed

## Step 1: Create Repository

```bash
# Create a new repository on GitHub (via web UI or gh CLI)
gh repo create daily-python-report --public --clone

# Or if you prefer the web UI:
# 1. Go to https://github.com/new
# 2. Name: daily-python-report
# 3. Public/Private: Your choice
# 4. Initialize: No (we'll push our code)
# 5. Click "Create repository"
```

## Step 2: Initialize Local Repository

```bash
# Navigate to your new repo
cd daily-python-report

# Copy all files from the generated structure
# (Assuming you have the files in /tmp/daily-python-report)
cp -r /tmp/daily-python-report/* .
cp -r /tmp/daily-python-report/.github .
cp /tmp/daily-python-report/.gitignore .

# Initialize git if needed
git init
git add .
git commit -m "feat: initial commit with automated daily reporting"

# Push to GitHub
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/daily-python-report.git
git push -u origin main
```

## Step 3: Configure GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under "Workflow permissions":
   - Select **"Read and write permissions"**
   - Check **"Allow GitHub Actions to create and approve pull requests"**
4. Click **Save**

## Step 4: Test the Workflow

### Manual Trigger

1. Go to **Actions** tab in your repository
2. Click **Daily Report Generation** workflow
3. Click **Run workflow** dropdown
4. Click **Run workflow** button
5. Wait for completion (should take ~1 minute)

### Verify Results

After the workflow completes:

1. Check the **Actions** run for logs
2. Look for a new PR titled "chore: daily status report update"
3. View the PR to see the generated report
4. Check that commits show the green verified checkmark ✅

## Step 5: Test Locally (Optional)

```bash
# Run setup script
chmod +x setup.sh
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Generate report
python scripts/generate_report.py

# View generated report
cat reports/daily_status.md
```

## Step 6: Customize (Optional)

### Change Schedule

Edit [.github/workflows/daily.yml](.github/workflows/daily.yml):

```yaml
on:
  schedule:
    - cron: '0 12 * * *'  # Change to noon UTC
```

### Add Labels

Customize PR labels in the workflow:

```yaml
labels: |
  automated
  report
  documentation
  daily-update  # Add your own
```

### Branch Protection

For production use:

1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - Require signed commits (optional)
4. Save changes

## Step 7: Monitor

### Daily Operation

- Workflow runs automatically daily at 00:00 UTC
- PRs created only when data changes
- All commits are verified ✅
- Review and merge PRs as needed

### Troubleshooting

If something goes wrong:

1. Check workflow logs in Actions tab
2. Look for red X marks indicating failures
3. Review [README.md](README.md) troubleshooting section
4. Check GITHUB_STEP_SUMMARY for detailed info

## Next Steps

- ⭐ Star the repository
- 📝 Customize the report format
- 🔔 Enable notifications for new PRs
- 📊 Add custom metrics
- 🤝 Contribute improvements

## Common Issues

### "Resource not accessible by integration"

**Solution**: Enable write permissions in Settings → Actions → General

### No PR created

**Solution**: Check if report actually changed (compare with existing)

### Commits not verified

**Solution**: Ensure using correct bot email in workflow

## Getting Help

- Read [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Open an issue for bugs or questions

---

**Congratulations!** 🎉 Your automated daily reporting system is now running!
