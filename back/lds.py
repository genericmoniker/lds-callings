import os
import requests


class AuthenticationError(Exception):
    pass


_service_config = None


def service_config():

    """Get the web service configuration.

    :return: deserialized JSON service configuration.
    """
    global _service_config
    if not _service_config:
        r = requests.get('https://tech.lds.org/mobile/ldstools/config.json')
        r.raise_for_status()
        _service_config = r.json()
    return _service_config


def login(username=None, password=None):
    """Log in with an LDS Account.

    :param: username, or None to get from an LDS_USERNAME environment variable.
    :param: password, or None to get from an LDS_PASSWORD environment variable.
    :return: a "requests" session with login cookies set.
    :raise: AuthenticationError if the credentials are incorrect.
    """
    username = username or os.environ.get('LDS_USERNAME')
    password = password or os.environ.get('LDS_PASSWORD')

    s = requests.Session()
    url = service_config()['auth-url']
    data = {'username': username, 'password': password}
    r = s.post(url, data)
    if r.status_code != 200:
        raise AuthenticationError(r)
    return s


def fetch_current_user_unit(s):
    """Fetch the unit number of the logged-in user.

    :param s: an authenticated "requests" session.
    :return: unit number as a string.
    """


def fetch_callings(s, unit):
    """Fetch the directory with callings for given unit.

    :param unit: unit number as a string.
    :param s: an authenticated "requests" session.
    :return: deserialized JSON callings data.
    """


if __name__ == '__main__':
    login()
