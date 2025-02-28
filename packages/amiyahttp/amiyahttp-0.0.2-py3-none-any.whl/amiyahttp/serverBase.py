import inspect
import asyncio
import uvicorn

from dataclasses import dataclass, field
from typing import List, Callable, Optional, Coroutine, Any

default_logging_options = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': '%(client_addr)s - %(request_line)s %(status_code)s',
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(asctime)s ｜ %(levelname)s ｜ %(message)s',
        },
    },
    'handlers': {
        'access': {
            'class': 'logging.StreamHandler',
            'formatter': 'access',
        },
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'uvicorn': {'handlers': ['default'], 'level': 'INFO'},
        'uvicorn.error': {'level': 'INFO'},
        'uvicorn.access': {'handlers': ['access'], 'level': 'INFO', 'propagate': False},
    },
}


@dataclass
class ServerConfig:
    title: str = 'Amiya HTTP'
    description: str = '对 FastAPI 进行二次封装的简易 HTTP Web 服务 SDK'

    api_prefix: str = '/api'

    fastapi_options: Optional[dict] = None
    uvicorn_options: Optional[dict] = None
    logging_options: dict = field(default_factory=lambda: default_logging_options)

    get_user_password: Optional[Callable[[str], Coroutine[Any, Any, str]]] = None


class ServerEventHandler:
    on_shutdown: List[Callable] = []


class ServerABCClass:
    def __init__(self):
        self.server: Optional[uvicorn.Server] = None

    async def serve(self):
        if self.server:
            await self.server.serve()


class ServerMeta(type):
    instances: List[ServerABCClass] = []
    shutdown_lock = False

    def __call__(cls, *args, **kwargs):
        inst = super().__call__(*args, **kwargs)

        cls.instances.append(inst)

        return inst

    def shutdown_all(cls, instance: ServerABCClass):
        if not cls.shutdown_lock:
            cls.shutdown_lock = True

            for inst in cls.instances:
                if inst != instance:
                    inst.server.should_exit = True

            for action in ServerEventHandler.on_shutdown:
                if inspect.iscoroutinefunction(action):
                    asyncio.create_task(action())
                else:
                    action()
