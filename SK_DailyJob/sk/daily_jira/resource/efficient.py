from flask import Flask, g
from flask import Blueprint
from flask_restful import Resource, reqparse
from daily_jira.resource import Api
from daily_jira.services.jira_result import jira_csv_result


class JiraMeta(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('project')
    get_parser.add_argument('broad')
    get_parser.add_argument('sprint')

    def post(self):
        args = self.get_parser.parse_args()
        project = args['project']
        broad = args['broad']
        sprint = args['sprint']
        return jira_csv_result('efficienty', project, broad, sprint)


def get_resources():
    blueprint = Blueprint('efficienty', __name__)
    api = Api(blueprint)
    api.add_resource(JiraMeta, '/jira/efficienty')
    return blueprint
