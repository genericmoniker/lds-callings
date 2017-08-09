

class AuthenticationError(Exception):
    pass


_service_config = None


def service_config():
    """Get the web service configuration.

    :return: deserialized JSON service configuration.
    """
    global _service_config
    if not _service_config:
        pass
        # fetch service config from https://tech.lds.org/mobile/ldstools/config.json
    return _service_config


def login(username, password):
    """Log in with an LDS Account.

    :param: username, or None to get from an LDS_USERNAME environment variable.
    :param: password, or None to get from an LDS_PASSWORD environment variable.
    :return: a "requests" session with login cookies set.
    :raise: AuthenticationError if the credentials are incorrect.
    """


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
