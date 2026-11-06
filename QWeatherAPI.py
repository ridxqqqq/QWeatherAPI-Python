#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""和风天气 API 调用示例。

使用前请将 myKey.example.py 复制为 myKey.py, 并填写 KEY 与 API_HOST,
凭据可在 https://console.qweather.com 获取。
"""

import os
import sys

import requests

try:
    from myKey import KEY, API_HOST
except ImportError:
    KEY = API_HOST = ''

TIMEOUT = 10
WECHAT_WEBHOOK = os.environ.get('QWEATHER_WECHAT_WEBHOOK', '')


def _request(path, **params):
    """请求 API 并返回解析后的 JSON, 状态码或业务码异常时抛出错误。"""
    params['key'] = KEY
    response = requests.get(f'https://{API_HOST}{path}', params=params, timeout=TIMEOUT)
    response.raise_for_status()
    data = response.json()
    if data.get('code') != '200':
        raise RuntimeError(f'API 错误: {data.get("code")} {data}')
    return data


def lookup_city(keyword):
    """按城市名查询, 返回 (城市ID, 区县, 城市, 省份, 国家, 纬度, 经度)。"""
    location = _request('/geo/v2/city/lookup', location=keyword)['location'][0]
    return (
        location['id'],
        location['name'],
        location['adm2'],
        location['adm1'],
        location['country'],
        location['lat'],
        location['lon'],
    )


def weather_now(city_id):
    """实况天气。"""
    return _request('/v7/weather/now', location=city_id)['now']


def weather_daily(city_id, days=3):
    """逐日预报, days 支持 3/7/10/15。"""
    return _request(f'/v7/weather/{days}d', location=city_id)['daily']


def weather_hourly(city_id, hours=24):
    """逐小时预报, hours 支持 24/72/168。"""
    return _request(f'/v7/weather/{hours}h', location=city_id)['hourly']


def rain_minutely(lat, lon):
    """分钟级降水, 返回未来两小时预报。"""
    return _request('/v7/minutely/5m', location=f'{lon},{lat}')


def air_now(city_id):
    """实时空气质量。"""
    return _request('/v7/air/now', location=city_id)['now']


def send_wecom(content):
    """通过企业微信群机器人 Webhook 发送文本通知。"""
    response = requests.post(
        WECHAT_WEBHOOK,
        json={'msgtype': 'text', 'text': {'content': content}},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    result = response.json()
    if result.get('errcode') != 0:
        raise RuntimeError(f'企业微信通知发送失败: {result}')


def main():
    if not KEY or not API_HOST:
        print('缺少凭据, 请将 myKey.example.py 复制为 myKey.py 并填写 KEY 与 API_HOST')
        return 1

    city_id, district, city, province, _country, lat, lon = lookup_city('南岔')

    current = weather_now(city_id)
    daily = weather_daily(city_id)
    hourly = weather_hourly(city_id)
    rain = rain_minutely(lat, lon)
    air = air_now(city_id)

    if city == district:
        title = f'{province} {city}市'
    else:
        title = f'{province} {city}市 {district}区'

    n_hours_later = 1
    n_days_later = 1
    lines = [
        title,
        f'当前天气： {current["text"]} {current["temp"]} °C 体感温度 {current["feelsLike"]} °C',
        f'空气质量指数： {air["aqi"]}',
        f'降水情况： {rain["summary"]}',
        f'今日天气： {daily[0]["textDay"]} {daily[0]["tempMin"]} - {daily[0]["tempMax"]} °C',
        f'{n_hours_later} 小时后天气： {hourly[n_hours_later]["text"]} {hourly[n_hours_later]["temp"]} °C',
        f'{n_days_later} 天后天气： {daily[n_days_later]["textDay"]} {daily[n_days_later]["tempMin"]} - {daily[n_days_later]["tempMax"]} °C',
    ]

    content = '\n'.join(lines)
    print(content)

    if WECHAT_WEBHOOK:
        send_wecom(content)
        print('已发送企业微信通知')
    else:
        print('未配置企业微信 Webhook, 跳过通知')

    return 0


if __name__ == '__main__':
    sys.exit(main())
