import inject
from daily_jira.models import *
from daily_jira import Base
from daily_jira.dependencies import Config, MainDBSession
from daily_jira.util.db import CommitContext
import logging


config = inject.instance(Config)
logger = logging.getLogger(__name__)


def init_mysql():
    session = inject.instance(MainDBSession)
    with CommitContext(session):
        Base.metadata.create_all()


def init_app_env():
    init_mysql()
