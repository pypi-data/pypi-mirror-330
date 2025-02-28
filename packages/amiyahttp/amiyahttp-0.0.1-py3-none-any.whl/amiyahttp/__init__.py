from typing import Any
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.staticfiles import StaticFiles

from amiyahttp.utils import snake_case_to_pascal_case, create_dir
from amiyahttp.serverBase import *


class HttpServer(ServerABCClass, metaclass=ServerMeta):
    def __init__(
        self,
        host: str,
        port: int,
        title: str = 'Amiya HTTP',
        description: str = '对 FastAPI 进行二次封装的简易 HTTP Web 服务 SDK',
        api_prefix: str = '/api',
        fastapi_options: Optional[dict] = None,
        uvicorn_options: Optional[dict] = None,
        logging_options: dict = default_logging_options,
    ):
        super().__init__()

        self.app = FastAPI(title=title, description=description, **(fastapi_options or {}))

        self.host = host
        self.port = port
        self.api_prefix = api_prefix
        self.uvicorn_options = uvicorn_options
        self.logging_options = logging_options

        self.router = InferringRouter()
        self.controller = cbv(self.router)

        self.__routes = []
        self.__allow_path = []
        self.__static_folders = []

        @self.app.middleware('http')
        async def interceptor(request: Request, call_next: Callable):
            path = request.scope['path']

            if path not in self.__allow_path and path.startswith(api_prefix):
                return Response('Unauthorized!', status_code=401)

            return await call_next(request)

        @self.app.on_event('shutdown')
        async def on_shutdown():
            HttpServer.shutdown_all(self)

        @self.app.exception_handler(HTTPException)
        async def on_exception(request: Request, exc: HTTPException):
            return JSONResponse(
                self.response(code=exc.status_code, message=exc.detail),
                status_code=exc.status_code,
            )

        @self.app.exception_handler(RequestValidationError)
        async def on_exception(request: Request, exc: RequestValidationError):
            messages = []
            for item in exc.errors():
                messages.append(item.get('loc')[1] + ': ' + item.get('msg'))

            return JSONResponse(
                self.response(code=422, message=';'.join(messages), result=exc.errors()),
                status_code=422,
            )

    def set_allow_path(self, paths: list):
        self.__allow_path += paths

    def __load_server(self, options: dict):
        return uvicorn.Server(
            config=uvicorn.Config(
                self.app,
                loop='asyncio',
                log_config=self.logging_options,
                **options,
            )
        )

    def route(
        self,
        router_path: Optional[str] = None,
        method: str = 'post',
        is_api: bool = True,
        allow_unauthorized: bool = False,
        **kwargs,
    ):
        def decorator(fn):
            nonlocal router_path

            path = fn.__qualname__.split('.')
            c_name = snake_case_to_pascal_case(path[0][0].lower() + path[0][1:])

            if not router_path:
                router_path = f'/{c_name}'
                if is_api:
                    router_path = self.api_prefix + router_path
                if len(path) > 1:
                    router_path += f'/{snake_case_to_pascal_case(path[1])}'

            arguments = {'path': router_path, 'tags': [c_name.title()] if len(path) > 1 else ['Alone'], **kwargs}

            router_builder = getattr(self.router, method)
            router = router_builder(**arguments)

            self.__routes.append(router_path)
            if allow_unauthorized:
                self.__allow_path.append(router_path)

            return router(fn)

        return decorator

    def add_static_folder(self, path: str, directory: str, **kwargs):
        create_dir(directory)
        self.app.mount(path, StaticFiles(directory=directory, **kwargs), name=directory)
        self.__static_folders.append('/' + directory)

    def set_index_html(self, directory: str, path: str = '/'):
        templates = Jinja2Templates(directory=directory)

        @self.app.get(path)
        async def read_root(request: Request):
            return templates.TemplateResponse('index.html', {'request': request})

    @staticmethod
    def response(
        result: Any = None,
        code: int = 200,
        message: str = 'ok',
    ):
        return {
            'code': code,
            'result': result,
            'message': message,
            'type': 'success' if code == 200 else 'error',
        }

    async def serve(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_methods=['*'],
            allow_headers=['*'],
            allow_credentials=True,
        )
        self.app.include_router(self.router)

        self.server = self.__load_server(
            options={
                'host': self.host,
                'port': self.port,
                **(self.uvicorn_options or {}),
            }
        )

        await super().serve()
