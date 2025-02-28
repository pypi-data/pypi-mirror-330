from verse.core import Component, Response, operation

from ._models import APIInfo


class API(Component):
    component: Component
    api_keys: list[str] | None
    host: str
    port: int

    def __init__(
        self,
        component: Component,
        api_keys: list[str] | None = None,
        host: str = "127.0.0.1",
        port: int = 8080,
        **kwargs,
    ):
        """Initialize.

        Args:
            component:
                Component to host as API.
            api_keys:
                API keys for authenticated access.
            host:
                Host IP address.
            port:
                HTTP port.
        """
        self.component = component
        self.api_keys = api_keys
        self.host = host
        self.port = port
        super().__init__(**kwargs)

    @operation()
    def run(self) -> Response[None]:
        """Run the API."""
        ...

    @operation()
    def get_info(self) -> Response[APIInfo]:
        """Get API Info"""
        ...
