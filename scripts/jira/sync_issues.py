from jira import JIRA
from requests_toolbelt import user_agent

# cog --> Atlassian account settings --> Security --> create api token

# This should be Remote Jira
ISSUES_TO_SYNC = [
    "XXX-177",
]
PROJECT_ID = 'PROJECT_ID_TO_SYN_TO'

def create_jira_client(server, username, password):
    """Create a JIRA client."""
    return JIRA(
        server=server,
        basic_auth=(username, password),
    )

def get_destination_jira_client():
    """Get a JIRA client for destination."""
    return create_jira_client(
        server="https://destination.atlassian.net",
        username="", # This should your username in destination JIRA
        password="", # This should token created from JIRA account settings
    )

def get_remote_jira_client():
    """Get a JIRA client for remote."""
    return create_jira_client(
        server="", # This should be remote Jira
        username="", # This should your username in remote JIRA
        password="", # This should token created from JIRA account settings
    )


def sync_issues():
    for issue in ISSUES_TO_SYNC:
        sync_issue(issue)


def sync_issue(issue_key):
    """Sync an issue."""
    print(f"Syncing issue {issue_key}")
    remote_jira = get_destination_jira_client()
    destination_jira = get_remote_jira_client()

    remote_issue = remote_jira.issue(issue_key)
    existing_issues = destination_jira.search_issues(f'project = {PROJECT_ID} AND summary ~ "{remote_issue.fields.summary}"')

    if existing_issues:
        print(f"Issue already exists - Copies found {len(existing_issues)} - Issue ID: {existing_issues[0].key}")
        return

    destination_issue = destination_jira.create_issue(project=PROJECT_ID,
                                summary=remote_issue.fields.summary,
                                description=remote_issue.fields.description,
                                issuetype=remote_issue.fields.issuetype.raw
                                )

    for attachment in remote_issue.fields.attachment:

        with open(attachment.filename, 'wb') as f:
            f.write(attachment.get())

        # Binary mode is important
        with open(attachment.filename, 'rb') as f:
            destination_jira.add_attachment(issue=destination_issue, attachment=f, filename=attachment.filename)

    print(f"Created issue - remote: {remote_issue.key} - destination - {destination_issue.key}")

if __name__ == "__main__":
    sync_issues()
