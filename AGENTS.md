# AGENT.md


## Goal: 

Create Github Issues and Github Project from a user-file in this repository. 
	


## Include the following in your tools
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects
- https://docs.github.com/en/issues
- https://cli.github.com/manual/gh
- https://cli.github.com/manual/gh_issue
- https://cli.github.com/manual/gh_project
- https://cli.github.com/manual/gh_api



## important: 


- Use any user-file within ./*_HERE  (note: * is wildcard) 

- use the substrings in the gh command line itself to determine the columns and values to read from the user-file

- user-file headers are encoded as `gh <COMMAND>_<FLAG>[:<DATATYPE>]`

example1: command = `gh label create <value>`, so use values from all columns with *LABEL* (wildcar/substring) in the header  

example2: command = `gh issue create --title "<value>" --body "<value>" --label "<value>,<value>", so use column values from *TITLE*, *BODY*, *LABEL* (wildcard/substring)


- the strings in the ISSUE_BODY column are semi-colon delimited sub-issues. the text is filled with symbols, so be careful when manipulating this data



- scripts are user-triggered via local terminal OR github action

- scripts live in ./SCRIPTS




## Design Principles:

DRY Mapping
Column names and script behavior mirror GitHub CLI syntax for intuitive mapping.

Idempotency 
Agents/scripts skip work when it’s already done; no accidental duplicates.

Composability
Agents/scripts can run independently or in a chained pipeline.

Local & CI Friendly
No local-only hacks; all agents/scripts can run in GitHub Actions without modification.

Small, uncomplicated code 
Built around gh CLI, jq, and lightweight Python for portability.



## example workflow: 

flowchart TD

A[Preflight & Index TSV] --> B[Sync Repository Labels]
B --> C[Upsert Issues by Title]
C --> D[Expand Task Lists into Child Issues]
D --> E[Ensure Project and Project Fields Exist]
E --> F[Add Issues as Project Items and Set Field Values]
F --> G[Post-Run Summary and Optional JSON Log]



Preflight & index → parse TSV once, check required columns, cache existing_labels + existing_issues_by_key_label, warn/fail on duplicate keys.

Sync labels → create missing labels (once per unique label).

Upsert issues → create only if key label not found; attach title, body, labels.

Sub-issue pass → from ISSUE_BODY semicolon tasks; create child issues; append task list to parent.

Project setup → ensure project exists, create fields/options if missing.

Project population → add all issues, set field values.

Post-run summary → counts of created/skipped items; optional JSON log for auditing.
