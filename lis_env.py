import math
import operator as op

Env = dict  # A Scheme environment (defined below) is a mapping of {variable: value}


def standard_env() -> Env:
    """An environment with some Scheme standard procedures."""
    env = Env()
