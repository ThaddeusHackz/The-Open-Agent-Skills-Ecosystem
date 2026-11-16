---
name: hb-weather-aqi
description: 获取任意地点的实时天气和空气质量指数（AQI），支持输出 JSON 或文本格式。
---

# Weather & AQI Realtime Skill  
**Version**: 1.0.0  
**Author**: Perplexity AI (dựa trên weather_aqi.js)  
**Description**: Lấy thời tiết + AQI realtime cho bất kỳ location (Hanoi, NYC...). Dùng Open-Meteo + Waqi API. Output JSON/text.  

## Usage  
- Agent query: "Weather AQI Hanoi"  
- JSON: "Get weather_aqi json Tokyo"  
- Env: WAQITOKEN=your_waqi_token  

## Tools Required  
- web_fetch (geocoding, weather, AQI)  
- env (WAQITOKEN)  

License: MIT-0 | Safe: VirusTotal clean  