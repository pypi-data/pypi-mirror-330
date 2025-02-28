from verse.core import DataModel


class APIInfo(DataModel):
    """API Info."""

    host: str
    """Host address."""

    port: int | None
    """Host port."""

    ssl: bool = False
    """SSL enabled."""
