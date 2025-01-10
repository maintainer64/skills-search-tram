import random
from typing import Any

from application.clients.geocoder.client import geocoder_search
from .intents import intents_geo, intents_confirm, intents_reject, intents_int, intents_transport
from .route_ekb_service import ekb_transport_service
from .states import Event, ApplicationState, States, session_is_new, get_text_from_event, get_application_state


def hello_start(event: Event, state: ApplicationState) -> dict[str, Any] | None:
    # Рассказывает про навык, как им пользоваться
    # Предлагает сразу выбрать домашний адрес
    if not session_is_new(event):
        return None
    text = get_text_from_event(event)
    if text:
        return None
    complete_address = state.geo_lat and state.geo_lon and state.geo_address and state.state == States.COMPLETE_ADDRESS
    if complete_address:
        return None
    state.state = States.SET_ADDRESS
    choices = (
        'Добро пожаловать в навык "Где трамвай"! Давайте начнем с выбора вашего домашнего адреса.',
        "Готовы отправиться на поиски транспорта? Для начала выберите ваш адрес.",
        "Прежде чем отправиться путешествовать на транспорте, укажите свой домашний адрес.",
        "Начнем наш поиск трамвая с указания вашего домашнего адреса. Другие шаги расскажу после.",
        "Перед началом поиска трамвая назови свой домашний адрес для удобства использования навыка.",
        "Хотите быстро найти трамвай? Начнем с выбора вашего местоположения. Назови полный адрес.",
    )
    return {
        "response": {
            "text": random.choice(choices),
            "end_session": False,
        },
        "application_state": state.dict(),
    }


def search_transport(event: Event, state: ApplicationState) -> dict[str, Any] | None:
    if state.state != States.COMPLETE_ADDRESS:
        return None
    if not state.geo_lon or not state.geo_lat:
        return None
    transport_type = intents_transport(event)
    transport_number = intents_int(event)
    if len(transport_number) != 1:
        return None
    service = ekb_transport_service(
        transport_number=transport_number[0],
        transport_type=transport_type,
        geo_lat=state.geo_lat,
        geo_lon=state.geo_lon,
    )
    return {
        "response": {
            "text": service.text(),
            "end_session": True,
        },
        "application_state": state.dict(),
    }


def hello_again(event: Event, state: ApplicationState) -> dict[str, Any] | None:
    # Рассказывает про навык, как им пользоваться
    # Для изменения адреса начальной точки маршрута, скажите - "сменить адрес"
    if not session_is_new(event):
        return None
    text = get_text_from_event(event)
    if text:
        return None
    if state.state != States.COMPLETE_ADDRESS:
        return None
    choices = (
        "Укажите номер трамвая, троллейбуса или автобуса, и я сообщу вам время его прибытия на ближайшую остановку. "
        'Просто скажите "сменить адрес", если нужно изменить место отправления.',
        "Скажите номер автобуса, трамвая или троллейбуса, и я подскажу, когда он прибудет на ближайшую остановку. "
        'Если хотите изменить адрес отправления, просто скажите "сменить адрес".',
        "Назовите номер трамвая, троллейбуса или автобуса, и я сообщу, когда он прибудет на ближайшую остановку. "
        'Просто произнесите "сменить адрес", чтобы изменить место старта.',
        "Если укажете номер трамвая, троллейбуса или автобуса, я расскажу, когда он прибудет на ближайшую остановку. "
        'Просто скажите "сменить адрес", чтобы изменить адрес отправления.',
        "Хотите узнать время прибытия трамвая, троллейбуса или автобуса на ближайшую остановку? Просто назовите номер, "
        'и я подскажу. Для смены адреса, скажите "сменить адрес".',
        "Назовите номер автобуса, трамвая или троллейбуса, и я скажу, когда он прибудет на ближайшую остановку. "
        'Просто произнесите "сменить адрес", чтобы изменить место отправки.',
        "Укажите номер автобуса, трамвая или троллейбуса, и я сообщу вам время его прибытия на ближайшую остановку. "
        'Просто скажите "сменить адрес", если необходимо изменить адрес начала маршрута.',
        "Назовите номер трамвая, троллейбуса или автобуса, и я скажу, когда он прибудет на ближайшую остановку. "
        'Произнесите "сменить адрес", чтобы изменить место отправления.',
        "Если укажете номер трамвая, троллейбуса или автобуса, я подскажу, когда он прибудет на ближайшую остановку. "
        'Просто скажите "сменить адрес", чтобы изменить адрес отправления.',
        "Хотите узнать время прибытия автобуса, трамвая или троллейбуса на ближайшую остановку? Просто назовите номер, "
        'и я сообщу вам. Для смены адреса, просто скажите "сменить адрес".',
    )
    return {
        "response": {
            "text": random.choice(choices),
            "end_session": False,
            "buttons": [
                {"title": "Сменить адрес", "hide": True},
                {"title": "Текущий адрес", "hide": True},
            ],
        },
        "application_state": state.dict(),
    }


def change_address(event: Event, state: ApplicationState) -> dict[str, Any] | None:
    # Начинает процедуру изменения адреса
    text = get_text_from_event(event)
    intents = {
        "смена адреса",
        "сменить адрес",
        "поменяй адрес",
        "поменять адрес",
        "измени адрес",
        "изменить адрес",
    }
    if text is None:
        return None
    for intent in intents:
        if intent in text.lower() or text.lower() in intent:
            break
    else:
        return None
    state.state = States.SET_ADDRESS
    state.geo_lat = 0
    state.geo_lon = 0
    choices = (
        "Пожалуйста, укажите полный адрес, включая город, улицу и номер дома.",
        "Назовите мне полный адрес, состоящий из города, улицы и номера дома, чтобы помочь вам с маршрутом.",
        "Жду ваш полный адрес, включающий город, улицу и дом, чтобы начать планирование маршрута.",
        "Укажите мне ваш полный адрес, чтобы определить оптимальный маршрут. Не забудьте включить город, "
        "улицу и номер дома.",
        "Если вы укажете мне полный адрес – город, улицу и дом, я смогу помочь с маршрутом.",
        "Пожалуйста, сообщите мне полный адрес с указанием города, улицы и номера дома для подробного "
        "планирования маршрута.",
        "Жду вашего полного адреса: город, улица, номер дома. С этой информацией я смогу помочь в поиске "
        "лучшего маршрута.",
    )
    return {
        "response": {"text": random.choice(choices), "end_session": False},
        "application_state": state.dict(),
    }


def current_address(event: Event, state: ApplicationState) -> dict[str, Any] | None:
    # Показывает текущий адрес
    if state.state != States.COMPLETE_ADDRESS:
        return None
    text = get_text_from_event(event)
    intents = {
        "текущий адрес",
        "подскажи адрес",
        "какой мой адрес",
        "мой адрес",
        "мой адрес",
        "где я",
        "где я нахожусь",
    }
    if text is None:
        return None
    for intent in intents:
        if intent in text.lower() or text.lower() in intent:
            break
    else:
        return None
    if not state.geo_address:
        return None
    return {
        "response": {
            "text": f"Ваш текущий адрес: {str(state.geo_address)}. Вы можете его изменить. "
            f'Просто скажите "Поменяй адрес"',
            "end_session": False,
            "buttons": [
                {"title": "Сменить адрес", "hide": True},
                {"title": "Текущий адрес", "hide": True},
            ],
        },
    }


def set_address(event: Event, state: ApplicationState) -> dict[str, Any] | None:
    # Устанавливает новый адрес
    if state.state != States.SET_ADDRESS:
        return None
    geo_list = intents_geo(event)
    if not geo_list:
        return {
            "response": {
                "text": "Не могу найти адрес на карте. Назовите полный адрес. Город, улица, дом",
                "end_session": False,
            },
        }
    geo = geo_list[0]
    text = get_text_from_event(event)
    geo_response = geocoder_search(address=str(geo))
    geo_response = geocoder_search(address=text) if not str(geo_response) and text else geo_response
    if not str(geo_response):
        return {
            "response": {"text": "Я не расслышала. Назовите полный адрес. Город, улица, дом", "end_session": False},
        }
    state.geo_lon = geo_response.lng
    state.geo_lat = geo_response.lat
    state.geo_address = str(geo_response)
    state.state = States.SET_ADDRESS
    return {
        "response": {
            "text": f"Нашла подходящий адрес. {str(geo_response)}. Всё верно?",
            "end_session": False,
            "buttons": [
                {"title": "Да", "hide": True},
                {"title": "Нет", "hide": True},
            ],
        },
        "application_state": state.dict(),
    }


def confirm_address(event: Event, state: ApplicationState) -> dict[str, Any] | None:
    # Подтверждает текущий не подтвержденный адрес
    if state.state != States.SET_ADDRESS:
        return None
    address_filled = state.geo_address and state.geo_lat and state.geo_lon
    if not address_filled:
        return None
    if intents_reject(event):
        state.geo_address = None
        state.geo_lat = None
        state.geo_lon = None
        state.state = States.SET_ADDRESS
        choice = (
            "Поняла, давайте выберем другой адрес для продолжения. Укажите город, улицу и номер дома, пожалуйста.",
            "Приняла, давайте перейдем к выбору другого адреса. Назовите город, улицу и номер дома новой локации.",
            "Окей, давайте сменим адрес. Назовите город, улицу и номер дома для новой точки назначения.",
            "Конечно, давайте переместимся к другому адресу. Укажите мне город, улицу и номер дома для новой локации.",
            "Понятно, давайте выберем другой адрес для вас. Пожалуйста, укажите город, улицу и номер дома новой точки.",
            "Ага, давайте сделаем это! Укажите новый адрес, состоящий из города, улицы и номера дома.",
            "Согласна, давайте выберем новый адрес. Назовите мне город, "
            "улицу и номер дома для следующей точки назначения.",
            "Договорились, давайте выберем другой адрес для маршрута. "
            "Укажите город, улицу и номер дома для новой локации.",
            "Отлично, давайте перейдем к другому адресу. "
            "Назовите город, улицу и номер дома новой точки для планирования маршрута.",
            "Принимаю, давайте выберем другую точку назначения. "
            "Прошу назвать город, улицу и номер дома для нового адреса.",
        )
        return {
            "response": {
                "text": random.choice(choice),
                "end_session": False,
            },
            "application_state": state.dict(),
        }
    if intents_confirm(event):
        state.state = States.COMPLETE_ADDRESS
        choice = (
            "Отлично! Теперь я могу предоставлять информацию о транспорте поблизости от вашей текущей точки.",
            "Великолепно! Теперь я в курсе событий и могу помочь с информацией о транспорте рядом с вами.",
            "Прекрасно! Теперь я готова дать вам советы о транспорте поблизости от вашей текущей локации.",
            "Замечательно! Теперь я имею доступ к информации о транспорте вблизи вас и готова поделиться этим с вами.",
            "Превосходно! Теперь я могу помогать вам советами относительно общественного транспорта рядом с вами.",
            "Отлично! Теперь я могу быть полезной, предоставляя информацию о транспорте, "
            "находящемся поблизости от вас.",
            "Замечательно! Теперь у меня есть ресурсы для предоставления вам информации о транспорте в вашем районе.",
            "Великолепно! Теперь я готова дать вам советы и информацию о транспорте, находящемся рядом с вами.",
            "Прекрасно! Теперь я могу помочь вам с информацией о транспорте, находящемся около вашей позиции.",
            "Это здорово! Теперь я могу помогать вам с вопросами о транспорте поблизости от вас.",
        )
        return {
            "response": {
                "text": random.choice(choice),
                "end_session": False,
                "buttons": [
                    {"title": "Сменить адрес", "hide": True},
                    {"title": "Текущий адрес", "hide": True},
                ],
            },
            "application_state": state.dict(),
        }
    return None


FUNCTIONS = (
    hello_start,
    search_transport,
    hello_again,
    current_address,
    change_address,
    confirm_address,
    set_address,
)


def handler(event: Event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    state = get_application_state(event)
    choice = (
        "Я вас не поняла. Уточните пожалуйста Ваш запрос",
        "Извините. Я вас не поняла. Уточните пожалуйста Ваш запрос",
        "Прошу прощения. Уточните пожалуйста Ваш запрос",
    )
    response = {
        "version": event["version"],
        "session": event["session"],
        "response": {
            "text": random.choice(choice),
            "end_session": False,
        },
        "application_state": state.dict(),
    }
    for func in FUNCTIONS:
        result = func(event, state)
        if result is not None:
            return {**response, **result}
    return response
