#!/usr/bin/env python3
"""
Diagnose and potentially fix workflow status issues
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


def get_workflow_status():
    """Get detailed workflow status."""
    print("🔍 Analyzing current workflow status...\n")
    
    # Get latest CI run
    cmd = "gh run list --repo cloudQuant/pyfolio --workflow ci.yml --limit 1 --json databaseId,status,conclusion,jobs"
    stdout, stderr, code = run_command(cmd)
    
    if code != 0:
        print(f"❌ Failed to get workflow info: {stderr}")
        return False
    
    try:
        runs = json.loads(stdout)
        if not runs:
            print("❌ No workflow runs found")
            return False
        
        run = runs[0]
        run_id = run.get('databaseId')
        
        print(f"📊 Latest Run ID: {run_id}")
        print(f"📊 Status: {run.get('status')}")
        print(f"📊 Conclusion: {run.get('conclusion')}")
        print()
        
        # Get detailed job information
        cmd = f"gh run view {run_id} --repo cloudQuant/pyfolio --json jobs"
        stdout, stderr, code = run_command(cmd)
        
        if code != 0:
            print(f"❌ Failed to get job details: {stderr}")
            return False
        
        run_details = json.loads(stdout)
        jobs = run_details.get('jobs', [])
        
        print("📋 Job Status Summary:")
        all_core_passed = True
        
        for job in jobs:
            name = job.get('name', 'Unknown')
            conclusion = job.get('conclusion', 'unknown')
            
            # Identify core jobs
            is_core = any(keyword in name.lower() for keyword in 
                         ['test python', 'lint', 'build distribution'])
            
            if is_core:
                status_icon = "✅" if conclusion == "success" else "❌"
                print(f"  {status_icon} {name}: {conclusion} (CORE)")
                if conclusion != "success":
                    all_core_passed = False
            else:
                status_icon = "✅" if conclusion == "success" else "⚠️"
                optional_tag = " (OPTIONAL)" if "install" in name.lower() else ""
                print(f"  {status_icon} {name}: {conclusion}{optional_tag}")
        
        print()
        
        # Analysis
        if all_core_passed and run.get('conclusion') == 'failure':
            print("⚠️  ISSUE DETECTED:")
            print("   All core jobs passed but workflow shows as failed")
            print("   This suggests a workflow configuration issue")
            return False
        elif all_core_passed:
            print("✅ ANALYSIS:")
            print("   All core jobs passed - workflow should show success")
            return True
        else:
            print("❌ ANALYSIS:")
            print("   Core jobs failed - workflow correctly shows failure")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse workflow data: {e}")
        return False


def suggest_fixes():
    """Suggest potential fixes."""
    print("\n💡 Suggested Actions:")
    print()
    print("1. **Immediate fixes:**")
    print("   - Check if any hidden jobs are failing")
    print("   - Verify no syntax errors in workflow YAML")
    print("   - Ensure no required status checks are blocking")
    print()
    print("2. **Diagnostic commands:**")
    print("   - gh run list --repo cloudQuant/pyfolio --workflow ci.yml --limit 5")
    print("   - gh run view [RUN_ID] --repo cloudQuant/pyfolio --log")
    print()
    print("3. **Potential solutions:**")
    print("   - Remove problematic continue-on-error jobs")
    print("   - Simplify workflow to only essential jobs")
    print("   - Check for GitHub Actions service issues")
    print()
    print("4. **Reset options:**")
    print("   - Create a simple test workflow to isolate issues")
    print("   - Temporarily disable non-essential jobs")


def main():
    """Main function."""
    print("🔧 Workflow Status Diagnostic Tool\n")
    
    # Check if gh is available
    stdout, stderr, code = run_command("gh --version")
    if code != 0:
        print("❌ GitHub CLI not found. Please install from: https://cli.github.com/")
        sys.exit(1)
    
    # Analyze current status
    status_ok = get_workflow_status()
    
    if not status_ok:
        suggest_fixes()
    else:
        print("✅ Workflow status appears correct")
        print("\nIf badge still shows failure:")
        print("  python scripts/check_badge_status.py refresh")


if __name__ == "__main__":
    main()