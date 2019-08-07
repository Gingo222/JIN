import logging
import time
from functools import wraps

from flask_restful import Api as _Api
from flask_restful.utils import unpack
from werkzeug.wrappers import Response as ResponseBase

logger = logging.getLogger(__name__)


class Api(_Api):
    def handle_error(self, ori_e):
        try:
            return self.make_response(ori_e.message, ori_e.code)
        except:
            logger.error('failed to handle error', exc_info=True)
            raise

    def output(self, resource):
        """Wraps a resource (as a flask view function), for cases where the
                resource does not directly return a response object

                :param resource: The resource as a flask view function
                """

        @wraps(resource)
        def wrapper(*args, **kwargs):
            resp = resource(*args, **kwargs)
            if isinstance(resp, ResponseBase):
                return resp
            data, code, headers = unpack(resp)
            # modify data to automatically generate consistent response structure
            data = {
                'data': data,
                'timestamp': int(time.time())
            }
            return self.make_response(data, code, headers=headers)
        wrapper.origin_func = resource
        return wrapper
