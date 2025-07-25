#!/usr/bin/env python3
"""
Analyze CI/CD logs to identify common issues
Usage: python analyze_ci_logs.py <log_file>
"""

import sys
import re
from collections import defaultdict


def analyze_log(log_content):
    """Analyze log content for common CI/CD issues."""
    issues = defaultdict(list)
    lines = log_content.split('\n')
    
    # Common error patterns
    patterns = {
        'timeout': [
            r'Error: The operation was canceled',
            r'cancelled \d+ .* ago',
            r'timeout',
            r'timed out'
        ],
        'installation': [
            r'ERROR: .* is not a valid wheel filename',
            r'ModuleNotFoundError: No module named',
            r'pip install.*failed',
            r'Failed to install',
            r'ERROR: Failed to install'
        ],
        'network': [
            r'Failed to establish a new connection',
            r'Connection refused',
            r'git clone.*failed',
            r'curl:.*Failed'
        ],
        'import': [
            r'ImportError:',
            r'AttributeError:.*has no attribute',
            r'Failed to import'
        ],
        'build': [
            r'Building wheel.*failed',
            r'error: Microsoft Visual C\+\+',
            r'compilation terminated',
            r'Build failed'
        ]
    }
    
    # Search for patterns
    for i, line in enumerate(lines):
        for issue_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, line, re.IGNORECASE):
                    # Get context (5 lines before and after)
                    start = max(0, i - 5)
                    end = min(len(lines), i + 6)
                    context = lines[start:end]
                    issues[issue_type].append({
                        'line_number': i + 1,
                        'line': line.strip(),
                        'context': '\n'.join(context)
                    })
    
    return issues


def print_analysis(issues):
    """Print analysis results."""
    if not any(issues.values()):
        print("✅ No common issues detected in the log.")
        return
    
    print("🔍 CI/CD Log Analysis Results:\n")
    
    issue_descriptions = {
        'timeout': '⏱️  Timeout Issues',
        'installation': '📦 Installation Issues',
        'network': '🌐 Network Issues',
        'import': '🐍 Import Issues',
        'build': '🔨 Build Issues'
    }
    
    for issue_type, occurrences in issues.items():
        if occurrences:
            print(f"\n{issue_descriptions.get(issue_type, issue_type)}:")
            print(f"Found {len(occurrences)} occurrence(s)")
            
            for i, occurrence in enumerate(occurrences[:3]):  # Show first 3
                print(f"\n  #{i+1} Line {occurrence['line_number']}: {occurrence['line']}")
                if i == 0:  # Show context for first occurrence
                    print("\n  Context:")
                    for ctx_line in occurrence['context'].split('\n'):
                        print(f"    {ctx_line}")
            
            if len(occurrences) > 3:
                print(f"\n  ... and {len(occurrences) - 3} more occurrence(s)")


def suggest_fixes(issues):
    """Suggest fixes based on detected issues."""
    print("\n\n💡 Suggested Fixes:\n")
    
    suggestions = {
        'timeout': [
            "- Increase timeout values in workflow",
            "- Add caching for dependencies",
            "- Use parallel installation where possible",
            "- Check if the runner is overloaded"
        ],
        'installation': [
            "- Verify package compatibility with Python version",
            "- Check if all dependencies are specified",
            "- Try upgrading pip/setuptools/wheel",
            "- Use --no-deps flag and install dependencies separately"
        ],
        'network': [
            "- Add retry logic for network operations",
            "- Use mirror repositories (e.g., Gitee as fallback)",
            "- Check GitHub Actions status page",
            "- Add network connectivity tests"
        ],
        'import': [
            "- Verify package is installed correctly",
            "- Check for circular imports",
            "- Ensure all dependencies are installed",
            "- Check Python path configuration"
        ],
        'build': [
            "- Install required build tools",
            "- Check compiler compatibility",
            "- Use pre-built wheels if available",
            "- Check for missing system dependencies"
        ]
    }
    
    shown_suggestions = set()
    for issue_type in issues:
        if issues[issue_type] and issue_type in suggestions:
            if issue_type not in shown_suggestions:
                print(f"For {issue_type} issues:")
                for suggestion in suggestions[issue_type]:
                    print(f"  {suggestion}")
                print()
                shown_suggestions.add(issue_type)


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_ci_logs.py <log_file>")
        print("Or pipe logs: gh run view <RUN_ID> --log | python analyze_ci_logs.py -")
        sys.exit(1)
    
    # Read log content
    if sys.argv[1] == '-':
        log_content = sys.stdin.read()
    else:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                log_content = f.read()
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found.")
            sys.exit(1)
    
    # Analyze
    issues = analyze_log(log_content)
    print_analysis(issues)
    
    if any(issues.values()):
        suggest_fixes(issues)


if __name__ == "__main__":
    main()