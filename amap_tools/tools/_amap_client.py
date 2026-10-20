"""Shared Amap Web Service client helpers."""

import httpx

API_BASE = "https://restapi.amap.com"


def amap_get(path: str, key: str, params: dict) -> dict:
    """GET an Amap endpoint and return the parsed JSON payload.

    Raises httpx.HTTPError on transport failure, ValueError on non-JSON body.
    Amap signals success with status == "1"; callers must check it.
    """
    resp = httpx.get(f"{API_BASE}{path}", params={**params, "key": key}, timeout=30)
    return resp.json()


def api_error(payload: dict) -> str | None:
    """Return a human-readable error string if the payload reports failure."""
    if payload.get("status") == "1":
        return None
    return f"Amap API error: {payload.get('info')} (infocode {payload.get('infocode')})"
