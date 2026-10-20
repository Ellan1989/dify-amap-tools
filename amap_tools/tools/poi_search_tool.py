"""POI keyword search via the Amap API."""

from collections.abc import Generator

import httpx
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._amap_client import amap_get, api_error

_PLACE_TEXT = "/v3/place/text"


class PoiSearchTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        key = (self.runtime.credentials.get("amap_key") or "").strip()
        if not key:
            yield self.create_text_message("Amap API key is missing. Please configure the plugin credentials first.")
            return
        keywords = str(tool_parameters.get("keywords") or "").strip()
        if not keywords:
            yield self.create_text_message("Please provide keywords to search for.")
            return
        city = str(tool_parameters.get("city") or "").strip()
        page_size = max(1, min(25, int(tool_parameters.get("page_size") or 10)))
        page = max(1, int(tool_parameters.get("page") or 1))

        params = {"keywords": keywords, "offset": page_size, "page": page, "extensions": "base"}
        if city:
            params["city"] = city

        try:
            payload = amap_get(_PLACE_TEXT, key, params)
        except httpx.HTTPError as e:
            yield self.create_text_message(f"Failed to reach the Amap API: {e}")
            return

        err = api_error(payload)
        if err:
            yield self.create_text_message(err)
            return

        pois_raw = payload.get("pois") or []
        pois = [
            {
                "name": p.get("name") or "",
                "category": p.get("type") or "",
                "address": (p.get("address") or "") if not isinstance(p.get("address"), list) else "",
                "location": p.get("location") or "",
                "city": p.get("cityname") or "",
                "phone": self._first_tel(p.get("tel")),
            }
            for p in pois_raw
            if isinstance(p, dict)
        ]
        yield self.create_json_message({"count": str(payload.get("count") or len(pois)), "pois": pois})

        lines = [f"Found {payload.get('count') or len(pois)} POI(s) for '{keywords}', showing {len(pois)}:"]
        for p in pois:
            bits = [p["name"]]
            if p["city"]:
                bits.append(p["city"])
            if p["address"]:
                bits.append(p["address"])
            lines.append("- " + " | ".join(bits))
        yield self.create_text_message("\n".join(lines))

    @staticmethod
    def _first_tel(tel) -> str:
        """Amap returns tel as a string or a list of strings."""
        if isinstance(tel, list):
            return tel[0] if tel else ""
        return str(tel or "")
