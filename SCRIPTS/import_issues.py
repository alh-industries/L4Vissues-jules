import pandas as pd
import os
import re

def get_tsv_file():
    """
    Finds the first TSV file in the TSV_HERE directory.
    """
    for file in os.listdir('TSV_HERE'):
        if file.endswith('.tsv'):
            return os.path.join('TSV_HERE', file)
    return None

def main():
    """
    Main function to run the issue import process.
    """
    print("--- Starting import_issues.py ---")

    tsv_file = get_tsv_file()
    if not tsv_file:
        print("No TSV file found in TSV_HERE directory.")
        return

    df = pd.read_csv(tsv_file, sep='\\t', engine='python')
    print(f"Successfully loaded {tsv_file} with {len(df)} rows.")

    issue_title_to_number = {}

    sync_labels(df)
    create_issues(df, issue_title_to_number)
    create_child_issues(df, issue_title_to_number)
    manage_project(df, issue_title_to_number)

    print("\\n--- import_issues.py finished ---")

def get_existing_labels():
    """
    Gets the existing labels in the repository.
    """
    print("Getting existing labels...")
    existing_labels = os.popen('gh label list --json name --jq ".[].name"').read().splitlines()
    return existing_labels

def sync_labels(df):
    """
    Syncs labels from the TSV file with the repository.
    """
    print("Syncing labels...")
    label_columns = [col for col in df.columns if col.startswith('ISSUE_LABEL')]
    all_labels = set()
    for col in label_columns:
        labels = df[col].dropna().unique()
        for label in labels:
            all_labels.add(label)

    existing_labels = get_existing_labels()
    new_labels = all_labels - set(existing_labels)

    print("Creating new labels...")
    for label in new_labels:
        escaped_label = label.replace("'", "'\\''")
        print(f"Creating label: {label}")
        os.system(f"gh label create '{escaped_label}' --color 'f29513'")

    print("Label sync complete.")

def create_issues(df, issue_title_to_number):
    """
    Creates issues from the TSV file.
    """
    print("\\nCreating issues...")
    for index, row in df.iterrows():
        title = row['ISSUE_TITLE']
        body = row['ISSUE_BODY']

        title = '' if pd.isna(title) else title
        body = '' if pd.isna(body) else body

        labels = []
        for col in [f'ISSUE_LABEL_{i}' for i in range(6)]:
            if col in row and pd.notna(row[col]):
                labels.append(row[col])

        escaped_title = title.replace("'", "'\\''")
        escaped_body = body.replace("'", "'\\''")

        label_flags = ",".join([f"'{label.replace('\'', '\'\\\'\'')}'" for label in labels])

        cmd = f"gh issue create --title '{escaped_title}' --body '{escaped_body}'"
        if label_flags:
            cmd += f" --label {label_flags}"

        print(f"Creating issue: {title}")
        issue_url = os.popen(cmd).read().strip()

        if issue_url:
            match = re.search(r'(\d+)$', issue_url)
            if match:
                issue_number = int(match.group(1))
                issue_title_to_number[title] = issue_number
                print(f"Successfully created issue #{issue_number} for '{title}'")
            else:
                print(f"Could not extract issue number from URL: {issue_url}")
        else:
            print(f"Failed to create issue for '{title}'")

    print("Issue creation complete.")

def create_child_issues(df, issue_title_to_number):
    """
    Creates child issues from the ISSUE_BODY of the parent issues.
    """
    print("\\nCreating child issues...")
    for index, row in df.iterrows():
        parent_issue_title = row['ISSUE_TITLE']
        body = row['ISSUE_BODY']

        parent_issue_title = '' if pd.isna(parent_issue_title) else parent_issue_title
        body = '' if pd.isna(body) else body

        sub_issues = [s.strip() for s in body.split(';') if s.strip()]

        if not sub_issues:
            continue

        parent_issue_number = issue_title_to_number.get(parent_issue_title)
        if not parent_issue_number:
            print(f"Could not find parent issue number for '{parent_issue_title}'. Skipping child issue creation.")
            continue

        print(f"\\n# Parent Issue: {parent_issue_title} (#{parent_issue_number})")

        child_issue_numbers = []
        for sub_issue_title in sub_issues:
            escaped_sub_issue_title = sub_issue_title.replace("'", "'\\''")
            cmd = f"gh issue create --title '{escaped_sub_issue_title}' --body ''"
            print(f"Creating child issue: {sub_issue_title}")
            child_issue_url = os.popen(cmd).read().strip()

            if child_issue_url:
                match = re.search(r'(\d+)$', child_issue_url)
                if match:
                    child_issue_number = int(match.group(1))
                    child_issue_numbers.append(child_issue_number)
                    print(f"Successfully created child issue #{child_issue_number}")
                else:
                    print(f"Could not extract issue number from URL: {child_issue_url}")
            else:
                print(f"Failed to create child issue for '{sub_issue_title}'")

        if child_issue_numbers:
            task_list = "\\n".join([f"- [ ] #{number}" for number in child_issue_numbers])
            escaped_task_list = task_list.replace("'", "'\\''")
            print(f"Updating parent issue #{parent_issue_number} with task list.")
            os.system(f"gh issue edit {parent_issue_number} --body '{escaped_task_list}'")

    print("\\nChild issue creation complete.")

def manage_project(df, issue_title_to_number):
    """
    Manages the GitHub project.
    """
    project_name = df['PROJECT'].dropna().unique()[0]
    print(f"\\n--- Managing Project: {project_name} ---")

    # Create project and get its number
    print(f"Creating project: {project_name}")
    project_url = os.popen(f"gh project create '{project_name}' --owner '@me'").read().strip()
    project_number = None
    if project_url:
        match = re.search(r'/(\d+)$', project_url)
        if match:
            project_number = int(match.group(1))
            print(f"Successfully created project #{project_number}")
        else:
            print(f"Could not extract project number from URL: {project_url}")
            return
    else:
        print(f"Failed to create project '{project_name}'")
        return

    # Add issues to project
    print("\\nAdding issues to project...")
    item_id_to_issue_number = {}
    for title, issue_number in issue_title_to_number.items():
        print(f"Adding issue #{issue_number} to project #{project_number}")
        item_id = os.popen(f"gh project item-add {project_number} --issue {issue_number}").read().strip()
        if item_id:
            item_id_to_issue_number[item_id] = issue_number
            print(f"Successfully added issue #{issue_number} as item {item_id}")
        else:
            print(f"Failed to add issue #{issue_number} to project")

    # Update project fields
    print("\\nUpdating project fields...")
    project_fields = [col for col in df.columns if col.startswith('PROJECT_FIELD_')]
    for item_id, issue_number in item_id_to_issue_number.items():
        row = df[df['ISSUE_TITLE'] == list(issue_title_to_number.keys())[list(issue_title_to_number.values()).index(issue_number)]].iloc[0]
        for field_col in project_fields:
            if pd.notna(row[field_col]):
                field_name = field_col.split(':')[0].replace('PROJECT_FIELD_', '')
                field_value = row[field_col]
                print(f"Updating field '{field_name}' for item {item_id} (issue #{issue_number}) to '{field_value}'")
                os.system(f"gh project item-edit --item-id {item_id} --field-name '{field_name}' --text '{field_value}'")

    print("\\n--- Project management finished ---")

if __name__ == "__main__":
    main()
