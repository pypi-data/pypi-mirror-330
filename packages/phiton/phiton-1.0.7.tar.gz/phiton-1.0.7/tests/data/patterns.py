#!/usr/bin/env python3
"""A Python file with common patterns for testing Phiton's pattern recognition."""

import os
import re


def list_comprehension_examples():
    """Examples of list comprehensions."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Basic list comprehension
    squares = [x**2 for x in numbers]

    # With condition
    even_squares = [x**2 for x in numbers if x % 2 == 0]

    # Nested list comprehension
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [x for row in matrix for x in row]

    # With function call
    names = ["Alice", "Bob", "Charlie", "David"]
    lengths = [len(name) for name in names]

    return {
        "squares": squares,
        "even_squares": even_squares,
        "flattened": flattened,
        "lengths": lengths,
    }


def control_flow_patterns():
    """Examples of common control flow patterns."""
    result = []

    # if-else pattern
    x = 10
    if x > 5:
        result.append("x is greater than 5")
    else:
        result.append("x is not greater than 5")

    # if-elif-else pattern
    if x < 5:
        result.append("x is less than 5")
    elif x < 10:
        result.append("x is between 5 and 10")
    else:
        result.append("x is 10 or greater")

    # Ternary operator
    message = "even" if x % 2 == 0 else "odd"
    result.append(f"x is {message}")

    # None check
    y = None
    if y is not None:
        result.append("y has a value")
    else:
        result.append("y is None")

    # Early return pattern
    def early_return(value):
        if value < 0:
            return "negative"
        if value == 0:
            return "zero"
        return "positive"

    result.append(early_return(x))

    # Loop with break
    for i in range(10):
        if i > 5:
            result.append(f"Breaking at {i}")
            break

    # Loop with continue
    for i in range(5):
        if i % 2 == 0:
            continue
        result.append(f"Odd number: {i}")

    return result


def function_patterns():
    """Examples of common function patterns."""

    # Map function
    numbers = [1, 2, 3, 4, 5]
    doubled = [x * 2 for x in numbers]

    # Filter function
    evens = list(filter(lambda x: x % 2 == 0, numbers))

    # Reduce function
    from functools import reduce

    product = reduce(lambda x, y: x * y, numbers)

    # Function with default arguments
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    # Function with *args and **kwargs
    def combine(*args, **kwargs):
        return {"args": args, "kwargs": kwargs}

    # Decorator example
    def timing_decorator(func):
        def wrapper(*args, **kwargs):
            import time

            time.time()
            result = func(*args, **kwargs)
            time.time()
            return result

        return wrapper

    @timing_decorator
    def slow_function():
        import time

        time.sleep(0.1)
        return "Done"

    return {
        "doubled": doubled,
        "evens": evens,
        "product": product,
        "greet1": greet("Alice"),
        "greet2": greet("Bob", greeting="Hi"),
        "combine": combine(1, 2, 3, a=4, b=5),
        "slow_function": slow_function(),
    }


def error_handling_patterns():
    """Examples of common error handling patterns."""
    results = []

    # Basic try-except
    try:
        pass
    except ZeroDivisionError:
        results.append("Caught zero division error")

    # Try-except-else
    try:
        pass
    except ZeroDivisionError:
        results.append("Caught zero division error")
    else:
        results.append("No error occurred")

    # Try-except-finally
    try:
        pass
    except ZeroDivisionError:
        results.append("Caught zero division error")
    finally:
        results.append("This always runs")

    # Multiple exceptions
    try:
        # Could raise different exceptions
        int("not a number")
    except (ValueError, TypeError):
        results.append("Caught value or type error")

    # Exception with as clause
    try:
        with open("nonexistent_file.txt") as f:
            f.read()
    except FileNotFoundError as e:
        results.append(f"File error: {e!s}")

    # Context manager with try
    try:
        with open(__file__) as f:
            first_line = f.readline()
            results.append(f"First line: {first_line.strip()}")
    except Exception as e:
        results.append(f"Error: {e!s}")

    return results


def string_manipulation_patterns():
    """Examples of common string manipulation patterns."""

    # String formatting
    name = "Alice"
    age = 30
    formatted1 = f"{name} is {age} years old"
    formatted2 = f"{name} is {age} years old"
    formatted3 = "%s is %d years old" % (name, age)

    # String methods
    s = "  Hello, World!  "
    stripped = s.strip()
    lowered = s.lower()
    uppered = s.upper()
    replaced = s.replace("Hello", "Hi")

    # String splitting and joining
    words = "apple,banana,cherry".split(",")
    joined = "-".join(words)

    # Regular expressions
    text = "The quick brown fox jumps over the lazy dog"
    pattern = r"\b\w{5}\b"  # 5-letter words
    matches = re.findall(pattern, text)

    return {
        "formatted1": formatted1,
        "formatted2": formatted2,
        "formatted3": formatted3,
        "stripped": stripped,
        "lowered": lowered,
        "uppered": uppered,
        "replaced": replaced,
        "words": words,
        "joined": joined,
        "matches": matches,
    }


def file_operation_patterns():
    """Examples of common file operation patterns."""
    results = []

    # Writing to a file
    with open("test_output.txt", "w") as f:
        f.write("Hello, World!\n")
        f.write("This is a test file.\n")

    # Reading from a file
    with open("test_output.txt") as f:
        content = f.read()
        results.append(f"File content length: {len(content)}")

    # Reading line by line
    with open("test_output.txt") as f:
        for i, line in enumerate(f):
            results.append(f"Line {i + 1}: {line.strip()}")

    # File existence check
    if os.path.exists("test_output.txt"):
        results.append("File exists")

    # File operations with try-finally
    f = None
    try:
        f = open("test_output.txt")
        first_char = f.read(1)
        results.append(f"First character: {first_char}")
    finally:
        if f:
            f.close()

    # Clean up
    os.remove("test_output.txt")

    return results


def main():
    """Run all pattern examples and print results."""
    list_results = list_comprehension_examples()
    for key in list_results:
        pass

    for _result in control_flow_patterns():
        pass

    func_results = function_patterns()
    for key in func_results:
        if key != "slow_function":  # Skip printing the timing output
            pass

    for _result in error_handling_patterns():
        pass

    string_results = string_manipulation_patterns()
    for key in string_results:
        pass

    for _result in file_operation_patterns():
        pass


if __name__ == "__main__":
    main()
