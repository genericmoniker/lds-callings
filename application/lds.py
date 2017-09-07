"""
Access to the LDS Tools web services.

Documentation: http://tech.lds.org/wiki/LDS_Tools_Web_Services
"""
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
    :return: a "requests" session with login cookies set, current user detail.
    :raise: AuthenticationError if the credentials are incorrect.
    """
    username = username or os.environ.get('LDS_USERNAME')
    password = password or os.environ.get('LDS_PASSWORD')

    s = requests.Session()
    url = service_config()['auth-url']
    data = {'username': username, 'password': password}
    r = s.post(url, data, allow_redirects=False)
    if r.status_code != 200:
        raise AuthenticationError(r)
    return s, fetch_current_user_detail(s)


def fetch_current_user_detail(s):
    """Fetch the details of the logged-in user.

    :param s: an authenticated "requests" session.
    :return: deserialized JSON detail data.
    """
    url = service_config()['current-user-detail']
    r = s.get(url)
    r.raise_for_status()
    return r.json()


def fetch_current_user_assignments(s):
    """Fetch the member assignments of the logged-in user.

    :param s: an authenticated "requests" session.
    :return: deserialized JSON assignment data.
    """


def fetch_current_user_id(s):
    """Fetch the member id of the logged-in user.

    :param s: an authenticated "requests" session.
    :return: member id as a string.
    """


def fetch_callings(s, unit):
    """Fetch the directory with callings for given unit.

    :param unit: unit number.
    :param s: an authenticated "requests" session.
    :return: deserialized JSON callings data.
    """
    unit = str(unit)
    url = service_config()['unit-members-and-callings'].replace('%@', unit)
    r = s.get(url)
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    login()
