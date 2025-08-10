# L4Vnew-jules

gh issue create --title "$issue_title" --body "$issue_body" "${label_args[@]}"
gh issue create --label bug --label "help wanted"
gh label create bug --description "Something isn't working" --color E99695
gh issue create --title "I found a bug" --body "Nothing works" --label 
--title <string>

gh issue create --title "My New Issue" --body "This is the issue description." --label "bug,enhancement,priority"


goals: 

- use DRY coding

- read from any {file} inside `/TSV_HERE` to accomplish the following

- using gh cli and gh api commands:  import Labels, Issues, Sub-issues, Projects, Project fields, 

- use the gh cli line itself to determine which header (columns) to query

- use wildcards to reference header substrings, so the commands are string and location agnostic. 

- header strings are encoded as {command_flag}, so for ISSUE_BODY, ISSUE = command and BODY = flag

ex: 

command syntax = `gh <command> <action> --<flag> "<value>"` and header syntax = command_flag

command = `gh label create <value>`, so use values from all columns with 'label' substring

command = `gh issue create --title "<value>" --body "<value>" --label "<value>,<value>", so use values from columns {command_flag} = issue_title, issue_body, issue_label




) create custom labels

cms: gh label create {title}
note: do not include flags --color or --description


) create issues, including their title, body, label

gh issue create
title 
body 
label








project portion


create project custom field ... specify project number... field datatype ... field options... 


gh project field-create [<project number>] [flags]


--data-type <string>

--single-select-options <strings>



# Create a field with three options to select from for owner monalisa


$ gh project field-create 1 --owner monalisa --name "new field" --data-type "SINGLE_SELECT" --single-select-options "one,two,three"

Create a field in the current user's project "1"

$ gh project field-create 1 --owner "@me" --name "new field" --data-type "text"





title==

gh <command> <action> --<flag> string

gh project create --title <string>


gh <command>-<action> --<flag> string

gh project field -create 1 --name "field-name" --data-type "SINGLE_SELECT" --single-select-options 


J.PROJECT_TITLE
K.PROJECT_FIELD_PRIORITY:SINGLE_SELECT

command_flag:data-type


project_field_name:datatype


command_name:datatype


project portion


create project custom field ... specify project number... field datatype ... field options... 

gh project field-create 

-

gh project field-create [<project number>] [flags]


--data-type <string> ... DataType of the new field.: {TEXT|SINGLE_SELECT|DATE|NUMBER}

--single-select-options <strings> ... tsv values



# Create a field with three options to select from for owner monalisa


$ gh project field-create 1 --name "new field" --data-type "SINGLE_SELECT" --single-select-options "one,two,three"

Create a field in the current user's project "1"

$ gh project field-create 1 --owner "@me" --name "new field" --data-type "text"




repo map

/

├── README.md         
├── TSV_HERE     <-- folder contains user-file used for import 
├── SCRIPTS      <-- folder contains scripts
└── ...


        <-- This folder contains user-file used for import
├── project-idea-1/   <-- A folder for Project 1.
│   ├── README.md     <-- A detailed README for the project, including a plan of attack.
│   └── ...           <-- Prototype code, assets, etc.
├── project-idea-2/   <-- A folder for Project 2.
│   ├── README.md
│   └── ...
└── ...

/
├── .github
├── devNOTES
├── INDEX.md
├── L4VPlanners
├── Planner files
├── PLANNERv6.csv
├── PLANNERv6.tsv
├── PLANNERv6.txt
├── README.md
├── SCRIPTS
├── TSV_HERE
└── workflows - Shortcut.lnk