# This is not a test
from main import *
data = {
    "user": "joe",
    "pass": ["x", "y", "z"],
    "type": ["y", "n"],
}

print(generate_combinations(data))
