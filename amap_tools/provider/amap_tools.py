import httpx
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

_API_BASE = "https://restapi.amap.com"
_GEOCODE = f"{_API_BASE}/v3/geocode/geo"


class AmapToolsProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        key = (credentials.get("amap_key") or "").strip()
        if not key:
            raise ToolProviderCredentialValidationError("Amap Web Service key is required.")
        try:
            resp = httpx.get(
                _GEOCODE,
                params={"address": "北京市朝阳区", "key": key},
                timeout=15,
            )
        except httpx.HTTPError as e:
            raise ToolProviderCredentialValidationError(f"Failed to reach the Amap API: {e}") from e
        if resp.status_code == 429:
            return
        try:
            payload = resp.json()
        except ValueError:
            raise ToolProviderCredentialValidationError(
                f"Unexpected non-JSON response from the Amap API (HTTP {resp.status_code})."
            )
        if payload.get("status") == "1":
            return
        raise ToolProviderCredentialValidationError(
            f"The Amap API rejected the key: {payload.get('info')} (infocode {payload.get('infocode')})"
        )
