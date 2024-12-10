import os
import csv
import pytest
from starwars import JediAnalyzer

@pytest.fixture
def setup_files():
    """Creates test input and output files."""
    input_file = "test_characters.csv"
    output_file = "test_valid_jedi.csv"

    # Create test input file
    with open(input_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "lightsaber_color", "homeworld"])
        writer.writeheader()
        writer.writerows([
            {"name": "Luke Skywalker", "lightsaber_color": "Blue", "homeworld": "Tatooine"},
            {"name": "Darth Vader", "lightsaber_color": "Red", "homeworld": "Tatooine"},
            {"name": "Yoda", "lightsaber_color": "Green", "homeworld": "Dagobah"},
            {"name": "Leia Organa", "lightsaber_color": "", "homeworld": "Alderaan"},
            {"name": "123 Invalid", "lightsaber_color": "Blue", "homeworld": "Unknown"},
        ])

    yield input_file, output_file

    # Cleanup test files
    os.remove(input_file)
    os.remove(output_file)

def test_analyze(setup_files):
    """Tests the Jedi analysis process."""
    input_file, output_file = setup_files
    analyzer = JediAnalyzer(input_file, output_file)

    results = analyzer.analyze()
    valid_jedi = results["valid_jedi"]
    stats = results["stats"]

    # Assert valid Jedi count
    assert len(valid_jedi) == 2
    assert valid_jedi[0]["name"] == "Luke Skywalker"
    assert valid_jedi[1]["name"] == "Yoda"

    # Assert homeworld statistics
    assert stats == {"Tatooine": 1, "Dagobah": 1}

    # Assert output file contents
    with open(output_file, mode='r') as file:
        reader = list(csv.DictReader(file))
        assert len(reader) == 2
        assert reader[0]["name"] == "Luke Skywalker"
        assert reader[1]["name"] == "Yoda"
