
from typing import List


def intersectValues(a: List[any], b: List[any]) -> List[any]:
    """
    Get values that intersect in lists.
    Example:
        c = intersectValues(["a", "b", "c"], ["x", "c", "a"])
        # c = ["a", "c"]

    Args:
        a (List[any]): First list to compare.
        b (List[any]): Second list to compare.

    Returns:
        List[any]: Intersecting values in a and b.
    """
    
    return [v for v in a if v in b]
    
def intersectIndices(a: List[any], b: List[any]) -> List[int]:
    """
    Get indices of list a for values that intersect with list b.
    Example:
        c = intersectValues(["a", "b", "c"], ["x", "c", "z"])
        # c = [2]

    Args:
        a (List[any]): First list to compare.
        b (List[any]): Second list to compare.

    Returns:
        List[int]: Indices of list a of values intersecting values in list b.
    """
    
    return [i for i, v in enumerate(a) if v in b]