"""
Модуль отвечающий за хранение контекстных переменных

Более подробно про методы работы https://docs.python.org/3/library/html
"""
import typing
from contextvars import ContextVar

app = ContextVar('app')

if typing.TYPE_CHECKING:
    import starlette.requests

# Информация по запросу
request: ContextVar['starlette.requests.Request'] = ContextVar('request')
