"""
Singleton Util
==============
@Singleton decorator making a class to be
a singleton.
"""


def singleton(cls):
    # type: (object) -> object
    """
    :param cls:
    :return: singleton instance
    """
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton
