import typing as t


def contains_nested_sequence(values: t.Any) -> bool:
    """
    Check if the given value contains a nested sequence (list or tuple).

    Parameters
    ----------
    values : Any
        The value to be checked for nested sequences.

    Returns
    -------
    bool
        True if the value contains a nested sequence, False otherwise.

    Examples
    --------
    >>> contains_nested_sequence([1, 2, (3, 4)])
    True
    >>> contains_nested_sequence([1, 2, 3])
    False
    >>> contains_nested_sequence((1, 2, [3, 4]))
    True
    >>> contains_nested_sequence((1, 2, 3))
    False
    """
    if isinstance(values, tuple) or isinstance(values, list):
        for value in values:
            if isinstance(value, tuple) or isinstance(value, list):
                return True
            else:
                return False
    else:
        return False
