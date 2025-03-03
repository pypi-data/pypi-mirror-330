from typing import List, Union
"""This module provides various mathematical functions including basic arithmetic, statistical calculations, and sorting algorithms. It is designed to work with lists of integers and floats, providing utility functions like mean, median, mode, variance, and standard deviation.

Example usage:
    >>> from math_test import mean, median
    >>> mean([1, 2, 3, 4, 5])
    3.0
    >>> median([1, 2, 3, 4, 5])
    3
"""


def _common_operations(numbers: List[Union[int, float]], number_type: str, start_number: int = 0) -> int | float:
    result = start_number
    for number in numbers:
        result = eval(f"result {number_type} {number}")
    return result


def sum(numbers: List[Union[int, float]]) -> int | float:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        int | float: The sum of the numbers.

    Examples:
        >>> sum([1, 2, 3])
        6
    """
    return _common_operations(numbers, "+")


def subtract(numbers: List[Union[int, float]]) -> int | float:
    """
    Calculates the difference of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        int | float: The result of the subtraction.

    Examples:
        >>> subtract([10, 5, 2])
        3
    """
    return _common_operations(numbers, "-")


def multiply(numbers: List[Union[int, float]]) -> int | float:
    """
    Calculates the product of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        int | float: The product of the numbers.

    Examples:
        >>> multiply([2, 3, 4])
        24
    """
    return _common_operations(numbers, "*", 1)


def divide(numbers: List[Union[int, float]]) -> float:
    """
    Calculates the division of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        float: The result of the division.

    Examples:
        >>> divide([100, 2, 5])
        10.0
    """
    return _common_operations(numbers, "/", 1)


def max(numbers: List[Union[int, float]]) -> int | float:
    """
    Finds the maximum number in a list.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        int | float: The maximum number.

    Examples:
        >>> max([1, 2, 3, 4, 5])
        5
    """
    result = numbers[0]
    for number in numbers:
        if number > result:
            result = number
    return result


def min(numbers: List[Union[int, float]]) -> int | float:
    """
    Finds the minimum number in a list.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        int | float: The minimum number.

    Examples:
        >>> min([1, 2, 3, 4, 5])
        1
    """
    result = numbers[0]
    for number in numbers:
        if number < result:
            result = number
    return result


def size(numbers: List[Union[int, float]]) -> int:
    """
    Returns the size (number of elements) of a list.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        int: The number of elements in the list.

    Examples:
        >>> size([1, 2, 3, 4])
        4
    """
    return sum(list(map(lambda x: 1, numbers)))


def sort(numbers: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Sorts a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        List[Union[int, float]]: Sorted list.

    Examples:
        >>> sort([3, 1, 4, 1, 5, 9, 2])
        [1, 1, 2, 3, 4, 5, 9]
    """
    if size(numbers) <= 1:
        return numbers
    pivot = numbers[size(numbers) // 2]
    left = [x for x in numbers if x < pivot]
    middle = [x for x in numbers if x == pivot]
    right = [x for x in numbers if x > pivot]
    return sort(left) + middle + sort(right)


def mean(numbers: List[Union[int, float]]) -> float:
    """
    Calculates the mean (average) of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        float: The mean of the numbers.

    Examples:
        >>> mean([1, 2, 3, 4, 5])
        3.0
    """
    return (sum(numbers) / size(numbers))


def median(numbers: List[Union[int, float]]) -> float:
    """
    Finds the median of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        List[Union[int, float]]: The mode(s) of the numbers.

    Examples:
        >>> mode([1, 2, 2, 3, 3, 3, 4, 5])
        [3]
    """
    data_sorted = sort(numbers)

    n = size(data_sorted)

    if n % 2 == 1:
        return data_sorted[n // 2]
    else:
        mid1 = data_sorted[n // 2 - 1]
        mid2 = data_sorted[n // 2]
        return (mid1 + mid2) / 2


def var(numbers: List[Union[int, float]]) -> float:
    """
    Calculates the variance of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        float: The variance of the numbers.

    Examples:
        >>> var([1, 2, 3, 4, 5])
        2.0
    """
    return sum((x - mean(numbers)) ** 2 for x in numbers) / size(numbers)


def std(numbers: List[Union[int, float]]) -> float:
    """
    Calculates the standard deviation of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        float: The standard deviation of the numbers.

    Examples:
        >>> std([1, 2, 3, 4, 5])
        1.4142135623730951
    """
    return var(numbers) ** 0.5


def mode(numbers: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Calculate the mode(s) of a list of numbers.

    Args:
        numbers (List[Union[int, float]]): List of numbers.

    Returns:
        List[Union[int, float]]: A list containing the mode(s) of the numbers.

    Examples:
        >>> mode([1, 2, 2, 3, 4, 4, 4, 5])
        [4]
        >>> mode([1, 1, 2, 2, 3, 3])
        [1, 2, 3]
    """
    freq = {}
    for number in numbers:
        freq[number] = freq.get(number, 0) + 1

    return [key for key, value in freq.items if value == max(list(freq.values()))]
