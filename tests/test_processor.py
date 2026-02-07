import pytest
from src.processor import format_names_after_2000

SAMPLE = {
    "results": [
        {"name": {"first": "John", "last": "Doe"}, "dob": {"date": "1990-05-12T10:15:30.000Z"}},
        {"name": {"first": "Young", "last": "Star"}, "dob": {"date": "2002-01-01T00:00:00.000Z"}}
    ]
}

def test_format_names_after_2000():
    out = format_names_after_2000(SAMPLE)
    assert "John Doe" in out
    assert "Young Star" not in out
