import pandas as pd
import os

def get_tsv_file():
    """
    Finds the first TSV file in the TSV_HERE directory.
    """
    for file in os.listdir('TSV_HERE'): # Corrected path
        if file.endswith('.tsv'):
            return os.path.join('TSV_HERE', file) # Corrected path
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

    sync_labels(df)
    create_issues(df)
    create_child_issues(df)

    print("\\n--- import_issues.py finished ---")

def create_child_issues(df):
    """
    Creates child issues from the ISSUE_BODY of the parent issues.
    """
    print("\\nCreating child issues...")
    print("The following gh issue create and gh issue edit commands would be executed:")
    for index, row in df.iterrows():
        parent_issue_title = row['ISSUE_TITLE']
        body = row['ISSUE_BODY']

        # Handle NaN values
        parent_issue_title = '' if pd.isna(parent_issue_title) else parent_issue_title
        body = '' if pd.isna(body) else body

        sub_issues = [s.strip() for s in body.split(';') if s.strip()]

        if not sub_issues:
            continue

        print(f"\\n# Parent Issue: {parent_issue_title}")

        # Create child issues
        for sub_issue_title in sub_issues:
            escaped_sub_issue_title = sub_issue_title.replace("'", "'\\''")
            print(f"gh issue create --title '{escaped_sub_issue_title}' --body ''")

        # Update parent issue with task list
        task_list = "\\n".join([f"- [ ] #{index+2} # Placeholder for child issue number" for index, sub_issue in enumerate(sub_issues)])

        escaped_parent_title = parent_issue_title.replace("'", "'\\''")
        escaped_task_list = task_list.replace("'", "'\\''")

        print(f"gh issue edit \"{escaped_parent_title}\" --body '{escaped_task_list}'")

    print("\\nChild issue creation complete.")

    print("\\n--- Would now call manage_project.py to handle project creation and management ---")

def create_issues(df):
    """
    Creates issues from the TSV file.
    """
    print("\\nCreating issues...")
    print("The following gh issue create commands would be executed:")
    for index, row in df.iterrows():
        title = row['ISSUE_TITLE']
        body = row['ISSUE_BODY']

        # Handle NaN values for title and body
        title = '' if pd.isna(title) else title
        body = '' if pd.isna(body) else body

        labels = []
        for col in [f'ISSUE_LABEL_{i}' for i in range(6)]:
            if col in row and pd.notna(row[col]):
                labels.append(row[col])

        # Escape single quotes
        escaped_title = title.replace("'", "'\\''")
        escaped_body = body.replace("'", "'\\''")

        # Format labels for the command line
        label_flags = ",".join([f"'{label.replace('\'', '\'\\\'\'')}'" for label in labels])

        cmd = f"gh issue create --title '{escaped_title}' --body '{escaped_body}'"
        if label_flags:
            cmd += f" --label {label_flags}"

        print(cmd)

    print("Issue creation complete.")

def get_existing_labels():
    """
    Gets the existing labels in the repository.
    (Simulated to return an empty list as we cannot run gh commands without a token)
    """
    print("Simulating gh label list (returning empty list)")
    return []

def sync_labels(df):
    """
    Syncs labels from the TSV file with the repository.
    """
    print("Syncing labels...")
    label_columns = [col for col in df.columns if col.startswith('ISSUE_LABEL')]
    all_labels = set()
    for col in label_columns:
        # dropna() to remove empty cells
        labels = df[col].dropna().unique()
        for label in labels:
            all_labels.add(label)

    existing_labels = get_existing_labels()
    new_labels = all_labels - set(existing_labels)

    print("The following gh label create commands would be executed:")
    for label in new_labels:
        # Escape single quotes in the label name
        escaped_label = label.replace("'", "'\\''")
        print(f"gh label create '{escaped_label}' --color 'f29513'")

    print("Label sync complete.")

if __name__ == "__main__":
    main()
