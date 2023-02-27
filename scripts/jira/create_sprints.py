import pendulum

destination_jira = get_destination_jira_client()

sprint_no = 11
DESTINATION_PROJECT_ID = 109

start_date = pendulum.datetime(2023, 3, 26)
end_date = start_date

while end_date.add(days=14) <= pendulum.datetime(2023, 12, 31):

    end_date = start_date.add(days=14)
    print(f"Sprint {sprint_no} - {start_date}<->{end_date}")
    destination_jira.create_sprint(board_id=DESTINATION_PROJECT_ID, name=f"Destination Sprint {sprint_no}", startDate=start_date.to_iso8601_string(), endDate=end_date.to_iso8601_string())
    # Increment the dates
    start_date = end_date
    sprint_no += 1
