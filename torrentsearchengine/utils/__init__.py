from torrentsearchengine.utils.kwargs import *
from torrentsearchengine.utils.urlutils import *
from torrentsearchengine.utils.jsonvalidator import *


def simple_hash(s):
    h = hex(hash(s))
    if h.startswith('-'):
        h = h[3:]
    else:
        h = h[2:]
    return h