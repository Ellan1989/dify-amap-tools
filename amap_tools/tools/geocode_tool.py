"""Geocode a Chinese address to coordinates via the Amap API."""

from collections.abc import Generator

import httpx
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._amap_client import amap_get, api_error

_GEOCODE = "/v3/geocode/geo"


def _text(v) -> str:
    """Amap returns [] for empty city/district fields."""
    if isinstance(v, list):
        return ""
    return str(v or "")


class GeocodeTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        key = (self.runtime.credentials.get("amap_key") or "").strip()
        if not key:
            yield self.create_text_message("Amap API key is missing. Please configure the plugin credentials first.")
            return
        address = str(tool_parameters.get("address") or "").strip()
        if not address:
            yield self.create_text_message("Please provide an address to geocode.")
            return
        city = str(tool_parameters.get("city") or "").strip()
        params = {"address": address}
        if city:
            params["city"] = city

        try:
            payload = amap_get(_GEOCODE, key, params)
        except httpx.HTTPError as e:
            yield self.create_text_message(f"Failed to reach the Amap API: {e}")
            return

        err = api_error(payload)
        if err:
            yield self.create_text_message(err)
            return

        geocodes = payload.get("geocodes") or []
        results = [
            {
                "address": address,
                "country": g.get("country") or "",
                "province": g.get("province") or "",
                "city": _text(g.get("city")),
                "district": _text(g.get("district")),
                "street": g.get("street") or "",
                "location": g.get("location") or "",
                "adcode": g.get("adcode") or "",
                "level": g.get("level") or "",
            }
            for g in geocodes
            if isinstance(g, dict)
        ]
        yield self.create_json_message({"results": results})
        if not results:
            yield self.create_text_message(f"No geocode result for '{address}'.")
            return
        r = results[0]
        lines = [f"{address} -> {r['location']}"]
        region = " ".join(x for x in (r["province"], r["city"], r["district"]) if x)
        if region:
            lines.append(f"Region: {region} (adcode {r['adcode']}, level {r['level']})")
        yield self.create_text_message("\n".join(lines))
