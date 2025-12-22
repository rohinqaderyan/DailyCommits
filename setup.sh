#!/bin/bash
# Setup script for local development

set -e

echo "🚀 Setting up Daily Python Report development environment..."

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Using Python $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create reports directory if it doesn't exist
mkdir -p reports

# Run tests to verify setup
echo "Running tests to verify setup..."
pytest tests/ -v

# Generate initial report
echo "Generating initial report..."
python scripts/generate_report.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run tests: pytest tests/ -v"
echo "  3. Generate report: python scripts/generate_report.py"
echo "  4. View report: cat reports/daily_status.md"
echo ""
echo "Happy coding! 🎉"
