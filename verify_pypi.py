#!/usr/bin/env python
"""Verify package on PyPI."""

import urllib.request
import json

try:
    response = urllib.request.urlopen('https://pypi.org/pypi/analystx/json')
    data = json.loads(response.read())
    info = data['info']
    
    print("=" * 60)
    print("✓ ANALYSTX PUBLISHED ON PYPI")
    print("=" * 60)
    print(f"Package Name: {info['name']}")
    print(f"Current Version: {info['version']}")
    print(f"Author: {info['author']}")
    print(f"Summary: {info['summary']}")
    print(f"License: {info['license']}")
    print(f"Home Page: {info['home_page']}")
    print(f"Project URLs: {info['project_urls']}")
    print("=" * 60)
    print("\nInstallation:")
    print("  pip install analystx==0.1.1")
    print("\nPyPI Page:")
    print("  https://pypi.org/project/analystx/")
    print("=" * 60)
    
except Exception as e:
    print(f"Error: {str(e)}")
