"""Top-level init."""

from importlib.metadata import version

from bfb_delivery.api import (
    build_routes_from_chunked,
    combine_route_tables,
    create_manifests,
    create_manifests_from_circuit,
    format_combined_routes,
    split_chunked_route,
)

try:
    __version__: str = version(__name__)
except Exception:
    __version__ = "unknown"

del version
