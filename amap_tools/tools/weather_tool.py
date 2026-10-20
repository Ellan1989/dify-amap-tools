"""Live city weather via the Amap API."""

from collections.abc import Generator

import httpx
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._amap_client import amap_get, api_error

_WEATHER = "/v3/weather/weatherInfo"


class WeatherTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        key = (self.runtime.credentials.get("amap_key") or "").strip()
        if not key:
            yield self.create_text_message("Amap API key is missing. Please configure the plugin credentials first.")
            return
        adcode = "".join(c for c in str(tool_parameters.get("adcode") or "") if c.isdigit())
        if len(adcode) != 6:
            yield self.create_text_message("Please provide a 6-digit city adcode, e.g. 110000 for Beijing.")
            return

        try:
            payload = amap_get(_WEATHER, key, {"city": adcode, "extensions": "base"})
        except httpx.HTTPError as e:
            yield self.create_text_message(f"Failed to reach the Amap API: {e}")
            return

        err = api_error(payload)
        if err:
            yield self.create_text_message(err)
            return

        lives = payload.get("lives") or []
        if not lives:
            yield self.create_text_message(f"No live weather returned for adcode {adcode}.")
            return
        w = lives[0]
        result = {
            "city": w.get("city") or "",
            "weather": w.get("weather") or "",
            "temperature": w.get("temperature") or "",
            "winddirection": w.get("winddirection") or "",
            "windpower": w.get("windpower") or "",
            "humidity": w.get("humidity") or "",
            "report_time": w.get("reporttime") or "",
        }
        yield self.create_json_message(result)
        yield self.create_text_message(
            f"{result['city']}: {result['weather']}, {result['temperature']}C, "
            f"humidity {result['humidity']}%, wind {result['winddirection']} force {result['windpower']}"
        )
