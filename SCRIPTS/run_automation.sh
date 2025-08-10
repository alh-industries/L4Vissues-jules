#!/bin/bash
set -e

echo "--- Starting Automation ---"
python3 SCRIPTS/import_issues.py
python3 SCRIPTS/manage_project.py
echo "--- Automation Finished ---"
