# Daily Python Report

[![Daily Report Generation](https://github.com/YOUR_USERNAME/daily-python-report/actions/workflows/daily.yml/badge.svg)](https://github.com/YOUR_USERNAME/daily-python-report/actions/workflows/daily.yml)

An automated GitHub repository that generates daily status reports with verified commits. This project demonstrates best practices for GitHub Actions automation, including idempotent operations, verified commits, and robust error handling.

## Features

- **Automated Daily Reports**: Generates comprehensive daily status reports including:
  - Repository metrics (open issues, PRs)
  - Recently merged pull requests
  - Code metrics and language breakdown
  
- **Idempotent Behavior**: Only creates PRs when actual changes occur (no duplicate PRs)

- **Verified Commits**: All commits are signed and show the green verified checkmark ✅

- **Robust Automation**: Includes retry logic, concurrency control, and comprehensive logging

- **Best Practices**: Least-privilege permissions, pinned action versions, PR-based workflow

## Repository Structure

```
daily-python-report/
├── .github/
│   └── workflows/
│       └── daily.yml           # GitHub Actions workflow
├── scripts/
│   └── generate_report.py      # Report generation script
├── tests/
│   └── test_generate_report.py # Unit tests
├── reports/
│   └── daily_status.md         # Generated report (auto-created)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## How It Works

### Automation Workflow

1. **Schedule**: Runs daily at 00:00 UTC via GitHub Actions cron schedule
2. **Manual Trigger**: Can also be triggered manually via `workflow_dispatch`
3. **Report Generation**: 
   - Collects repository metrics using GitHub CLI
   - Calculates code statistics
   - Generates a markdown report
4. **Change Detection**: Compares new report with existing one (excludes timestamps)
5. **PR Creation**: If changes detected, creates a pull request with verified commits
6. **No Changes**: If no changes, workflow completes without creating a PR

### Verified Commits Explained

All commits in this repository show the verified checkmark (✅) because:

- **GitHub Actions Bot Identity**: Uses `github-actions[bot]` as the commit author
- **Automatic Signing**: GitHub automatically signs commits from the Actions bot when using the official bot email: `41898282+github-actions[bot]@users.noreply.github.com`
- **GITHUB_TOKEN**: Uses the built-in `GITHUB_TOKEN` which provides authentication

This approach:
- ✅ Works out-of-the-box (no GPG key setup required)
- ✅ Shows verified badge on all commits
- ✅ Complies with GitHub's security best practices
- ✅ No secrets management needed

### Concurrency Control

The workflow uses concurrency groups to prevent overlapping runs:
- Only one daily report generation runs at a time
- New runs wait for existing runs to complete
- Prevents race conditions and inconsistent states

## Local Usage

### Prerequisites

- Python 3.11 or higher
- GitHub CLI (`gh`) installed and authenticated (optional, for full metrics)
- Git repository initialized

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/daily-python-report.git
cd daily-python-report
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Authenticate GitHub CLI for full metrics:
```bash
gh auth login
```

### Running the Script

Generate a report manually:

```bash
python scripts/generate_report.py
```

The report will be created/updated at `reports/daily_status.md`.

### Running Tests

Execute the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html

# Run specific test
pytest tests/test_generate_report.py::TestReportGenerator::test_run_creates_report -v
```

## Configuration

### Workflow Schedule

To change the daily run time, edit `.github/workflows/daily.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Change this to your desired schedule
```

Cron syntax: `minute hour day month day-of-week`

Examples:
- `0 0 * * *` - Daily at midnight UTC
- `0 12 * * *` - Daily at noon UTC
- `0 0 * * 1` - Weekly on Mondays at midnight UTC

### Permissions

The workflow uses minimal required permissions:

```yaml
permissions:
  contents: write      # To commit report changes
  pull-requests: write # To create PRs
  issues: read         # To read issue counts
```

### Action Versions

All actions are pinned to specific versions for security and reproducibility:
- `actions/checkout@v4.2.2`
- `actions/setup-python@v5.3.0`
- `peter-evans/create-pull-request@v7.0.5`

Update these periodically to get security fixes and new features.

## Troubleshooting

### Issue: No PR Created Despite Changes

**Symptoms**: Workflow runs successfully but no PR appears

**Solutions**:
1. Check workflow logs in Actions tab
2. Verify `steps.check_changes.outputs.changed` is `true`
3. Ensure `GITHUB_TOKEN` has sufficient permissions
4. Check branch protection rules aren't blocking PR creation

### Issue: Commits Not Showing as Verified

**Symptoms**: Commits appear but without green checkmark

**Solutions**:
1. Verify you're using the correct bot email:
   ```yaml
   committer: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
   ```
2. Ensure `GITHUB_TOKEN` is used (not a personal access token)
3. Check that organization settings don't require GPG signing

### Issue: Workflow Fails with "Resource not accessible by integration"

**Symptoms**: Workflow fails when trying to create PR

**Solutions**:
1. Check repository Settings → Actions → General
2. Ensure "Read and write permissions" is enabled for workflows
3. Verify required permissions are in workflow YAML

### Issue: GitHub CLI Commands Fail

**Symptoms**: Report shows "gh CLI not configured"

**Solutions**:
1. Verify `gh` is installed (pre-installed on `ubuntu-latest`)
2. Ensure `GH_TOKEN` environment variable is set
3. Check token has `repo` scope

### Issue: Tests Fail Locally

**Symptoms**: `pytest` command fails or tests don't run

**Solutions**:
```bash
# Install test dependencies
pip install -r requirements.txt

# Run from repository root
cd /path/to/daily-python-report
python -m pytest tests/ -v

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/scripts"
```

### Issue: Report Always Shows "No Changes"

**Symptoms**: Report generates but workflow says no changes

**Solutions**:
1. Check if report is actually changing (view diff in logs)
2. Verify `git diff` command works locally
3. Ensure report file is tracked by git
4. Check `.gitignore` isn't excluding reports directory

## Development

### Adding New Metrics

To add new metrics to the report:

1. Add data collection in `generate_report.py`:
```python
def get_new_metric(self) -> Dict[str, any]:
    # Your metric collection logic
    return {"metric_name": value}
```

2. Include in report generation:
```python
def generate_report_content(self) -> str:
    # ... existing code ...
    new_metric = self.get_new_metric()
    report += f"- New Metric: {new_metric['metric_name']}\n"
```

3. Add tests in `test_generate_report.py`:
```python
def test_new_metric(self, generator):
    metric = generator.get_new_metric()
    assert "metric_name" in metric
```

### Modifying the Workflow

When making changes to `.github/workflows/daily.yml`:

1. Test locally using [act](https://github.com/nektos/act) (GitHub Actions simulator)
2. Create a PR to test in a safe environment
3. Check workflow run summaries in GitHub Actions
4. Monitor for any failures or unexpected behavior

## Security Considerations

- **Token Permissions**: Uses least-privilege principle
- **Action Pinning**: All actions pinned to specific SHA versions
- **No Secrets**: Doesn't require custom secrets (uses built-in `GITHUB_TOKEN`)
- **Verified Commits**: All automation commits are signed and verified
- **Branch Protection**: Works with protected branches (uses PRs)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Create a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request) for the excellent PR creation action
- GitHub Actions team for the automation platform
- Python community for excellent tooling

## Support

For issues or questions:
- Open an issue in this repository
- Check the [Troubleshooting](#troubleshooting) section
- Review GitHub Actions logs for detailed error messages

---

**Note**: Remember to replace `YOUR_USERNAME` in URLs with your actual GitHub username after creating the repository.
