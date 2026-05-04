"""
Opt-in correlation handle that tags every outbound gRPC request with a session id.

Use [`tracing_session`][rerun._tracing_session.tracing_session] when you want to
attach a single, copy-pasteable identifier to a block of catalog calls so support
can look them up in distributed tracing.

```python
from rerun import tracing_session

with tracing_session():
    dataset.scan(...).read_all()
# → INFO message printed at scope entry: "rerun tracing session started: rs_8f3a91e2"
```

The implementation is a thin Python wrapper around a Rust-side `ContextVar`.
The Rust gRPC client reads the variable on every outbound request and merges
`rerun_session_id=<id>` into the W3C `tracestate` header. The Rerun Data Platform
records it as a span attribute, queryable in Tempo as
`{ .rerun_session_id = "…" }`.

This module is private — public re-export lives in `rerun.__init__`.
"""

from __future__ import annotations

import contextlib
import logging
import secrets
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger("rerun")

_SESSION_ID_PREFIX = "rs_"
_SESSION_ID_HEX_LEN = 8


def _generate_session_id() -> str:
    """Return a fresh session id of the form `rs_<8 lowercase hex digits>`."""
    return f"{_SESSION_ID_PREFIX}{secrets.token_hex(_SESSION_ID_HEX_LEN // 2)}"


def _is_valid_session_id(sid: str) -> bool:
    """Mirror of `re_perf_telemetry::is_valid_rerun_session_id`."""
    if not sid.startswith(_SESSION_ID_PREFIX):
        return False
    rest = sid[len(_SESSION_ID_PREFIX) :]
    return len(rest) == _SESSION_ID_HEX_LEN and all(c in "0123456789abcdef" for c in rest)


@contextlib.contextmanager
def tracing_session() -> Iterator[str]:
    """
    Tag every gRPC request inside the `with` block with a fresh session id.

    The id is logged to the `rerun` logger at INFO level the moment the scope is
    entered, so it stays visible even if the workflow crashes or hangs before
    completing. Send the logged id to support and they can query
    `{ .rerun_session_id = "<id>" }` in Tempo to surface every related request.

    The id is also yielded as the `as` target for programmatic access — handy
    for tests or integration code, but not the main customer-facing way to
    retrieve it.

    The session id is propagated through the W3C `tracestate` header. When you
    later opt into exporting client-side traces (by setting an OTLP endpoint)
    those exported spans automatically carry the same id, so the client→server
    trace tree stays correlated end-to-end.

    When the rerun telemetry stack is not active (typically because
    `TELEMETRY_ENABLED=true` was not set before importing rerun), the context
    manager logs a warning, yields the empty string, and proceeds as a no-op.
    Catalog calls inside the block are not tagged in this case.

    Examples
    --------
    ```python
    import rerun as rr
    from rerun import tracing_session

    client = rr.catalog.CatalogClient("rerun://…")
    with tracing_session():
        ds = client.get_dataset(name="…")
        _ = ds.scan().read_all()
    # The session id appears in the logs at scope entry:
    #   INFO rerun: rerun tracing session started: rs_8f3a91e2
    ```

    """
    from rerun_bindings import (
        _dec_active_tracing_sessions,
        _get_tracing_session_var,
        _inc_active_tracing_sessions,
        _is_telemetry_active,
        _log_tracing_session_started,
    )

    var = _get_tracing_session_var() if _is_telemetry_active() else None

    if var is None:
        logger.warning(
            "tracing_session() is a no-op: the rerun telemetry stack is not active. "
            "Set the environment variable TELEMETRY_ENABLED=true before importing "
            "rerun to enable session correlation.",
        )
        # Yield an obviously-invalid id so callers that bind via `as sid` still
        # work, but the value is clearly not a real session id.
        yield ""
        return

    sid = _generate_session_id()
    assert _is_valid_session_id(sid), f"generated invalid session id: {sid!r}"

    # The atomic counter lets the Rust enricher skip GIL acquisitions when no
    # `tracing_session()` scope is active anywhere in the process. Increment
    # first so any RPC fired between `var.set` and the yield still sees a
    # non-zero gate, and pair it with an outer `try` so the counter is always
    # decremented even if `var.set` itself raises.
    _inc_active_tracing_sessions()
    try:
        token = var.set(sid)
        try:
            # Surface the id immediately so the customer can grab it even if
            # their workflow crashes or hangs before exiting the `with` block.
            # Routed through the Rust `tracing` stack so it follows the same
            # `RUST_LOG` and fmt-layer pipeline as every other rerun log,
            # rather than the Python `logging` pipeline (which has no default
            # handler attached to the `rerun` logger and would silently drop
            # INFO records in environments like ipython).
            _log_tracing_session_started(sid)
            yield sid
        finally:
            var.reset(token)
    finally:
        _dec_active_tracing_sessions()
