# Amap Tools

China location tools for [Dify](https://dify.ai), based on the
**Amap (Gaode Maps) Web Service API**: geocoding, reverse geocoding,
POI keyword search and city weather.

> This is an independent third-party integration. It is **not** developed by
> or affiliated with Amap. It requires your own Amap API key; free tier with
> daily quotas is available for individual developers.

## Tools

### 1. Geocode Address

Convert a Chinese address into coordinates (longitude, latitude) with
province/city/district breakdown and a match-precision level.

### 2. Reverse Geocode

Convert `longitude,latitude` coordinates (GCJ-02) back into a formatted
Chinese address with administrative divisions and adcode.

### 3. POI Search

Search points of interest in China by keyword — stores, landmarks, brand
outlets, stations — optionally restricted to one city. Returns name,
category, address, coordinates and phone per match.

### 4. City Weather

Current live weather for a Chinese city by 6-digit adcode
(Beijing `110000`, Shanghai `310000`, Guangzhou `440100`, Shenzhen `440300`).

## Credentials

1. Sign up at the Amap open platform: <https://lbs.amap.com>
2. Create an application and add a key of type **Web Service**.
3. In Dify, open **Tools → Amap Tools → Authorize**, and paste the key into
   the `Amap Web Service key` field.

The key is sent as the `key` query parameter on every API call. Users must
comply with the Amap open platform terms of service.

## Usage

1. Install the plugin from the Dify Marketplace (or install the `.difypkg`
   package via *Install from local file*).
2. Authorize it with your Web Service key.
3. Add any tool to an Agent or Workflow node — for example geocode an
   address, or search POIs around a city.

## Data & privacy

See [PRIVACY.md](PRIVACY.md). In short: the plugin only forwards the
address/keyword/adcode you provide to the official Amap endpoint and returns
the result; nothing is stored or sent anywhere else.

## Source

<https://github.com/Ellan1989/dify-amap-tools>

## License

Apache-2.0
