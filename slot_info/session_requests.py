import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class SessionRequest:
    default_headers = headers = {
        "Content-Type": "application/json",
        "Accept-Language": "hi_IN",
        "user-agent": "*"
    }

    def __init__(self, headers=None,
                 max_retries=3,
                 backoff_factor=0.1):
        session_headers = self.default_headers if headers is None else headers

        retries = Retry(total=max_retries,
                        backoff_factor=backoff_factor)
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.session.headers = session_headers

    def get(self, url, **kwargs):
        try:
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_error:
            raise http_error
