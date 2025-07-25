#!/bin/bash
# Shell script to push to both origin and cloudquant remotes

echo "Pushing to origin (Gitee)..."
git push origin "$@"

if [ $? -eq 0 ]; then
    echo ""
    echo "Syncing to cloudquant (GitHub)..."
    git push cloudquant "$@"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "Successfully pushed to both remotes!"
    else
        echo ""
        echo "Failed to push to cloudquant remote"
        exit 1
    fi
else
    echo ""
    echo "Failed to push to origin"
    exit 1
fi