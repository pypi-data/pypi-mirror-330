import random


def rand_inf():
    '''Picks a number from a very large negative to a very large positive range, avoiding infinity.'''
    return random.uniform(-1e307, 1e307)  # Reduced the range to avoid overflow


def rand_prob(list_ele, list_prob, n=1):
    """Returns 'n' random elements from list_ele based on list_prob."""
    result = random.choices(list_ele, weights=list_prob, k=n)
    return result[0] if n == 1 else result  # Return a single element if n=1



def rand_prob_times(list_ele, list_prob, n=1):
    for i in range(n):
        result = random.choices(list_ele, list_prob, k=1)[0]
        return result


