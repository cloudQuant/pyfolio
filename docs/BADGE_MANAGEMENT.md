# Badge Management Guide

## Overview

This guide explains how to manage and troubleshoot GitHub badges in the README.md file.

## Current Badges

The README.md includes the following badges:

1. **CI Tests**: Shows the status of the main CI workflow
   - URL: `https://github.com/cloudQuant/pyfolio/actions/workflows/ci.yml/badge.svg?branch=master`
   - Links to: CI workflow runs

2. **Quick Tests**: Shows the status of quick test workflow
   - URL: `https://github.com/cloudQuant/pyfolio/actions/workflows/quick-test.yml/badge.svg?branch=master`
   - Links to: Quick test workflow runs

3. **Python Versions**: Static badge showing supported Python versions

4. **License**: Static badge showing Apache 2.0 license

## Badge URL Format

The badges use the following format:
```
https://github.com/{owner}/{repo}/actions/workflows/{workflow_file}/badge.svg?branch={branch}
```

## Common Issues and Solutions

### 1. Badge Shows "Failing" When Tests Pass

**Cause**: Badge cache hasn't been updated

**Solutions**:

1. **Automatic Refresh** (Recommended):
   - The `badge-refresh.yml` workflow runs automatically after CI completes
   - It forces cache refresh by making requests with cache-busting parameters

2. **Manual Refresh**:
   ```bash
   # Check current badge status
   python scripts/check_badge_status.py
   
   # Force refresh badges
   python scripts/check_badge_status.py refresh
   ```

3. **Browser Refresh**:
   - Hard refresh the README page (Ctrl+F5 or Cmd+Shift+R)
   - Open badge URL directly in incognito/private browsing

### 2. Badge Not Updating After Workflow Changes

**Solutions**:

1. **Check workflow file name matches badge URL**
2. **Verify branch name is correct** (master vs main)
3. **Wait for GitHub's cache to expire** (usually 5-15 minutes)

### 3. Badge Shows "Unknown" Status

**Causes**:
- Workflow file doesn't exist
- Workflow hasn't run yet
- Branch name mismatch

**Solutions**:
1. Verify workflow file exists in `.github/workflows/`
2. Trigger workflow manually
3. Check branch name in URL matches actual branch

## Badge Cache Behavior

GitHub badges are cached at multiple levels:

1. **GitHub's CDN**: 5-15 minutes
2. **Browser Cache**: Varies by browser settings
3. **Third-party CDNs**: Up to 1 hour

## Best Practices

1. **Use specific branch names** in badge URLs (e.g., `?branch=master`)
2. **Link badges to workflow pages** for better user experience
3. **Test badge URLs** after making workflow changes
4. **Monitor badge status** after CI updates

## Troubleshooting Commands

```bash
# Check if workflows exist
ls .github/workflows/

# Check recent workflow runs
gh run list --limit 5

# Manually trigger workflow
gh workflow run ci.yml

# Check badge status
python scripts/check_badge_status.py

# Force badge refresh
python scripts/check_badge_status.py refresh
```

## Advanced Badge Options

You can add additional query parameters to customize badge behavior:

- `&event=push` - Only show status for push events
- `&event=pull_request` - Only show status for PR events
- `&t=timestamp` - Cache busting parameter

Example:
```markdown
![Tests](https://github.com/cloudQuant/pyfolio/actions/workflows/ci.yml/badge.svg?branch=master&event=push)
```