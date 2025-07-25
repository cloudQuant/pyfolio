#!/usr/bin/env python3
"""
Check the status of GitHub badges and refresh them if needed
"""

import requests
import time
import sys
from urllib.parse import urlencode


def check_badge_status():
    """Check the current status of GitHub badges."""
    badges = {
        'CI Tests': 'https://github.com/cloudQuant/pyfolio/actions/workflows/ci.yml/badge.svg?branch=master',
        'Quick Tests': 'https://github.com/cloudQuant/pyfolio/actions/workflows/quick-test.yml/badge.svg?branch=master'
    }
    
    print("🔍 Checking badge status...\n")
    
    for name, url in badges.items():
        try:
            # Add cache-busting parameter
            cache_bust_url = f"{url}&t={int(time.time())}"
            response = requests.get(cache_bust_url, timeout=10)
            
            if response.status_code == 200:
                # Try to determine status from SVG content
                svg_content = response.text.lower()
                
                if 'passing' in svg_content or 'success' in svg_content:
                    status = "✅ PASSING"
                elif 'failing' in svg_content or 'failed' in svg_content:
                    status = "❌ FAILING"
                elif 'error' in svg_content:
                    status = "⚠️  ERROR"
                else:
                    status = "❓ UNKNOWN"
                
                print(f"{name}: {status}")
                
                # Show cache headers
                cache_control = response.headers.get('cache-control', 'N/A')
                last_modified = response.headers.get('last-modified', 'N/A')
                print(f"  Cache-Control: {cache_control}")
                print(f"  Last-Modified: {last_modified}")
                
            else:
                print(f"{name}: ❌ HTTP {response.status_code}")
                
        except requests.RequestException as e:
            print(f"{name}: ❌ Error - {e}")
        
        print()


def refresh_badges():
    """Force refresh GitHub badges."""
    print("🔄 Refreshing badge cache...\n")
    
    badges = [
        'https://github.com/cloudQuant/pyfolio/actions/workflows/ci.yml/badge.svg?branch=master',
        'https://github.com/cloudQuant/pyfolio/actions/workflows/quick-test.yml/badge.svg?branch=master'
    ]
    
    for badge_url in badges:
        print(f"Refreshing: {badge_url}")
        
        # Multiple refresh attempts with different strategies
        strategies = [
            # Cache busting with timestamp
            f"{badge_url}&t={int(time.time())}",
            # Different query parameter
            f"{badge_url}&refresh=1",
            # Force reload
            f"{badge_url}&reload=true"
        ]
        
        for i, url in enumerate(strategies, 1):
            try:
                headers = {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'User-Agent': f'BadgeRefresh-{i}/{time.time()}'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                print(f"  Attempt {i}: HTTP {response.status_code}")
                
                if i < len(strategies):
                    time.sleep(2)  # Wait between attempts
                    
            except requests.RequestException as e:
                print(f"  Attempt {i}: Error - {e}")
        
        print()
    
    print("✅ Badge refresh completed!")
    print("Note: It may take a few minutes for changes to be visible due to CDN caching.")


def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == 'refresh':
        refresh_badges()
    else:
        check_badge_status()
        
        print("💡 To force refresh badges, run:")
        print("   python scripts/check_badge_status.py refresh")


if __name__ == "__main__":
    main()