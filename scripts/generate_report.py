#!/usr/bin/env python3
"""
Daily Report Generator

Generates a deterministic daily report with repository metrics.
Only updates the report file if content changes (idempotent behavior).
"""

import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import json


class ReportGenerator:
    """Generates daily status reports for the repository."""

    def __init__(self, repo_path: str = "."):
        """
        Initialize the report generator.
        
        Args:
            repo_path: Path to the repository root
        """
        self.repo_path = Path(repo_path).resolve()
        self.reports_dir = self.repo_path / "reports"
        self.report_file = self.reports_dir / "daily_status.md"

    def get_code_metrics(self) -> Dict[str, any]:
        """
        Calculate basic code metrics for the repository.
        
        Returns:
            Dictionary containing file counts and language breakdown
        """
        metrics = {
            "total_files": 0,
            "python_files": 0,
            "yaml_files": 0,
            "markdown_files": 0,
            "total_lines": 0,
        }

        # Exclude common directories
        exclude_dirs = {".git", "venv", "__pycache__", ".pytest_cache", "node_modules", "reports"}

        for root, dirs, files in os.walk(self.repo_path):
            # Remove excluded directories from traversal
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                metrics["total_files"] += 1
                file_path = Path(root) / file

                if file.endswith(".py"):
                    metrics["python_files"] += 1
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            metrics["total_lines"] += len(f.readlines())
                    except Exception:
                        pass
                elif file.endswith((".yml", ".yaml")):
                    metrics["yaml_files"] += 1
                elif file.endswith(".md"):
                    metrics["markdown_files"] += 1

        return metrics

    def get_github_data(self) -> Dict[str, any]:
        """
        Fetch GitHub repository data using GitHub CLI if available.
        Falls back to placeholder data if gh CLI is not available.
        
        Returns:
            Dictionary containing GitHub metrics
        """
        github_data = {
            "open_issues": 0,
            "open_prs": 0,
            "recent_merged_prs": [],
        }

        try:
            # Check if gh CLI is available
            subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                check=True,
                timeout=5
            )

            # Get open issues count
            result = subprocess.run(
                ["gh", "issue", "list", "--state", "open", "--json", "number"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                issues = json.loads(result.stdout)
                github_data["open_issues"] = len(issues)

            # Get open PRs count
            result = subprocess.run(
                ["gh", "pr", "list", "--state", "open", "--json", "number"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                prs = json.loads(result.stdout)
                github_data["open_prs"] = len(prs)

            # Get last 10 merged PRs
            result = subprocess.run(
                ["gh", "pr", "list", "--state", "merged", "--limit", "10", "--json", "title,number"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                merged_prs = json.loads(result.stdout)
                github_data["recent_merged_prs"] = [
                    f"#{pr['number']}: {pr['title']}" for pr in merged_prs
                ]

        except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
            # gh CLI not available or error occurred - use placeholder data
            github_data["recent_merged_prs"] = ["No merged PRs available (gh CLI not configured)"]

        return github_data

    def generate_report_content(self) -> str:
        """
        Generate the report content.
        
        Returns:
            String containing the formatted report
        """
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        github_data = self.get_github_data()
        code_metrics = self.get_code_metrics()

        report = f"""# Daily Status Report

**Generated:** {current_date}

## Repository Metrics

### GitHub Activity
- **Open Issues:** {github_data['open_issues']}
- **Open Pull Requests:** {github_data['open_prs']}

### Recently Merged Pull Requests (Last 10)
"""

        if github_data['recent_merged_prs']:
            for pr in github_data['recent_merged_prs']:
                report += f"- {pr}\n"
        else:
            report += "- No recently merged pull requests\n"

        report += f"""
## Code Metrics

- **Total Files:** {code_metrics['total_files']}
- **Python Files:** {code_metrics['python_files']}
- **YAML Files:** {code_metrics['yaml_files']}
- **Markdown Files:** {code_metrics['markdown_files']}
- **Total Lines of Python Code:** {code_metrics['total_lines']}

### Language Breakdown
"""

        total = code_metrics['total_files']
        if total > 0:
            python_pct = (code_metrics['python_files'] / total) * 100
            yaml_pct = (code_metrics['yaml_files'] / total) * 100
            markdown_pct = (code_metrics['markdown_files'] / total) * 100
            other_pct = 100 - python_pct - yaml_pct - markdown_pct

            report += f"- Python: {python_pct:.1f}%\n"
            report += f"- YAML: {yaml_pct:.1f}%\n"
            report += f"- Markdown: {markdown_pct:.1f}%\n"
            report += f"- Other: {other_pct:.1f}%\n"

        report += """
---
*This report is automatically generated daily by the GitHub Actions workflow.*
"""

        return report

    def calculate_content_hash(self, content: str) -> str:
        """
        Calculate SHA256 hash of content.
        
        Args:
            content: String content to hash
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def should_update_report(self, new_content: str) -> bool:
        """
        Check if report needs updating by comparing content hashes.
        
        Args:
            new_content: New report content to compare
            
        Returns:
            True if report should be updated, False otherwise
        """
        if not self.report_file.exists():
            return True

        try:
            with open(self.report_file, "r", encoding="utf-8") as f:
                existing_content = f.read()

            # Compare hashes excluding timestamp line
            existing_lines = [
                line for line in existing_content.split("\n")
                if not line.startswith("**Generated:**")
            ]
            new_lines = [
                line for line in new_content.split("\n")
                if not line.startswith("**Generated:**")
            ]

            existing_hash = self.calculate_content_hash("\n".join(existing_lines))
            new_hash = self.calculate_content_hash("\n".join(new_lines))

            return existing_hash != new_hash

        except Exception as e:
            print(f"Error reading existing report: {e}", file=sys.stderr)
            return True

    def write_report(self, content: str) -> None:
        """
        Write report content to file.
        
        Args:
            content: Report content to write
        """
        # Ensure reports directory exists
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        with open(self.report_file, "w", encoding="utf-8") as f:
            f.write(content)

    def run(self) -> bool:
        """
        Run the report generation process.
        
        Returns:
            True if report was updated, False if no changes were needed
        """
        print("Generating daily status report...")

        # Generate new report content
        new_content = self.generate_report_content()

        # Check if update is needed (idempotent behavior)
        if not self.should_update_report(new_content):
            print("No changes detected. Report is up to date.")
            return False

        # Write the report
        self.write_report(new_content)
        print(f"Report generated successfully: {self.report_file}")
        return True


def main():
    """Main entry point for the script."""
    repo_path = os.getenv("GITHUB_WORKSPACE", ".")

    try:
        generator = ReportGenerator(repo_path)
        updated = generator.run()

        # Exit with code 0 (success) regardless of whether report was updated
        # The workflow will check git diff to determine if changes occurred
        sys.exit(0)

    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
