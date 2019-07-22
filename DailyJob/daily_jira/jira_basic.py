from jira import JIRA
from daily_jira.dependencies import Config
import inject
import json
import requests


config = inject.instance(Config)


class JiraMeta(object):

    def __init__(self):
        self.jira = self.jira_basic_login()
        self.jira_web = self.jira_url_login()

    @staticmethod
    def jira_basic_login():
        jira = JIRA(server=config.JIRA_URL,
                    basic_auth=tuple(config.AUTH))
        return jira

    @staticmethod
    def jira_url_login():
        session = requests.session()
        session.post(url=config.JIRA_LOGIN,
                     data=config.JIRA_AUTH_DATA)
        return session

    def get_jira_projects(self):
        projects = self.jira.projects()
        for project in projects:
            if project.name == config.PROJECT:
                return project.key

    def get_jira_board(self, board_name):
        boards = self.jira.boards()
        for board in boards:
            if board.name == board_name:
                return board.id

    def get_jira_sprint(self, board_id):
        sprints = self.jira.sprints(board_id=board_id)
        return sprints[-1].id

    def get_jira_changelog(self, issue):
        print(config.CHANGE_LOG.replace("{}", issue))
        res = self.jira_web.get(url=config.CHANGE_LOG.replace("{}", issue))
        return json.loads(res.text)

    def get_jira_issues(self, project=None, sprint=None):
        if project is None:
            return
        if sprint is None:
            board_id = self.get_jira_board(config.BROAD)
            sprint_id = self.get_jira_sprint(board_id)
        else:
            sprint_id = sprint
        print('project={} and Sprint={}'.format(project, sprint_id))
        issue = self.jira.search_issues('project={} and Sprint={}'.format(project, sprint_id),
                                        maxResults=1000,
                                        json_result=True)
        print(json.dumps(issue['issues']))
        return issue['issues']

    def get_jira_story_point(self, issue):
        pass


if __name__ == '__main__':
    jira = JiraMeta()
    issue = (jira.get_jira_issues(project=config.PROJECT))
