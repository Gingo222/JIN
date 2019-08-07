from daily_jira.services.jira_dataclass import JiraData
from daily_jira.services.jira_basic import JiraMeta
from daily_jira.dependencies import Config
import inject
from flask import send_file


config = inject.instance(Config)
jira_data = JiraData()
jira_meta = JiraMeta()


def jira_csv_result(file_type, project, sprint, board):
    if not project:
        project = Config.PROJECT, sprint = config.SPRINT, board = config.BROAD
    issues = jira_meta.get_jira_issues(project=project, sprint=sprint, board=board)
    issue_dict = jira_data.deal_issue(issues)
    for issue in issue_dict.items():
        for iss in issue[1]:
            jira_data.csv_writer(issue=iss, issue_type=issue[0], issues=issues, file_type=file_type)
    if file_type == 'story':
        return send_file(config.STORY_CSV_FILE)
    if file_type == 'efficienty':
        return send_file(config.EFFICIENCY_CSV_FILE)
    else:
        return None
