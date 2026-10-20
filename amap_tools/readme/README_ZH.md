# 高德地图工具（Amap Tools）

一个 [Dify](https://dify.ai) 工具插件，基于**高德地图 Web 服务 API**：地理编码、
逆地理编码、POI 关键词搜索与城市天气查询。

> 本插件为独立第三方集成，与高德官方无关联。需使用你自己的高德 API key，
> 个人开发者有免费日配额。

## 工具

### 1. 地理编码（Geocode Address）

把中文地址转换为经纬度坐标，返回省市区信息与匹配精度。

### 2. 逆地理编码（Reverse Geocode）

把「经度,纬度」（GCJ-02 坐标系）转换回结构化中文地址（含行政区划与 adcode）。

### 3. POI 搜索（POI Search）

按关键词搜索国内兴趣点——门店、地标、品牌、车站等，可限定城市。
返回名称、分类、地址、坐标与电话。

### 4. 城市天气（City Weather）

按 6 位 adcode 查询城市实时天气（北京 `110000`、上海 `310000`、
广州 `440100`、深圳 `440300`）。

## 凭据配置

1. 在高德开放平台注册：<https://lbs.amap.com>
2. 创建应用，添加「Web 服务」类型的 key。
3. Dify 中打开 **工具 → Amap Tools → 授权**，粘贴到
   `Amap Web Service key` 输入框。

key 以 `key` 查询参数发送。使用者须遵守高德开放平台服务条款。

## 使用方法

1. 从 Dify Marketplace 安装插件（或本地安装 `.difypkg`）。
2. 用 Web 服务 key 完成授权。
3. 在 Agent 或工作流节点中添加任意工具——例如地理编码一个地址，
   或在某城市内搜索 POI。

## 数据与隐私

见 [PRIVACY.md](../PRIVACY.md)：本插件只把你传入的地址/关键词/adcode
转发给高德官方接口并返回结果，不存储、不外发到任何第三方。

## 源码

<https://github.com/Ellan1989/dify-amap-tools>

## 许可

Apache-2.0
