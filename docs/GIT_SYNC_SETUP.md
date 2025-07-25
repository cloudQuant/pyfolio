# Git Sync Setup Guide

This guide explains how to set up automatic synchronization to push your changes to both Gitee and GitHub while keeping pull operations from the original Gitee repository.

## Setup

The cloudquant remote has already been added. You can verify this by running:
```bash
git remote -v
```

You should see:
- `origin` pointing to `https://gitee.com/yunjinqi/pyfolio.git`
- `cloudquant` pointing to `https://github.com/cloudQuant/pyfolio.git`

## Usage

### Option 1: Use the sync scripts (Recommended)

#### Windows
```bash
git-push-sync.bat [branch-name]
# Examples:
git-push-sync.bat              # Push current branch to both remotes
git-push-sync.bat master       # Push master branch to both remotes
git-push-sync.bat --all        # Push all branches to both remotes
```

#### Linux/macOS
```bash
./git-push-sync.sh [branch-name]
# Examples:
./git-push-sync.sh              # Push current branch to both remotes
./git-push-sync.sh master       # Push master branch to both remotes
./git-push-sync.sh --all        # Push all branches to both remotes
```

### Option 2: Manual push to both remotes

```bash
# Push to origin (Gitee)
git push origin master

# Then push to cloudquant (GitHub)
git push cloudquant master
```

### Option 3: Use git alias (One-time setup)

Add this alias to your git config:
```bash
git config --local alias.push-all '!git push origin "$@" && git push cloudquant "$@"'
```

Then use:
```bash
git push-all master
```

## Pull Operations

Pull operations remain unchanged and will continue to fetch from the origin (Gitee):
```bash
git pull
# or
git pull origin master
```

## Notes

1. The sync scripts will push to origin first, then to cloudquant
2. If the push to origin fails, it won't attempt to push to cloudquant
3. Both remotes will receive the same commits and branches
4. Make sure you have push access to both repositories