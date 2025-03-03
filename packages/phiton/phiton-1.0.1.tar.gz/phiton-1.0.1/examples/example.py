#!/usr/bin/env python3
"""Example Python file to test Phiton compression."""

import math


def calculate_statistics(numbers: list[float]) -> dict[str, float]:
    """Calculate basic statistics for a list of numbers.

    Args:
        numbers: List of numbers to analyze

    Returns:
        Dictionary with statistics (mean, median, std_dev)
    """
    if not numbers:
        return {"mean": 0.0, "median": 0.0, "std_dev": 0.0}

    # Calculate mean
    mean = sum(numbers) / len(numbers)

    # Calculate median
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n % 2 == 0:
        median = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
    else:
        median = sorted_numbers[n // 2]

    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    std_dev = math.sqrt(variance)

    return {"mean": mean, "median": median, "std_dev": std_dev}


class DataAnalyzer:
    """Class for analyzing data."""

    def __init__(self, name: str, data: list[float] | None = None):
        """Initialize the analyzer.

        Args:
            name: Name of the analyzer
            data: Optional initial data
        """
        self.name = name
        self.data = data or []
        self.results: dict[str, float | str] = {}

    def add_data(self, values: list[float]) -> None:
        """Add data to the analyzer.

        Args:
            values: List of values to add
        """
        self.data.extend(values)

    def analyze(self) -> dict[str, float | str]:
        """Analyze the data and return statistics.

        Returns:
            Dictionary with analysis results
        """
        if not self.data:
            return {"error": "No data to analyze"}

        stats = calculate_statistics(self.data)
        self.results = {"name": self.name, "count": len(self.data), **stats}
        return self.results

    def __str__(self) -> str:
        """Return string representation of the analyzer."""
        if not self.results:
            return f"DataAnalyzer({self.name}, {len(self.data)} items, not analyzed)"

        return (
            f"DataAnalyzer({self.name}, {self.results['count']} items):\n"
            f"  Mean: {self.results['mean']:.2f}\n"
            f"  Median: {self.results['median']:.2f}\n"
            f"  Std Dev: {self.results['std_dev']:.2f}"
        )


def main() -> None:
    """Main function to demonstrate the DataAnalyzer."""
    # Create an analyzer
    analyzer = DataAnalyzer("Temperature Data")

    # Add some data
    temperatures = [22.5, 23.1, 19.8, 21.3, 20.9, 24.7, 22.8, 21.5, 23.2, 22.1]
    analyzer.add_data(temperatures)

    # Analyze and print results
    analyzer.analyze()


if __name__ == "__main__":
    main()
