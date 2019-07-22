from daily_jira.jira_dataclass import JiraData
from daily_jira.jira_basic import JiraMeta
from daily_jira.dependencies import Config
import inject


config = inject.instance(Config)
jira_data = JiraData()
jira_meta = JiraMeta()


def jira_csv_result():
    issues = jira_meta.get_jira_issues(project=Config.PROJECT, sprint=config.SPRINT)
    issue_dict = jira_data.deal_issue(issues)
    for issue in issue_dict.items():
        for iss in issue[1]:
            jira_data.csv_writer(issue=iss, issue_type=issue[0], issues=issues)


if __name__ == '__main__':
    jira_csv_result()