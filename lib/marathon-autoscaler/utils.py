
def clamp(num, smallest, largest):
    """
    Propose a number and a range (smallest, largest) to receive a number that is clamped within that range.
    :param num: a number to propose
    :param smallest: minimum of range
    :param largest: maximum of range
    :return: number in range
    """
    return max(smallest, min(num, largest))


def list_get(lst, index, default=None):
    """
    A safety mechanism for accessing uncharted indexes of a list. Always remember: safety first!
    :param lst: list
    :param index: int
    :param default: A default value
    :return: Value of list at index -or- default value
    """
    assert type(lst) == list, "Requires a list type"
    return_value = default
    try:
        return_value = lst[index]
    except IndexError:
        pass

    return return_value
