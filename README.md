Crowdskout Alfred Workflow
=====================

## Requirements
1. [Alfred](http://www.alfredapp.com/#download)
2. [Alfred Powerpack](https://buy.alfredapp.com/)

## Installation
1. Download the latest .alfredworkflow file from [releases](https://github.com/Elite50/Crowdskout-Alfred-Workflow/releases) page
2. Double-click to import into Alfred

## Commands
| Command | Description |
| ------- | ------------|
| `crowdskout {endpoint}` | Jump to somewhere in the app |
| `cs {endpoint}` | Alias of `crowdskout` |
| `jira {options} {query}` | Jump to Crowdskout JIRA |
| `jirasetuser {username}` | Set JIRA user name |
| `jirasetpassword {password}` | Set JIRA password |
| `jiraclearuser` | Clear JIRA credential settings |
| `cs-update workflow:update` | Run manual update |


Available JIRA options

| Option | Description |
| ------- | ------------|
| `open` | Jump to ticket with given ticket number |
| `search` | Search tickets with given keywords |
| `current_sprint` | Open the kanban of current sprint |
| `backlog` | Open the backlog list |
| `create` | Create a new JIRA ticket |
| `my_open_issue` | List of my open tickets |
| `report_by_me` | List of tickets reported by me |
| `reports` | Report page |
| `components` | Components page |
| `data_import` | Data import board |
