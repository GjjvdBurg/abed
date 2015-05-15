"""
Functions for generating fractional ranks

"""

def get_ranks(x):
    """
        Get ranks for a vector

        >>> x = [7, 0.1, 0.5, 0.1, 10, 100, 200]
        >>> get_ranks(x)
        [4.0, 1.5, 3.0, 1.5, 5.0, 6.0, 7.0]
    """
    l = len(x)
    r = 1
    ranks = [0]*l
    while not all([k is None for k in x]):
        m = min([k for k in x if not k is None])
        idx = [1 if k == m else 0 for k in x]
        s = sum(idx)
        ranks = [r + (s-1)/2.0 if idx[k] else ranks[k] for k in range(l)]
        r += s
        x = [None if idx[k] else x[k] for k in range(l)]
    return ranks


