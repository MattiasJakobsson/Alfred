import inspect


def get_available_commands(cls):
    return [item for item in inspect.getmembers(cls, predicate=inspect.ismethod) if item[0].endswith('_command')]


def get_available_queries(cls):
    return [item for item in inspect.getmembers(cls, predicate=inspect.ismethod) if item[0].endswith('_query')]
