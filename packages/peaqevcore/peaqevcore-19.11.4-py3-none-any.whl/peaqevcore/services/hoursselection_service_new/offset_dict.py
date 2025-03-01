from datetime import date, timedelta
from .const import TODAY, TOMORROW
from statistics import mean, stdev


def get_offset_dict(offset_dict, dt_now) -> dict:
    return {
        TODAY: offset_dict.get(dt_now.date(), {}),
        TOMORROW: offset_dict.get(dt_now.date() + timedelta(days=1), {}),
    }


def set_offset_dict(prices: list[float], day: date, min_price: float) -> dict:
    ret = {}
    _len = len(prices)
    today: list = []
    tomorrow: list = []
    match _len:
        case 23 | 24 | 25 | 92 | 96 | 100:
            today = prices
        case 47 | 48 | 49 | 188 | 192 | 196:
            today = prices[: len(prices) // 2]
            tomorrow = prices[len(prices) // 2 : :]
    ret[day] = _deviation_from_mean(today, prices, min_price)
    ret[day + timedelta(days=1)] = _deviation_from_mean(tomorrow, prices, min_price)
    return ret


def _deviation_from_mean(prices: list[float], checker: list[float], min_price:float) -> dict[int, float]:
    if not len(prices):
        return {}
    avg = mean(checker)
    devi = stdev(prices)
    deviation_dict = {}
    for i, num in enumerate(prices):
        deviation = (num - avg) / devi
        if devi < 1:
            deviation *= 0.5
        setval = 0
        if num <= min_price:
            setval = min(round(deviation, 2),0)
        elif num <= min_price * 2:
            setval = deviation - 1 if deviation > 1 else deviation
        else:
            setval = round(deviation, 2)
        deviation_dict[i] = setval
    return deviation_dict
