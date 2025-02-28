from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.staticfiles import StaticFiles

from amiyahttp.utils import snake_case_to_pascal_case, create_dir
from amiyahttp.serverBase import *
from amiyahttp.oauth2 import *


class HttpServer(ServerABCClass, metaclass=ServerMeta):
    def __init__(self, host: str, port: int, config: ServerConfig = ServerConfig()):
        super().__init__()

        app = FastAPI(title=config.title, description=config.description, **(config.fastapi_options or {}))

        self.app = app
        self.host = host
        self.port = port
        self.config = config

        self.router = InferringRouter()
        self.controller = cbv(self.router)

        self.__routes = []

        @app.post(f'{config.api_prefix}/token')
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            if not self.config.get_user_password:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot get user password')

            user_password = await self.config.get_user_password(form_data.username)
            if not user_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Cannot get user password by username: {form_data.username}',
                )

            if not authenticate_user(form_data.password, user_password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={'sub': form_data.username}, expires_delta=access_token_expires)
            return self.response(
                extend={
                    'access_token': access_token,
                    'token_type': 'bearer',
                }
            )

        @app.on_event('shutdown')
        async def on_shutdown():
            HttpServer.shutdown_all(self)

        @app.exception_handler(HTTPException)
        async def on_exception(request: Request, exc: HTTPException):
            return JSONResponse(
                self.response(code=exc.status_code, message=exc.detail),
                status_code=exc.status_code,
            )

        @app.exception_handler(RequestValidationError)
        async def on_exception(request: Request, exc: RequestValidationError):
            messages = []
            for item in exc.errors():
                messages.append(item.get('loc')[1] + ': ' + item.get('msg'))

            return JSONResponse(
                self.response(code=422, message=';'.join(messages), result=exc.errors()),
                status_code=422,
            )

    @property
    def routes(self):
        return self.__routes

    def route(self, router_path: Optional[str] = None, method: str = 'post', **kwargs):
        def decorator(fn):
            nonlocal router_path

            path = fn.__qualname__.split('.')
            c_name = snake_case_to_pascal_case(path[0][0].lower() + path[0][1:])

            if not router_path:
                router_path = f'{self.config.api_prefix}/{c_name}'
                if len(path) > 1:
                    router_path += f'/{snake_case_to_pascal_case(path[1])}'

            arguments = {'path': router_path, 'tags': [c_name.title()] if len(path) > 1 else ['None'], **kwargs}

            router_builder = getattr(self.router, method)
            router = router_builder(**arguments)

            self.__routes.append(router_path)

            return router(fn)

        return decorator

    def add_static_folder(self, path: str, directory: str, **kwargs):
        create_dir(directory)
        self.app.mount(path, StaticFiles(directory=directory, **kwargs), name=directory)

    def set_index_html(self, directory: str, path: str = '/'):
        templates = Jinja2Templates(directory=directory)

        @self.app.get(path)
        async def read_root(request: Request):
            return templates.TemplateResponse('index.html', {'request': request})

    async def serve(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_methods=['*'],
            allow_headers=['*'],
            allow_credentials=True,
        )
        self.app.include_router(self.router)

        self.server = uvicorn.Server(
            config=uvicorn.Config(
                self.app,
                host=self.host,
                port=self.port,
                loop='asyncio',
                log_config=self.config.logging_options,
                **(self.config.uvicorn_options or {}),
            )
        )

        await super().serve()

    @staticmethod
    def response(
        result: Any = None,
        code: int = 200,
        message: str = '',
        extend: Optional[dict] = None,
    ):
        return {
            'code': code,
            'result': result,
            'message': message,
            **(extend or {}),
        }
