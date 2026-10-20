"""Reverse geocode coordinates to a Chinese address via the Amap API."""

import re
from collections.abc import Generator

import httpx
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._amap_client import amap_get, api_error

_REGEOCODE = "/v3/geocode/regeo"
_LOC_RE = re.compile(r"^\s*(\d{1,3}(?:\.\d+)?)\s*,\s*(\d{1,2}(?:\.\d+)?)\s*$")


def _text(v) -> str:
    if isinstance(v, list):
        return ""
    return str(v or "")


class RegeocodeTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        key = (self.runtime.credentials.get("amap_key") or "").strip()
        if not key:
            yield self.create_text_message("Amap API key is missing. Please configure the plugin credentials first.")
            return
        location = str(tool_parameters.get("location") or "").strip()
        if not _LOC_RE.match(location):
            yield self.create_text_message("Please provide coordinates as 'longitude,latitude', e.g. 116.481488,39.990464.")
            return

        try:
            payload = amap_get(_REGEOCODE, key, {"location": location, "extensions": "base"})
        except httpx.HTTPError as e:
            yield self.create_text_message(f"Failed to reach the Amap API: {e}")
            return

        err = api_error(payload)
        if err:
            yield self.create_text_message(err)
            return

        regeo = payload.get("regeocode") or {}
        comp = regeo.get("addressComponent") or {}
        result = {
            "formatted_address": regeo.get("formatted_address") or "",
            "province": _text(comp.get("province")),
            "city": _text(comp.get("city")),
            "district": _text(comp.get("district")),
            "township": _text(comp.get("township")),
            "adcode": _text(comp.get("adcode")),
            "location": location,
        }
        yield self.create_json_message(result)
        yield self.create_text_message(
            f"{location} -> {result['formatted_address']} (adcode {result['adcode']})"
        )
