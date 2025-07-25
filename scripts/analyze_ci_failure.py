#!/usr/bin/env python3
"""
Analyze CI workflow failure to identify the specific cause
"""

import subprocess
import json
import sys


def run_command(cmd):
    """Run shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1


def get_latest_workflow_run():
    """Get the latest workflow run information."""
    cmd = "gh run list --repo cloudQuant/pyfolio --workflow ci.yml --limit 1 --json status,conclusion,databaseId,jobs"
    stdout, stderr, code = run_command(cmd)
    
    if code != 0:
        print(f"❌ Failed to get workflow info: {stderr}")
        return None
    
    try:
        runs = json.loads(stdout)
        return runs[0] if runs else None
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse workflow data: {e}")
        return None


def analyze_workflow_run(run_id):
    """Analyze a specific workflow run."""
    print(f"🔍 Analyzing workflow run #{run_id}...\n")
    
    # Get detailed run information with jobs
    cmd = f"gh run view {run_id} --repo cloudQuant/pyfolio --json jobs,status,conclusion"
    stdout, stderr, code = run_command(cmd)
    
    if code != 0:
        print(f"❌ Failed to get run details: {stderr}")
        return
    
    try:
        run_data = json.loads(stdout)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse run data: {e}")
        return
    
    print(f"📊 Workflow Status: {run_data.get('status', 'unknown')}")
    print(f"📊 Workflow Conclusion: {run_data.get('conclusion', 'unknown')}")
    print()
    
    # Analyze each job
    jobs = run_data.get('jobs', [])
    
    # Categorize jobs
    core_jobs = []
    optional_jobs = []
    
    for job in jobs:
        job_name = job.get('name', 'Unknown')
        if any(keyword in job_name.lower() for keyword in ['test python', 'lint', 'build']):
            core_jobs.append(job)
        else:
            optional_jobs.append(job)
    
    # Analyze core jobs
    print("🔬 Core Jobs Analysis:")
    core_failed = False
    for job in core_jobs:
        name = job.get('name', 'Unknown')
        status = job.get('status', 'unknown')
        conclusion = job.get('conclusion', 'unknown')
        
        if conclusion == 'success':
            print(f"  ✅ {name}: {conclusion}")
        elif conclusion == 'failure':
            print(f"  ❌ {name}: {conclusion}")
            core_failed = True
        else:
            print(f"  ⚠️  {name}: {conclusion}")
    
    print()
    
    # Analyze optional jobs
    if optional_jobs:
        print("🔧 Optional Jobs Analysis:")
        for job in optional_jobs:
            name = job.get('name', 'Unknown')
            conclusion = job.get('conclusion', 'unknown')
            
            if conclusion == 'success':
                print(f"  ✅ {name}: {conclusion}")
            elif conclusion == 'failure':
                print(f"  ⚠️  {name}: {conclusion} (optional)")
            else:
                print(f"  ❓ {name}: {conclusion}")
    
    print()
    
    # Overall assessment
    print("🎯 Overall Assessment:")
    if not core_failed:
        print("  ✅ All core jobs passed - CI should show as SUCCESS")
        print("  💡 If badge shows failure, it may be a caching issue")
        print("  💡 Run: python scripts/check_badge_status.py refresh")
    else:
        print("  ❌ Core jobs failed - CI correctly shows as FAILURE")
        print("  🔧 Review failed job logs for specific errors")
    
    print()
    print("🔗 Useful Commands:")
    print(f"  View logs: gh run view {run_id} --repo cloudQuant/pyfolio --log")
    print(f"  Download logs: gh run download {run_id} --repo cloudQuant/pyfolio")
    print(f"  Rerun workflow: gh run rerun {run_id} --repo cloudQuant/pyfolio")


def main():
    """Main function."""
    print("🔍 CI Failure Analysis Tool\n")
    
    # Check if gh is available
    stdout, stderr, code = run_command("gh --version")
    if code != 0:
        print("❌ GitHub CLI not found. Please install from: https://cli.github.com/")
        sys.exit(1)
    
    # Get run ID from command line or use latest
    if len(sys.argv) > 1:
        run_id = sys.argv[1]
        analyze_workflow_run(run_id)
    else:
        # Get latest run
        latest_run = get_latest_workflow_run()
        if not latest_run:
            print("❌ No workflow runs found")
            sys.exit(1)
        
        run_id = latest_run.get('databaseId')
        if not run_id:
            print("❌ Could not get run ID")
            sys.exit(1)
        
        print(f"📋 Latest workflow run: #{run_id}")
        print(f"📋 Status: {latest_run.get('status', 'unknown')}")
        print(f"📋 Conclusion: {latest_run.get('conclusion', 'unknown')}")
        print()
        
        analyze_workflow_run(run_id)


if __name__ == "__main__":
    main()