import os
from typing import Any
from main import generate_parser_form_combinations, parse_form_file_lookups


os.chdir(os.path.dirname(__file__))


def test_generates_all_combinations():
    data: Any = {
        "user": "joe",
        "pass": ["x", "y", "z"],
        "type": ["y", "n"],
        "$file": "./wordlist.txt",
    }
    combinations = list(generate_parser_form_combinations(data))
    assert len(combinations) == 3 * 2
    combinations = list(generate_parser_form_combinations(parse_form_file_lookups(data)))
    print(combinations)
    assert len(combinations) == 3 * 2 * 5
