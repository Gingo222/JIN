from _threading_local import local
from typing import (
    Callable,
    List,
)
from sqlalchemy.orm import Session
import logging
import inject
from functools import wraps


logger = logging.getLogger(__name__)


class CommitContext:
    registry = local()

    def __init__(self, session: Session, do_commit_at_outermost=True):
        self.session = session
        self.id = str(id(session))
        self.after_commit_queue_id = f'queue_{self.id}'
        self.do_commit_at_outermost = do_commit_at_outermost
        try:
            assert getattr(self.registry, self.id)
            self.is_outermost = False
        except AttributeError:
            self.is_outermost = True
            setattr(self.registry, self.id, True)
            setattr(self.registry, self.after_commit_queue_id, [])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_outermost:
            after_commit_queue: List[Callable] = getattr(self.registry, self.after_commit_queue_id)
            delattr(self.registry, self.id)
            delattr(self.registry, self.after_commit_queue_id)
            if exc_type:
                self.session.rollback()
            else:
                if self.do_commit_at_outermost:
                    self.session.commit()
                    for func in after_commit_queue:
                        try:
                            func()
                        except KeyboardInterrupt:
                            raise
                        except:
                            logger.error(f'failed to execute {func.__name__}', exc_info=True)
                else:
                    self.session.rollback()
        else:
            if not exc_type:
                self.session.flush()

    @classmethod
    def add_after_commit_call(cls, session: Session, func: Callable):
        after_commit_queue_id = f'queue_{str(id(session))}'
        after_commit_queue: List[Callable] = getattr(cls.registry, after_commit_queue_id)
        after_commit_queue.append(func)


def autocommit(session_cls, do_commit_at_outermost=True):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            session = inject.instance(session_cls)
            with CommitContext(session, do_commit_at_outermost=do_commit_at_outermost):
                return func(*args, **kwargs)
        return wrap
    return decorator