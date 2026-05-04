from __future__ import annotations

from typing import TYPE_CHECKING

from rerun._tracing_session import (
    _generate_session_id,
    _is_valid_session_id,
    tracing_session,
)

if TYPE_CHECKING:
    import pytest


def test_generated_id_is_valid() -> None:
    for _ in range(8):
        sid = _generate_session_id()
        assert _is_valid_session_id(sid), f"generated invalid id: {sid!r}"


def test_validation_rejects_malformed_ids() -> None:
    bad_ids = [
        "",
        "rs_",
        "rs_cafebab",  # 7 hex chars
        "rs_cafebabe1",  # 9 hex chars
        "rs_CAFEBABE",  # uppercase
        "rs_cafebabz",  # non-hex
        "xx_cafebabe",  # wrong prefix
        "cafebabe",  # missing prefix
    ]
    for sid in bad_ids:
        assert not _is_valid_session_id(sid), f"unexpectedly accepted: {sid!r}"


def test_logs_session_id_at_scope_entry(monkeypatch: pytest.MonkeyPatch) -> None:
    """The session id must be forwarded to the Rust `tracing` stack on scope entry."""
    import rerun_bindings  # noqa: TID251

    captured: list[str] = []

    def fake_log(sid: str) -> None:
        captured.append(sid)

    # The context manager imports its bindings lazily from `rerun_bindings`, so
    # patching the symbols on that module is what gets picked up at scope entry.
    # `_is_telemetry_active` is forced to `True` so the test exercises the
    # active-telemetry branch regardless of whether `TELEMETRY_ENABLED=true`
    # was set for the running process (CI does not set it).
    monkeypatch.setattr(rerun_bindings, "_is_telemetry_active", lambda: True)
    monkeypatch.setattr(rerun_bindings, "_log_tracing_session_started", fake_log)

    with tracing_session() as sid:
        pass

    assert captured == [sid], f"expected Rust logger to be called once with {sid!r}, got: {captured!r}"


def test_warns_and_no_ops_when_telemetry_inactive(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Warn and yield an empty id when `TELEMETRY_ENABLED` is not truthy."""
    import rerun_bindings  # noqa: TID251

    # Force the inactive-telemetry branch regardless of process-wide env so
    # this case exercises in CI even when telemetry happens to be active.
    monkeypatch.setattr(rerun_bindings, "_is_telemetry_active", lambda: False)

    with caplog.at_level("WARNING", logger="rerun"):
        with tracing_session() as sid:
            assert sid == ""

    assert any("TELEMETRY_ENABLED=true" in r.getMessage() for r in caplog.records), (
        f"expected a WARNING about TELEMETRY_ENABLED, got: {[r.getMessage() for r in caplog.records]}"
    )
