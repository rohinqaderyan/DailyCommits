# Security Policy

## Supported Versions

This project is currently in active development. Security updates are provided for the latest version only.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. **Do NOT** open a public issue
2. Email the maintainers directly (or use GitHub Security Advisories)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a timeline for a fix.

## Security Best Practices

This project follows these security practices:

- **Minimal Permissions**: Workflow uses least-privilege access
- **Pinned Actions**: All GitHub Actions are pinned to specific versions
- **No Secrets Required**: Uses built-in GITHUB_TOKEN only
- **Verified Commits**: All automated commits are signed and verified
- **Dependency Management**: Regular updates to dependencies
- **Code Review**: All changes reviewed before merge

## Known Security Considerations

### GitHub Token

- The workflow uses `GITHUB_TOKEN` which is automatically provided
- Token has minimal required permissions (contents: write, pull-requests: write, issues: read)
- Token is short-lived and scoped to the workflow run

### Third-Party Actions

We use these vetted third-party actions:
- `peter-evans/create-pull-request@v7.0.5` - Well-maintained, widely used action
- All actions are pinned to specific SHA for reproducibility

### Python Dependencies

- Minimal dependencies (pytest only for development)
- Core script uses Python stdlib only
- Regular updates via Dependabot (when enabled)

## Updates and Patches

Security patches will be released as soon as possible after discovery. Users should:
- Watch the repository for security advisories
- Update to the latest version regularly
- Review changelogs for security-related updates
