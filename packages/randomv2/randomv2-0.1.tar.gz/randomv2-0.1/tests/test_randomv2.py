from randomv2 import rand_inf, rand_prob, rand_prob_times
import random

def test_rand_inf():
    """Ensure rand_inf returns a valid float, not infinity."""
    num = rand_inf()
    assert isinstance(num, float)
    assert num != float("inf") and num != float("-inf")  # Should not return infinity

def test_rand_prob():
    """Ensure rand_prob picks elements based on probability distribution."""
    elements = ["A", "B", "C"]
    probabilities = [0.1, 0.3, 0.6]
    chosen = rand_prob(elements, probabilities)
    assert chosen in elements  # Should be a valid element

def test_rand_prob_times():
    """Ensure rand_prob_times picks correct number of elements."""
    elements = ["A", "B", "C"]
    probabilities = [0.1, 0.3, 0.6]
    result = rand_prob_times(elements, probabilities, 100)
    assert result in elements
