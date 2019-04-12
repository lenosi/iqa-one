import os
import sys
import errno
from io import IOBase

basename = os.path.basename(sys.argv[0])


# utils
def substitute_main_filename(pattern):
    """ if pattern contains %s, substitute that with script filename
    @type pattern: str, NoneType, file
    @param pattern: filename pattern, with or without %s, or NoneType or file
    @rtype: str, NoneType, file
    @return: substituted string with script's filename, if applicable, None and file will pass through
    """
    tmp = pattern
    if tmp is None or isinstance(tmp, IOBase):
        return tmp
    if '%s' in pattern:
        tmp = pattern % (basename,)
    return tmp


def prepare_file_path(filename):
    """ Checks filepath if it exists, otherwise create all necessary dirs
    @param filename: logging filename / filepath
    @return: None
    """
    tmp = os.path.dirname(filename)
    if tmp:
        try:
            os.makedirs(tmp)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
