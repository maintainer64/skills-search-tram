import logging

logger = logging.getLogger(__name__)


def language_minutes(minutes: int) -> str:
    """
    Передаёт верную форму слова `через N мин`
    :param minutes: Параметр минут
    :return:
    """
    assert 0 <= minutes <= 60, "Неверное использование окончания минут"
    if minutes in {1, 21, 31, 41, 51}:
        return "минуту"
    if minutes in {2, 22, 32, 42, 52, 3, 23, 33, 43, 53, 4, 24, 34, 44, 54}:
        return "минуты"
    return "минут"


def language_hours(hours: int) -> str:
    """
    Передаёт верную форму слова `через N час`
    :param hours: Параметр часов
    :return:
    """
    assert 0 <= hours <= 23, "Неверное использование окончания часов"
    if hours in {1, 21}:
        return "час"
    if hours in {2, 22, 3, 23, 4, 24}:
        return "часа"
    return "часов"
