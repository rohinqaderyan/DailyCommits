"""
Unit tests for the daily report generator.
"""

import os
import tempfile
from pathlib import Path
import pytest

# Add parent directory to path to import the script
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_report import ReportGenerator


class TestReportGenerator:
    """Test cases for ReportGenerator class."""

    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Create a temporary repository structure for testing."""
        # Create some test files
        (tmp_path / "test.py").write_text("print('hello')\n")
        (tmp_path / "config.yml").write_text("key: value\n")
        (tmp_path / "README.md").write_text("# Test\n")
        return tmp_path

    @pytest.fixture
    def generator(self, temp_repo):
        """Create a ReportGenerator instance for testing."""
        return ReportGenerator(repo_path=str(temp_repo))

    def test_initialization(self, generator, temp_repo):
        """Test that generator initializes correctly."""
        assert generator.repo_path == temp_repo
        assert generator.reports_dir == temp_repo / "reports"
        assert generator.report_file == temp_repo / "reports" / "daily_status.md"

    def test_get_code_metrics(self, generator):
        """Test code metrics calculation."""
        metrics = generator.get_code_metrics()

        assert isinstance(metrics, dict)
        assert "total_files" in metrics
        assert "python_files" in metrics
        assert "yaml_files" in metrics
        assert "markdown_files" in metrics
        assert "total_lines" in metrics

        # Check that it found our test files
        assert metrics["total_files"] >= 3
        assert metrics["python_files"] >= 1
        assert metrics["yaml_files"] >= 1
        assert metrics["markdown_files"] >= 1

    def test_get_github_data(self, generator):
        """Test GitHub data fetching (will use fallback data in tests)."""
        github_data = generator.get_github_data()

        assert isinstance(github_data, dict)
        assert "open_issues" in github_data
        assert "open_prs" in github_data
        assert "recent_merged_prs" in github_data

        assert isinstance(github_data["open_issues"], int)
        assert isinstance(github_data["open_prs"], int)
        assert isinstance(github_data["recent_merged_prs"], list)

    def test_generate_report_content(self, generator):
        """Test report content generation."""
        content = generator.generate_report_content()

        assert isinstance(content, str)
        assert len(content) > 0

        # Check for expected sections
        assert "# Daily Status Report" in content
        assert "Repository Metrics" in content
        assert "GitHub Activity" in content
        assert "Code Metrics" in content
        assert "Language Breakdown" in content

        # Check for metrics
        assert "Open Issues:" in content
        assert "Open Pull Requests:" in content
        assert "Total Files:" in content

    def test_calculate_content_hash(self, generator):
        """Test content hash calculation."""
        content1 = "test content"
        content2 = "test content"
        content3 = "different content"

        hash1 = generator.calculate_content_hash(content1)
        hash2 = generator.calculate_content_hash(content2)
        hash3 = generator.calculate_content_hash(content3)

        assert hash1 == hash2
        assert hash1 != hash3
        assert len(hash1) == 64  # SHA256 produces 64 character hex string

    def test_should_update_report_no_existing_file(self, generator):
        """Test that should_update_report returns True when no file exists."""
        new_content = "test content"
        assert generator.should_update_report(new_content) is True

    def test_should_update_report_same_content(self, generator):
        """Test that should_update_report returns False for identical content."""
        content = generator.generate_report_content()
        generator.write_report(content)

        # Should not update if content is the same (excluding timestamp)
        assert generator.should_update_report(content) is False

    def test_should_update_report_different_content(self, generator, temp_repo):
        """Test that should_update_report returns True for different content."""
        initial_content = "# Initial Report\n\nOld data"
        generator.write_report(initial_content)

        new_content = "# Initial Report\n\nNew data"
        assert generator.should_update_report(new_content) is True

    def test_write_report(self, generator):
        """Test report writing."""
        content = "# Test Report\n\nTest content"
        generator.write_report(content)

        assert generator.report_file.exists()
        assert generator.report_file.read_text() == content

    def test_write_report_creates_directory(self, generator):
        """Test that write_report creates the reports directory if needed."""
        assert not generator.reports_dir.exists()

        content = "# Test Report"
        generator.write_report(content)

        assert generator.reports_dir.exists()
        assert generator.report_file.exists()

    def test_run_creates_report(self, generator):
        """Test full report generation run."""
        result = generator.run()

        assert generator.report_file.exists()
        assert result is True  # Should return True for first run

    def test_run_idempotent_behavior(self, tmp_path):
        """Test that running twice without changes doesn't update."""
        # Create a fresh temporary directory with no file changes between runs
        test_repo = tmp_path / "stable_repo"
        test_repo.mkdir()
        
        # Create some static test files
        (test_repo / "test.py").write_text("# Static content\n")
        (test_repo / "README.md").write_text("# Test\n")
        
        generator = ReportGenerator(repo_path=str(test_repo))
        
        # First run
        result1 = generator.run()
        assert result1 is True
        
        # Capture the report content (excluding timestamp)
        report1 = generator.report_file.read_text()
        lines1 = [l for l in report1.split("\n") if not l.startswith("**Generated:**")]

        # Second run - filesystem unchanged
        result2 = generator.run()
        
        # Capture second report
        report2 = generator.report_file.read_text()
        lines2 = [l for l in report2.split("\n") if not l.startswith("**Generated:**")]
        
        # Content excluding timestamp should be identical
        assert lines1 == lines2
        
        # Second run should return False (no update needed)
        assert result2 is False

    def test_report_format_is_valid_markdown(self, generator):
        """Test that generated report is valid markdown."""
        content = generator.generate_report_content()

        # Basic markdown checks
        assert content.startswith("# ")
        assert "##" in content
        assert "**" in content
        assert "-" in content  # List items

    def test_metrics_are_non_negative(self, generator):
        """Test that all metrics are non-negative."""
        metrics = generator.get_code_metrics()

        for key, value in metrics.items():
            assert value >= 0, f"{key} should be non-negative"

    def test_github_data_structure(self, generator):
        """Test GitHub data has correct structure."""
        github_data = generator.get_github_data()

        assert github_data["open_issues"] >= 0
        assert github_data["open_prs"] >= 0
        assert len(github_data["recent_merged_prs"]) >= 0


class TestReportGeneratorEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_repository(self, tmp_path):
        """Test handling of empty repository."""
        generator = ReportGenerator(repo_path=str(tmp_path))
        metrics = generator.get_code_metrics()

        assert metrics["total_files"] == 0
        assert metrics["python_files"] == 0

    def test_repository_with_special_characters(self, tmp_path):
        """Test handling of files with special characters."""
        # Create file with special characters
        special_file = tmp_path / "file with spaces.py"
        special_file.write_text("# Test\n")

        generator = ReportGenerator(repo_path=str(tmp_path))
        metrics = generator.get_code_metrics()

        assert metrics["python_files"] >= 1

    def test_large_file_handling(self, tmp_path):
        """Test handling of large files."""
        large_file = tmp_path / "large.py"
        large_file.write_text("# Comment\n" * 10000)

        generator = ReportGenerator(repo_path=str(tmp_path))
        metrics = generator.get_code_metrics()

        assert metrics["total_lines"] >= 10000
