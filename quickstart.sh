#!/bin/bash
# Quick start script for daily-python-report

echo "🚀 Daily Python Report - Quick Start"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -f "scripts/generate_report.py" ]; then
    echo "❌ Error: Run this script from the daily-python-report directory"
    exit 1
fi

echo "📋 Step 1: Testing the setup..."
python3 verify_setup.py
if [ $? -ne 0 ]; then
    echo "❌ Setup verification failed. Please check the output above."
    exit 1
fi

echo ""
echo "📋 Step 2: Running tests..."
python3 -m pip install -q pytest pytest-cov
python3 -m pytest tests/ -v --tb=short

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please check the output above."
    exit 1
fi

echo ""
echo "📋 Step 3: Generating initial report..."
python3 scripts/generate_report.py

echo ""
echo "📋 Step 4: Viewing the report..."
if [ -f "reports/daily_status.md" ]; then
    echo "----------------------------------------"
    cat reports/daily_status.md
    echo "----------------------------------------"
else
    echo "❌ Report file not found"
    exit 1
fi

echo ""
echo "✅ Success! Your daily-python-report is ready!"
echo ""
echo "📦 Next Steps:"
echo "  1. Initialize git:"
echo "     git init"
echo "     git add ."
echo "     git commit -m 'feat: initial commit'"
echo ""
echo "  2. Create GitHub repository:"
echo "     gh repo create daily-python-report --public --source=. --push"
echo "     # Or manually create on github.com and push"
echo ""
echo "  3. Configure GitHub Actions permissions:"
echo "     - Go to Settings → Actions → General"
echo "     - Enable 'Read and write permissions'"
echo "     - Enable 'Allow GitHub Actions to create and approve pull requests'"
echo ""
echo "  4. Test the workflow:"
echo "     - Go to Actions tab"
echo "     - Click 'Daily Report Generation'"
echo "     - Click 'Run workflow'"
echo ""
echo "  5. Verify commits show verified checkmark ✅"
echo ""
echo "📖 Documentation:"
echo "  - README.md: Complete documentation"
echo "  - QUICKSTART.md: Detailed setup guide"
echo "  - STRUCTURE.md: Repository structure"
echo "  - PROJECT_SUMMARY.md: Implementation details"
echo ""
echo "Happy automating! 🎉"
