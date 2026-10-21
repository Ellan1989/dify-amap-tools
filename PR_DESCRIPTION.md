# Plugin Submission

## Plugin information

- **Author**: ellan1989
- **Plugin name**: amap_tools
- **Version**: 0.0.1
- **Source repository**: https://github.com/Ellan1989/dify-amap-tools
- **Contact**: Ellan1989@users.noreply.github.com

## Submission type

- [x] New plugin
- [ ] Version update

## What changed

New tool plugin providing China location capabilities via the Amap (Gaode
Maps) Web Service API (https://lbs.amap.com):

- `geocode` tool — convert a Chinese address into coordinates with
  province/city/district breakdown and match precision.
- `regeocode` tool — convert GCJ-02 coordinates back into a formatted Chinese
  address with administrative divisions and adcode.
- `poi_search` tool — keyword search over points of interest in China
  (stores, landmarks, stations), optionally restricted to a city.
- `weather` tool — current live weather for a Chinese city by 6-digit adcode.

Requires the user's own Amap Web Service key (free tier with daily quotas),
configured as the `amap_key` credential. Independent third-party integration,
clearly labeled as not affiliated with Amap in the README.

## Risk level

- [x] Low risk
- [ ] Medium risk
- [ ] High risk

The plugin makes read-only GET requests to a single API domain (declared in
`manifest.yaml` `network.domains`). No file, shell, database, or
arbitrary-URL capabilities.

## Required checks

- [x] I have read and followed the [Marketplace submission requirements](https://github.com/langgenius/dify-plugins/blob/main/docs/plugin-submission-requirements.md).
- [x] I have read and comply with the Plugin Developer Agreement.
- [x] I tested this plugin on Dify Community Edition and Dify Cloud, or documented any limitation below.
- [x] The package contains only files needed at runtime.
- [x] The package does not contain secrets, local credentials, `.env` files, `.git` directories, virtual environments, caches, logs, or IDE files.
- [x] The package does not contain executables or bundled binaries, or I explained why they are required below.
- [x] The plugin README includes setup steps, usage instructions, required APIs or credentials, connection requirements, and the source repository link.
- [x] The plugin includes `PRIVACY.md` or a hosted privacy policy, and `manifest.yaml` references it.
- [x] All user-facing text is primarily in English, with any localized README files following the [i18n guidance](https://docs.dify.ai/en/develop-plugin/features-and-specs/plugin-types/multilingual-readme).

## Security and privacy notes

None. The plugin forwards only the user-provided address / coordinates /
keyword / adcode to the official endpoint `https://restapi.amap.com`
(JSON GET, key in a Dify secret credential sent as the `key` query
parameter). No data is stored, logged, or sent anywhere else. See PRIVACY.md.

## Local validation

Ran the official local validator from langgenius/dify-marketplace-toolkit:

```
python validator/validate-difypkg.py ellan1989/amap_tools/amap_tools-0.0.1.difypkg --output-dir ./validation-report
```

Result: **0 blocking failures**; all blocking checks PASS. Remaining warnings
are informational (single declared outbound domain; 2 pinned dependencies).

Also verified locally: the plugin loads under dify-plugin 0.10.2 (all four
tools register); the API error path was exercised live (an invalid key
returns `{"status":"0","info":"INVALID_USER_KEY"}` and surfaces cleanly to
the user); Amap's quirk of returning `[]` for empty city/district/tel fields
is handled defensively.

## Reviewer notes

- Resubmission of #3427, which was closed because the previous PR body accidentally
  contained two non-English header lines from a local template file. The package is
  unchanged; this body is pure English per the submission template (verified locally
  with check-pr-body.py from dify-marketplace-toolkit).

- No marketplace plugin currently covers the Amap Web Service API, so this
  fills a gap for location tasks in China (a common need for agents serving
  the Chinese market).
- `dify-plugin` and `httpx` are pinned to exact versions in both
  `requirements.txt` and `pyproject.toml` per validator guidance.
