import logging

import requests

from .base import Notification


log = logging.getLogger(__name__)


class Bugsnag(Notification):
    def __call__(self, token):
        with requests.Session() as http:
            r = http.post(
                'https://build.bugsnag.com/',
                json={
                    'apiKey': token,
                    'releaseStage': self.environment,
                    'appVersion': self.version,
                },
            )
            log.info('%s returned %s: %s', r.url, r.status_code, r.text)
