#!/usr/bin/env python3
"""
Verification script to check that the repository structure is correct.
Run this to ensure all required files are present and properly configured.
"""

import os
import sys
from pathlib import Path


def check_file_exists(file_path: Path, description: str) -> bool:
    """Check if a file exists and report the result."""
    if file_path.exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (MISSING)")
        return False


def check_file_content(file_path: Path, required_strings: list, description: str) -> bool:
    """Check if a file contains required strings."""
    if not file_path.exists():
        print(f"❌ {description}: {file_path} (FILE MISSING)")
        return False
    
    try:
        content = file_path.read_text()
        missing = []
        for req_string in required_strings:
            if req_string not in content:
                missing.append(req_string)
        
        if missing:
            print(f"⚠️  {description}: Missing required content: {', '.join(missing)}")
            return False
        else:
            print(f"✅ {description}: All required content present")
            return True
    except Exception as e:
        print(f"❌ {description}: Error reading file: {e}")
        return False


def main():
    """Run all verification checks."""
    print("🔍 Verifying Daily Python Report repository structure...\n")
    
    repo_root = Path(__file__).parent
    all_checks_passed = True
    
    # Check core files
    print("📁 Core Files:")
    all_checks_passed &= check_file_exists(
        repo_root / "scripts" / "generate_report.py",
        "Report generation script"
    )
    all_checks_passed &= check_file_exists(
        repo_root / "tests" / "test_generate_report.py",
        "Test file"
    )
    all_checks_passed &= check_file_exists(
        repo_root / "requirements.txt",
        "Requirements file"
    )
    
    print("\n📁 GitHub Workflows:")
    all_checks_passed &= check_file_exists(
        repo_root / ".github" / "workflows" / "daily.yml",
        "Daily workflow"
    )
    all_checks_passed &= check_file_exists(
        repo_root / ".github" / "workflows" / "test.yml",
        "Test workflow"
    )
    
    print("\n📁 Documentation:")
    all_checks_passed &= check_file_exists(
        repo_root / "README.md",
        "README"
    )
    all_checks_passed &= check_file_exists(
        repo_root / "QUICKSTART.md",
        "Quick Start Guide"
    )
    all_checks_passed &= check_file_exists(
        repo_root / "CONTRIBUTING.md",
        "Contributing Guide"
    )
    all_checks_passed &= check_file_exists(
        repo_root / "SECURITY.md",
        "Security Policy"
    )
    all_checks_passed &= check_file_exists(
        repo_root / "CHANGELOG.md",
        "Changelog"
    )
    
    print("\n📁 Configuration:")
    all_checks_passed &= check_file_exists(
        repo_root / ".gitignore",
        ".gitignore"
    )
    all_checks_passed &= check_file_exists(
        repo_root / "pytest.ini",
        "pytest configuration"
    )
    all_checks_passed &= check_file_exists(
        repo_root / "LICENSE",
        "License file"
    )
    
    # Check workflow content
    print("\n🔍 Workflow Content Checks:")
    all_checks_passed &= check_file_content(
        repo_root / ".github" / "workflows" / "daily.yml",
        [
            "peter-evans/create-pull-request@v7.0.5",
            "github-actions[bot]",
            "concurrency:",
            "GITHUB_STEP_SUMMARY"
        ],
        "Daily workflow configuration"
    )
    
    # Check script content
    print("\n🔍 Script Content Checks:")
    all_checks_passed &= check_file_content(
        repo_root / "scripts" / "generate_report.py",
        [
            "class ReportGenerator",
            "def should_update_report",
            "def calculate_content_hash",
            "idempotent"
        ],
        "Report generator implementation"
    )
    
    # Check README content
    print("\n🔍 Documentation Content Checks:")
    all_checks_passed &= check_file_content(
        repo_root / "README.md",
        [
            "Verified Commits",
            "Idempotent",
            "Troubleshooting",
            "peter-evans/create-pull-request"
        ],
        "README documentation"
    )
    
    # Check directory structure
    print("\n📂 Directory Structure:")
    required_dirs = [
        repo_root / "scripts",
        repo_root / "tests",
        repo_root / "reports",
        repo_root / ".github" / "workflows",
    ]
    
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Directory missing: {dir_path}")
            all_checks_passed = False
    
    # Final summary
    print("\n" + "="*60)
    if all_checks_passed:
        print("✅ All checks passed! Repository is properly configured.")
        print("\nNext steps:")
        print("  1. Review README.md for setup instructions")
        print("  2. Run: python scripts/generate_report.py")
        print("  3. Run: pytest tests/ -v")
        print("  4. Push to GitHub and configure Actions permissions")
        return 0
    else:
        print("❌ Some checks failed. Please review the output above.")
        print("\nCommon fixes:")
        print("  - Ensure all files were copied correctly")
        print("  - Check file permissions")
        print("  - Verify directory structure")
        return 1


if __name__ == "__main__":
    sys.exit(main())
