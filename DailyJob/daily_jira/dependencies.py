from dataclasses import dataclass
from typing import Tuple
import os
import yaml


@dataclass
class Config:
    IP: str = '103.211.47.132'
    PORT: str = '8080'
    USER: str = 'jinjie'
    PWD: str = '123'
    ISSUE: str = 'ISSUE'
    JIRA_URL: str = 'http://{}:{}'.format(IP, PORT)
    JIRA_LOGIN: str = '{}/login.jsp'.format(JIRA_URL)
    CHANGE_LOG: str = '{}/rest/api/latest/issue/{}?expand=changelog'.format(JIRA_URL, ISSUE)
    AUTH: Tuple[str] = ('jinjie', '123')
    JIRA_AUTH_DATA: str = ''
    STORY_CSV_FILE: str = ''
    EFFICIENCY_CSV_FILE: str = ''
    PROJECT: str = '冠脉智能诊断'
    BROAD: str = '冠脉研发'
    SPRINT: str = ''


def bind_config(binder):
    config_filename = os.getenv('CONFIG')
    if not config_filename:
        config_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'jira.yml')
    with open(config_filename) as fin:
        data = yaml.load(fin)
        config = Config(**data)
    binder.bind(Config, config)


def bind(binder):
    binder.install(bind_config)


