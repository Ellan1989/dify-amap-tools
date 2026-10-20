# Privacy Policy — Amap Tools Dify Plugin

Last updated: 2026-10-20

This plugin ("Amap Tools") is a tool plugin for the Dify platform. It calls
the Amap (Gaode Maps) Web Service API on behalf of the Dify user who invokes
it. It is an independent third-party integration and is not affiliated with
Amap.

## What the plugin collects

Nothing. The plugin itself does not collect, store, log, or share any
personal data. It has no analytics, no telemetry, and no third-party
services besides the Amap API described below.

## What the plugin transmits, and where

- **Tool input you provide** (an address, coordinates, a POI keyword, or a
  city adcode) is sent to the official endpoint `https://restapi.amap.com`
  to perform the lookup, and the API response is returned to your Dify app.
- **Your Amap Web Service key** is stored by Dify as plugin credentials and
  sent to the Amap API as the `key` query parameter. It is never sent
  anywhere else and never included in tool output.

## Third-party service

Requests are made to the Amap open platform. Their own terms and privacy
policy apply to that service: <https://lbs.amap.com>

## Contact

For any questions about this plugin, open an issue at
<https://github.com/Ellan1989/dify-amap-tools>.
