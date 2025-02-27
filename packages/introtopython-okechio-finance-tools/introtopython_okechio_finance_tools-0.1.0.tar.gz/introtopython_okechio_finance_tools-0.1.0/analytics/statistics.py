def moving_average(data, period):
    return sum(data[-period:]) / period