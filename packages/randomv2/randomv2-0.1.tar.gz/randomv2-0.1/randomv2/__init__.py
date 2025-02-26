import random as _random  # Import built-in random
from .core import rand_inf, rand_prob, rand_prob_times  # Import your functions

# Manually expose all functions from random
globals().update({name: getattr(_random, name) for name in dir(_random) if not name.startswith("_")})

# Define __all__ to include both built-in and custom functions
__all__ = ["rand_inf", "rand_prob", "rand_prob_times"] + [name for name in dir(_random) if not name.startswith("_")]

