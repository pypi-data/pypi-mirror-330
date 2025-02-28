from __future__ import annotations

__all__ = ["FastAPI"]

import asyncio
import inspect
from typing import Any

import uvicorn
from fastapi import APIRouter, Depends
from fastapi import FastAPI as BaseFastAPI
from fastapi import HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    SecurityScopes,
)
from starlette.middleware.cors import CORSMiddleware

from verse.core import (
    Component,
    Context,
    DataModel,
    Operation,
    OperationParser,
    Provider,
    Response,
)
from verse.core.exceptions import BaseError
from verse.core.spec import ComponentSpec, SpecBuilder

from .._models import APIInfo
from .._operation import APIOperation

app = None


class FastAPI(Provider):
    component: Component
    api_keys: list[str] | None
    host: str | None
    port: int | None
    reload: bool
    workers: int
    cors_origins: str | list[str] | None
    cors_methods: str | list[str] | None
    cors_headers: str | list[str] | None
    cors_credentials: bool | None
    nparams: dict[str, Any]

    _app: BaseFastAPI

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        reload: bool = False,
        workers: int = 1,
        cors_origins: str | list[str] | None = None,
        cors_methods: str | list[str] | None = "*",
        cors_headers: str | list[str] | None = "*",
        cors_credentials: bool | None = True,
        nparams: dict[str, Any] = dict(),
        **kwargs,
    ):
        """Initialize.

        Args:
            host:
                Host IP address.
            port:
                HTTP port.
            reload:
                A value indicating whether the app should be reloaded
                when any files are modified.
            workers:
                Number of uvicorn worker processes.
            cors_origins:
                Allowed origins for CORS.
                If None, CORS middleware is not enabled.
            cors_methods:
                Allowed methods for CORS.
                Defaults to *.
            cors_headers:
                Allowed headers for CORS.
                Defaults to *.
            cors_credentials:
                A value indicating whether credentials
                are allowed for CORS. Defaults to true.
            nparams:
                Native parameters to FastAPI and uvicorn client.
        """
        self.host = host
        self.port = port
        self.reload = reload
        self.workers = workers
        self.cors_origins = cors_origins
        self.cors_methods = cors_methods
        self.cors_headers = cors_headers
        self.cors_credentials = cors_credentials
        self.nparams = nparams
        self._app = BaseFastAPI(**self.nparams)

    def __run__(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        result = None
        op_parser = OperationParser(operation)
        if op_parser.op_equals(APIOperation.GET_INFO):
            result = self._get_info()
            return Response(result=result)
        else:
            api = GenericAPI(self.get_component().component)
            server = self._get_server(api)
            try:
                asyncio.run(server.serve())
            except asyncio.CancelledError:
                pass
            except KeyboardInterrupt:
                pass
        return Response(result=result)

    async def __arun__(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        result = None
        op_parser = OperationParser(operation)
        if op_parser.op_equals(APIOperation.GET_INFO):
            result = self._get_info()
        else:
            api = GenericAsyncAPI(self.get_component().component)
            server = self._get_server(api)
            try:
                await server.serve()
            except asyncio.CancelledError:
                pass
            except KeyboardInterrupt:
                pass
        return Response(result=result)

    def _get_server(self, api: BaseAPI) -> uvicorn.Server:
        dependencies = []
        if self.get_component().api_keys is not None:
            auth = Auth(self.get_component().api_keys)
            dependencies.append(Security(auth.authenticate))
        self._app.include_router(api.router, dependencies=dependencies)
        if self.cors_origins:
            allow_origins = (
                [self.cors_origins]
                if isinstance(self.cors_origins, str)
                else self.cors_origins
            )
            allow_methods = (
                [self.cors_methods]
                if isinstance(self.cors_methods, str)
                else self.cors_methods
            )
            allow_headers = (
                [self.cors_headers]
                if isinstance(self.cors_headers, str)
                else self.cors_headers
            )
            allow_credentials = self.cors_credentials
            self._app.add_middleware(
                CORSMiddleware,
                allow_origins=allow_origins,
                allow_credentials=allow_credentials,
                allow_methods=allow_methods,
                allow_headers=allow_headers,
            )
        if self.reload is False and self.workers == 1:
            config = uvicorn.Config(
                self._app,
                host=self.host or self.get_component().host,
                port=self.port or self.get_component().port,
                reload=self.reload,
                workers=self.workers,
            )
            server = uvicorn.Server(config)
            return server
        else:
            global app
            app = self._app
            config = uvicorn.Config(
                self._get_app_string(),
                host=self.host or self.get_component().host,
                port=self.port or self.get_component().port,
                reload=self.reload,
                workers=self.workers,
            )
            server = uvicorn.Server(config)
            return server

    def _get_app_string(self) -> str:
        module = inspect.getmodule(self)
        if module is not None:
            return f"{module.__name__}:app"
        raise ModuleNotFoundError("Module not found")

    def _get_info(self) -> APIInfo:
        return APIInfo(
            host=self.host or self.get_component().host,
            port=self.port or self.get_component().port,
        )


class BaseAPI:
    component: Component
    router: APIRouter


class Request(DataModel):
    operation: Operation | None = None
    context: Context | None = None


class GenericAPI(BaseAPI):
    def __init__(self, component: Component):
        self.component = component
        self.router = APIRouter()
        self.router.add_api_route("/__run__", self.run, methods=["POST"])
        self.router.add_api_route("/__spec__", self.spec, methods=["GET"])

    def run(self, request: Request) -> Any:
        """Run operation."""
        try:
            return self.component.__run__(
                operation=request.operation, context=request.context
            )
        except BaseError as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))

    async def spec(self) -> ComponentSpec:
        """Get component spec."""
        component_name = self.component._get_name()
        spec_builder = SpecBuilder()
        spec = spec_builder.build_component_spec(component_name=component_name)
        return spec


class GenericAsyncAPI(BaseAPI):
    def __init__(self, component: Component):
        self.component = component
        self.router = APIRouter()
        self.router.add_api_route("/__run__", self.run, methods=["POST"])
        self.router.add_api_route("/__spec__", self.spec, methods=["GET"])

    async def run(self, request: Request) -> Any:
        """Run operation."""
        try:
            return await self.component.__arun__(
                operation=request.operation,
                context=request.context,
            )
        except BaseError as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))

    async def spec(self) -> ComponentSpec:
        """Get component spec."""
        component_name = self.component._get_name()
        spec_builder = SpecBuilder()
        spec = spec_builder.build_component_spec(component_name=component_name)
        return spec


class Auth:
    api_keys: list[str]

    def __init__(self, api_keys: list[str]):
        self.api_keys = api_keys

    async def authenticate(
        self,
        security_scopes: SecurityScopes,
        token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer()),
    ) -> None:
        if token is not None and token.credentials in self.api_keys:
            return
        raise UnauthenticatedException()


class UnauthenticatedException(HTTPException):
    def __init__(self, detail: str = "Requires authentication"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
