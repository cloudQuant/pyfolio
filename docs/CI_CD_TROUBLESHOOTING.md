# CI/CD Troubleshooting Guide

## Overview

This guide helps troubleshoot CI/CD issues in the pyfolio project.

## Common Issues and Solutions

### 1. Installation Timeouts

**Symptoms:**
- Jobs cancelled after 20-30 minutes
- Stuck during empyrical or pyfolio installation

**Solutions:**
- Timeout has been increased to 30 minutes
- Retry logic added for network operations
- Use fallback URLs (GitHub → Gitee)

### 2. macOS Font Cache Issues

**Symptoms:**
- Matplotlib font_manager errors
- Timeout during font cache building

**Solutions:**
- Font cache building is now non-critical (`continue-on-error: true`)
- Uses Agg backend to avoid GUI issues

### 3. Windows Wildcard Issues

**Symptoms:**
- "*.whl is not a valid wheel filename" error

**Solutions:**
- All scripts now use `shell: bash` for consistent behavior
- Explicit file detection before installation

## Debugging Tools

### 1. Debug Workflow

Run the debug workflow manually to investigate specific issues:

1. Go to Actions → Debug CI Issues
2. Click "Run workflow"
3. Select OS and Python version
4. Review detailed logs

### 2. Enhanced Logging

The main CI now includes:
- System information output
- Network connectivity tests
- Detailed error messages
- Package installation verification
- Retry attempts with wait times

### 3. Error Recovery

The workflow includes:
- Automatic retries for network operations
- Fallback URLs for dependencies
- Non-critical operations marked with `continue-on-error`
- Explicit error messages with context

## Manual Debugging Steps

If CI continues to fail:

1. **Check Recent Changes**
   ```bash
   git log --oneline -n 10
   ```

2. **Test Locally**
   ```bash
   # Create clean environment
   python -m venv test_env
   source test_env/bin/activate  # or test_env\Scripts\activate on Windows
   
   # Install dependencies
   pip install --upgrade pip wheel setuptools
   pip install ipython>=7.0.0
   pip install git+https://github.com/cloudQuant/empyrical.git
   
   # Build and install
   python -m build
   pip install dist/*.whl
   
   # Test
   python -c "import pyfolio; print(pyfolio.__version__)"
   ```

3. **Check GitHub Status**
   - Visit https://www.githubstatus.com/
   - Check for ongoing incidents

4. **Review Workflow Logs**
   - Click on failed job
   - Expand each step
   - Look for "ERROR:" prefixed messages

## CI Status Analysis

Use our specialized tool to analyze CI failures:

```bash
# Analyze latest workflow run
python scripts/analyze_ci_failure.py

# Analyze specific run
python scripts/analyze_ci_failure.py [RUN_ID]
```

This tool will:
- Distinguish between core jobs (test, lint, build) and optional jobs
- Explain why CI shows as failed even when tests pass
- Provide specific remediation steps

## Core vs Optional Jobs

**Core Jobs** (determine CI status):
- `test`: Main test suite across all Python versions and OS
- `lint`: Code quality checks  
- `build`: Package building

**Optional Jobs** (don't affect CI status):
- `test-install`: Installation testing (marked as `continue-on-error`)

The CI badge will show "passing" if all core jobs pass, even if optional jobs fail.

## Reporting Issues

When reporting CI/CD issues:

1. Run `python scripts/analyze_ci_failure.py` first
2. Include the exact error message
3. Specify OS and Python version
4. Link to the failed workflow run
5. Note any recent changes to dependencies