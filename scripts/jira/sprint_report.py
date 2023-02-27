"""
Make you find the custom field for Story Points in your Jira instance.
and then replace customfield_10024 with your custom field.
"""
from datetime import datetime, timedelta
from jira import JIRA
from requests_toolbelt import user_agent
import polars as pl


PROJECTS = {
    "ABC": 100,
    "BCD": 101,
}


BA = [
    "BA One",
    "BA Two",
    "BA Three",
]

DEV = [
    "Dev One",
    "DEV Two",
    "DEV Three",
]



def create_jira_client(server, username, password):
    """Create a JIRA client."""
    return JIRA(
        server=server,
        basic_auth=(username, password),
    )

def get_destination_jira_client():
    """Get a JIRA client for your instance."""
    return create_jira_client(
        server="https://destination.atlassian.net",
        username="",
        password="",
    )



def total_by_sprint(df):
    res = df[['Sprint', 'StoryPoints']].groupby('Sprint').agg([pl.sum('StoryPoints')])
    return res

def total_by_project(df):
    res = df[['Project', 'StoryPoints']].groupby('Project').mean()
    return res

def average_by_sprint(df):
    res = df[['Sprint', 'StoryPoints']].sort('Sprint', descending=False).groupby('Sprint').mean()
    return res

def average_by_user(df):
    res = df[['User', 'StoryPoints']].groupby('User').mean()
    return res

def average_by_ba(df):
    res = df.filter(pl.col('BA') == True)[['User', 'StoryPoints']].groupby('User').mean()
    by_user = res.groupby('User').mean()
    by_points = res['StoryPoints'].mean()
    return by_user, by_points

def average_by_dev(df):
    res = df.filter(pl.col('DEV') == True)[['User', 'StoryPoints']].groupby('User').mean()
    by_user = res.sort('StoryPoints', descending=True).groupby('User').mean()
    by_points = res['StoryPoints'].mean()
    return by_user, by_points


def get_current_week_num():
    now = datetime.now()

    # Calculate the week number using isocalendar() method
    year, week_num, day_of_week = now.isocalendar()
    return week_num

def get_all_sprints(board_id, not_before=None):
    """Get all sprints."""
    destination_jira = get_destination_jira_client()
    c = get_current_week_num()

    sprints = destination_jira.sprints(board_id=board_id)

    return sprints

RESULT = {}
def get_sprint_stats(project_id, sprint_name):
    """Get sprint stats."""
    # print("Getting sprint stats for", sprint_name)

    destination_jira = get_destination_jira_client()

    issues = destination_jira.search_issues(
        f'project = {project_id} AND sprint = "{sprint_name}" AND issuetype in (Bug, Story)',
    )

    result = {}

    for f in (issues):

        story_points = f.fields.customfield_10024
        if f.fields.customfield_10024 == None:
            story_points = 0

        result[f.fields.assignee] = result.get(f.fields.assignee, 0) + story_points

    return result


"Write a function which retreives user worksload by sprint"
if __name__ == "__main__":


    NEW_RES = {}

    for board_key, board_id in PROJECTS.items():
        sprints = get_all_sprints(board_id)

        shortlisted_sprints = []

        for sprint in sprints:
            monthAgo = datetime.now() - timedelta(days=30)
            sprintAfter = datetime.now() + timedelta(days=14)

            is_not_future_or_active = (sprint.state != 'future' and sprint.state != 'active')

            startDate = datetime.strptime(sprint.startDate, '%Y-%m-%dT%H:%M:%S.%fZ')
            endDate = datetime.strptime(sprint.endDate, '%Y-%m-%dT%H:%M:%S.%fZ')

            if (startDate >=  monthAgo and endDate <= sprintAfter) and is_not_future_or_active:
                shortlisted_sprints.append(sprint)

        print("Shortlisted sprints for", board_key, "are", [sprint.name for sprint in shortlisted_sprints])

        for sprint in shortlisted_sprints:
            project_id = sprint.name.split(' ')[0]
            if project_id:
                a = get_sprint_stats(project_id, sprint.name)
                for user, story_points in a.items():
                    u = getattr(user, 'displayName', "None")
                    NEW_RES['Project'] = NEW_RES.get('Project', []) + [board_key]
                    NEW_RES['Sprint'] = NEW_RES.get('Sprint', []) + [sprint.name]
                    NEW_RES['SprintStartDate'] = NEW_RES.get('SprintStartDate', []) + [sprint.startDate]
                    NEW_RES['SprintEndDate'] = NEW_RES.get('SprintEndDate', []) + [sprint.endDate]
                    NEW_RES['SprintState'] = NEW_RES.get('SprintState', []) + [sprint.state]
                    NEW_RES["StoryPoints"] = NEW_RES.get("StoryPoints", []) + [story_points]
                    NEW_RES["User"] = NEW_RES.get("User", []) + [u]
                    NEW_RES["BA"] = NEW_RES.get("BA", []) + [True if u in BA else False]
                    NEW_RES["DEV"] = NEW_RES.get("DEV", []) + [True if u in DEV else False]
            
            else:
                print("No project found for", sprint.name)


    df = pl.DataFrame._from_dict(NEW_RES)

    # user_res = df.groupby('User', 'Sprint').agg([pl.sum('StoryPoints')]).sort(['Sprint', 'User'])
    # sprint_res = df.groupby('Sprint').agg([pl.sum('StoryPoints')]).sort('Sprint')
    pl.Config.set_tbl_rows(100)
    pl.Config.set_tbl_cols(100)

    print("--"*10, "By Project", "--"*10)
    print(total_by_project(df))

    # print(df)
    print("--"*10, "Average by sprint", "--"*10)
    print(average_by_sprint(df))

    print("--"*10, "Average by user", "--"*10)
    print(average_by_user(df))

    print("--"*10, "Average by BA", "--"*10)
    print(average_by_ba(df))

    print("--"*10, "Average by DEV", "--"*10)
    print(average_by_dev(df))

