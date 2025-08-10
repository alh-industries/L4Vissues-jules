#!/bin/bash
set -e

echo "--- Starting Automation ---"
python3 SCRIPTS/import_issues.py
echo "--- Automation Finished ---"
