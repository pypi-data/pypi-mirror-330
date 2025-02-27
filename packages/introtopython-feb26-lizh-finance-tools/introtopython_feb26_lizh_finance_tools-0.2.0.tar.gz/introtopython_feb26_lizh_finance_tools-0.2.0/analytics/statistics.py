def moving_average(data, period):
    return sum(data[-period:]) / period


def weighted_moving_average(data, period):
    weights = list(range(1, period + 1))
    weighted_sum = sum(data[-period:] * weights)
    return weighted_sum / sum(weights)