#!/bin/bash
# Script to check CI/CD status using GitHub CLI
# Requires GitHub CLI (gh) to be installed

echo "=== Checking CI/CD Status for pyfolio ==="
echo

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "ERROR: GitHub CLI is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Get repository info
REPO_URL=$(git remote get-url origin)
echo "Repository: $REPO_URL"
echo

# Extract owner/repo from URL
REPO="cloudQuant/pyfolio"
echo "Checking workflows for: $REPO"
echo

# List recent workflow runs
echo "=== Recent Workflow Runs ==="
gh run list --repo $REPO --limit 10

echo
echo "=== Failed Runs (Last 5) ==="
gh run list --repo $REPO --status failure --limit 5

echo
echo "=== To view details of a specific run: ==="
echo "gh run view [RUN_ID] --repo $REPO"
echo
echo "=== To view logs of a specific run: ==="
echo "gh run view [RUN_ID] --repo $REPO --log"
echo
echo "=== To download logs of a failed run: ==="
echo "gh run download [RUN_ID] --repo $REPO"
echo
echo "=== To rerun a failed workflow: ==="
echo "gh run rerun [RUN_ID] --repo $REPO"