#!/usr/bin/env python3
"""A complex Python file for testing Phiton conversion with advanced features."""

import math
import random
from dataclasses import dataclass
from typing import Any


@dataclass
class Point:
    """A simple 2D point class."""

    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Calculate the Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Shape:
    """Base class for geometric shapes."""

    def __init__(self, name: str):
        """Initialize a shape with a name."""
        self.name = name

    def area(self) -> float:
        """Calculate the area of the shape."""
        msg = "Subclasses must implement area()"
        raise NotImplementedError(msg)

    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        msg = "Subclasses must implement perimeter()"
        raise NotImplementedError(msg)

    def __str__(self) -> str:
        return (
            f"{self.name} (area: {self.area():.2f}, perimeter: {self.perimeter():.2f})"
        )


class Circle(Shape):
    """A circle shape."""

    def __init__(self, center: Point, radius: float):
        """Initialize a circle with a center point and radius."""
        super().__init__("Circle")
        self.center = center
        self.radius = radius

    def area(self) -> float:
        """Calculate the area of the circle."""
        return math.pi * self.radius**2

    def perimeter(self) -> float:
        """Calculate the perimeter (circumference) of the circle."""
        return 2 * math.pi * self.radius

    def contains_point(self, point: Point) -> bool:
        """Check if a point is inside the circle."""
        return self.center.distance_to(point) <= self.radius


class Rectangle(Shape):
    """A rectangle shape."""

    def __init__(self, top_left: Point, width: float, height: float):
        """Initialize a rectangle with top-left corner, width, and height."""
        super().__init__("Rectangle")
        self.top_left = top_left
        self.width = width
        self.height = height

    def area(self) -> float:
        """Calculate the area of the rectangle."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Calculate the perimeter of the rectangle."""
        return 2 * (self.width + self.height)

    def contains_point(self, point: Point) -> bool:
        """Check if a point is inside the rectangle."""
        return (
            self.top_left.x <= point.x <= self.top_left.x + self.width
            and self.top_left.y <= point.y <= self.top_left.y + self.height
        )


class ShapeCollection:
    """A collection of shapes with operations."""

    def __init__(self, shapes: list[Shape] | None = None):
        """Initialize a collection with optional shapes."""
        self.shapes = shapes or []

    def add_shape(self, shape: Shape) -> None:
        """Add a shape to the collection."""
        self.shapes.append(shape)

    def total_area(self) -> float:
        """Calculate the total area of all shapes."""
        return sum(shape.area() for shape in self.shapes)

    def total_perimeter(self) -> float:
        """Calculate the total perimeter of all shapes."""
        return sum(shape.perimeter() for shape in self.shapes)

    def find_shapes_containing_point(self, point: Point) -> list[Shape]:
        """Find all shapes that contain the given point."""
        return [
            shape
            for shape in self.shapes
            if hasattr(shape, "contains_point") and shape.contains_point(point)
        ]

    def get_shapes_by_type(self, shape_type: type) -> list[Shape]:
        """Get all shapes of a specific type."""
        return [shape for shape in self.shapes if isinstance(shape, shape_type)]

    def __len__(self) -> int:
        return len(self.shapes)

    def __iter__(self):
        return iter(self.shapes)


def generate_random_shapes(count: int) -> ShapeCollection:
    """Generate a collection of random shapes.

    Args:
        count: Number of shapes to generate

    Returns:
        A collection of random shapes
    """
    collection = ShapeCollection()

    for _ in range(count):
        # Generate random parameters
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        point = Point(x, y)

        # Randomly choose between Circle and Rectangle
        if random.random() < 0.5:
            radius = random.uniform(1, 5)
            collection.add_shape(Circle(point, radius))
        else:
            width = random.uniform(1, 5)
            height = random.uniform(1, 5)
            collection.add_shape(Rectangle(point, width, height))

    return collection


def analyze_shapes(collection: ShapeCollection) -> dict[str, Any]:
    """Analyze a collection of shapes and return statistics.

    Args:
        collection: Collection of shapes to analyze

    Returns:
        Dictionary with analysis results
    """
    circles = collection.get_shapes_by_type(Circle)
    rectangles = collection.get_shapes_by_type(Rectangle)

    # Calculate average areas
    avg_circle_area = sum(c.area() for c in circles) / len(circles) if circles else 0
    avg_rect_area = (
        sum(r.area() for r in rectangles) / len(rectangles) if rectangles else 0
    )

    # Find shapes with largest and smallest areas
    all_shapes = list(collection)
    largest_shape = max(all_shapes, key=lambda s: s.area()) if all_shapes else None
    smallest_shape = min(all_shapes, key=lambda s: s.area()) if all_shapes else None

    return {
        "total_shapes": len(collection),
        "circle_count": len(circles),
        "rectangle_count": len(rectangles),
        "total_area": collection.total_area(),
        "total_perimeter": collection.total_perimeter(),
        "avg_circle_area": avg_circle_area,
        "avg_rectangle_area": avg_rect_area,
        "largest_shape": largest_shape,
        "smallest_shape": smallest_shape,
    }


def main():
    """Main function to demonstrate the shape operations."""
    # Create some shapes
    collection = generate_random_shapes(10)

    # Analyze the shapes
    results = analyze_shapes(collection)

    # Print the results

    if results["largest_shape"]:
        pass

    if results["smallest_shape"]:
        pass

    # Test point containment
    test_point = Point(0, 0)
    containing_shapes = collection.find_shapes_containing_point(test_point)
    for _shape in containing_shapes:
        pass


if __name__ == "__main__":
    main()
