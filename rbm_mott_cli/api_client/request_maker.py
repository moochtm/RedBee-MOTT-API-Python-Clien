from json.decoder import JSONDecodeError
import requests
import functools
import json

import logging
logger = logging.getLogger(__name__)


class Request:
    def __init__(self, method):
        self.method = method.upper()
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }

    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(obj, *args, **kwargs) -> requests.request:
            logger.info('-'*60)
            logger.info(f'{str(type(obj).__name__)}: {str(f.__name__)}')

            payload = f(obj, *args, **kwargs)
            args = {
                'method': self.method,
                'url': payload['url'],
                'headers': {**self.headers, **obj.default_headers},
                'params': payload['params'] if 'params' in payload.keys() else None,
                'data': payload['data'].encode('utf8') if 'data' in payload.keys() else None
            }
            response = requests.request(**args)

            logger.debug(f'{str(f.__name__)}: args: {json.dumps(args, indent=4)}')
            try:
                logger.info(f'{str(f.__name__)}: json: {json.dumps(response.json(), indent=4)}')
            except JSONDecodeError as e:
                logger.info('{str(f.__name__)}: json: None')
            logger.info(f'{str(f.__name__)}: status code: {response.status_code}')

            return response
        return wrapper
