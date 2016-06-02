import re

__version__ = "0.0.3"

compare = {
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
    "=": lambda a, b: a == b,
    "==": lambda a, b: a == b
}

DOWN = -1
UP = 1
IDLE = 0

TRUTHINESS = ["true", "t", "yes", "y", "1"]

FLAP_SIGNATURES = [
    [-1, 1, -1, 1],
    [1, -1, 1, -1],
    [-1, 0, 1, 0, -1, 0, 1],
    [1, 0, -1, 0, 1, 0, -1]
]


RE_VERSION_CHECK = re.compile(r"^\d+\.\d+\.\d+")
RE_DELIMITERS = re.compile(r"[\s,|/]+")
RE_THRESHOLD = re.compile(r"(?P<op>[=><]{1,2})\s*(?P<val>[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?)")
#          capture group op ^     ^          ^
#          any 1 or 2 variations   ^^^^^^^^^^ of =, >, <
#          spaces 0 or more                   ^^^
#          capture group val                     ^      ^                                   ^
#          complex signed decimal w/ scientific notation ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# if you hate this explanation or it's just not enough... https://regex101.com/
