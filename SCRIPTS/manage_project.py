import pandas as pd
import os

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
    Main function to run the project management process.
    """
    print("--- Starting manage_project.py ---")

    tsv_file = get_tsv_file()
    if not tsv_file:
        print("No TSV file found in TSV_HERE directory.")
        return

    df = pd.read_csv(tsv_file, sep='\\t', engine='python')
    print(f"Successfully loaded {tsv_file} with {len(df)} rows.")

    project_name = df['PROJECT'].dropna().unique()[0]

    print(f"\\n--- Simulating Project Management for project: {project_name} ---")

    # Simulate getting the project number
    project_number = 1

    print(f"\\n--- Simulating Project Creation ---")
    print(f"gh project create \"{project_name}\" --owner \"@me\"")

    print(f"\\n--- Simulating Adding Issues to Project ---")
    issue_ids = [f"#{i+1}" for i in range(len(df))] # Placeholder issue IDs
    for issue_id in issue_ids:
        print(f"gh project item-add {project_number} --issue \"{issue_id}\"")

    print(f"\\n--- Simulating Updating Project Fields ---")
    project_fields = [col for col in df.columns if col.startswith('PROJECT_FIELD_')]

    for index, row in df.iterrows():
        issue_id = f"#{index+1}" # Placeholder issue ID
        for field_col in project_fields:
            if pd.notna(row[field_col]):
                field_name = field_col.split(':')[0].replace('PROJECT_FIELD_', '')
                field_value = row[field_col]
                print(f"gh project item-edit --project-number {project_number} --issue \"{issue_id}\" --field-name \"{field_name}\" --text \"{field_value}\"")

    print("\\n--- manage_project.py finished ---")

if __name__ == "__main__":
    main()
