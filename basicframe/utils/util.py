from datetime import datetime

proxies = {
    'http': 'http://localhost:7890',
    'https': 'https://localhost:7890',
}


def generate_std_name(url):
    return f"{url.replace('/', '_').replace(':', '_').replace('.', '_')}"


def current_date_time(strf="%Y_%m_%d_%H:%M"):
    now = datetime.now()
    time_str = now.strftime(strf)
    return time_str


def withMetaclass(meta, *bases):
    """Create a base class with a metaclass."""

    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class MetaClass(meta):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(MetaClass, 'temporary_class', (), {})


