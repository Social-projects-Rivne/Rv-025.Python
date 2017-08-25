"""This module parses database's configfile
"""

from ConfigParser import ConfigParser


def config(filename='../config.ini', section='RDB'):
    """ Parse database's configfile

    Args:
        filename (str): file with parameters for connecting to database
        section (str): section name

    Returns:
        dict: keys are config variables names,
        values are config variable values
    """
    parser = ConfigParser()
    parser.read(filename)

    db = dict()
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section %s not found in the %s' % (section, filename))

    return db
