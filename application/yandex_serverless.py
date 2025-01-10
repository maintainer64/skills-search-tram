import asyncio

from application.container.container import DI
from application.handlers.states import Event


def handler(event: Event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    return asyncio.run(DI().yandex_handler().handler(event=event, context=context))
