import re
import csv
from collections import Counter

# Base class for processing Star Wars data
class StarWarsDataProcessor:
    """Processes Star Wars data from a CSV file."""

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_csv(self):
        """Reads a CSV file and returns its content as a list of dictionaries."""
        try:
            with open(self.input_file, mode='r') as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.input_file} not found.")

    def write_csv(self, data, fieldnames):
        """Writes a list of dictionaries to a CSV file."""
        with open(self.output_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

# Subclass for specific data validation
class JediValidator(StarWarsDataProcessor):
    """Validates Star Wars data, including Jedi and lightsaber attributes."""

    NAME_REGEX = r'^[A-Za-z]+(?: [A-Za-z]+)*$'
    LIGHTSABER_REGEX = r'^(blue|green|purple|yellow|white|cyan)$'

    def validate_names(self, characters):
        """Validates character names using regex."""
        return [
            char for char in characters if re.match(self.NAME_REGEX, char.get("name", ""))
        ]

    def validate_lightsabers(self, characters):
        """Filters characters with valid lightsaber colors."""
        return [
            char for char in characters
            if re.match(self.LIGHTSABER_REGEX, char.get("lightsaber_color", "").lower())
        ]

    def homeworld_statistics(self, characters):
        """Returns a dictionary with counts of characters per homeworld."""
        homeworlds = [char.get("homeworld", "Unknown") for char in characters]
        return dict(Counter(homeworlds))

# Subclass for advanced Jedi analysis
class JediAnalyzer(JediValidator):
    """Performs analysis on validated Jedi data."""

    def analyze(self):
        """Processes and analyzes Jedi data."""
        characters = self.read_csv()

        # Step 1: Validate names
        valid_names = self.validate_names(characters)

        # Step 2: Validate lightsabers
        valid_jedi = self.validate_lightsabers(valid_names)

        # Step 3: Generate homeworld stats
        stats = self.homeworld_statistics(valid_jedi)

        # Save valid Jedi to the output file
        self.write_csv(valid_jedi, fieldnames=["name", "lightsaber_color", "homeworld"])

        return {"valid_jedi": valid_jedi, "stats": stats}
