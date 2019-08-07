import uuid
from sqlalchemy import func, Column, String, DateTime, Integer, Float, Numeric
from sqlalchemy_utils.types import UUIDType
from daily_jira import Base


class JiraMeta(Base):
    __table_name__ = 'jira_meta'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4(), index=True)
    story_id = Column(String(60), nullable=False, default='', index=True, unique=True)
    state = Column(String(16), nullable=False, index=True, default='')
    author = Column(String(30), nullable=False, index=True, default='')
    created_time = Column(DateTime)
    status_from = Column(String(60), nullable=False, default='', index=True)
    statues_to = Column(String(60), nullable=False, default='', index=True)

    def to_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return result

