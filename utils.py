import requests
from datetime import datetime
from typing import Dict, Optional, Any

# 统一返回格式的工具函数
def mcp_response(success: bool, data: Any = None, error: Optional[str] = None) -> Dict[str, Any]:
    """
    统一MCP工具返回结构，便于大模型解析。
    :param success: 是否成功
    :param data: 主要数据内容
    :param error: 错误信息
    :return: 结构化JSON
    """
    return {
        "success": success,
        "data": data,
        "error": error
    }

# 工具函数区

def get_week(date_str: str) -> str:
    """
    获取日期对应的星期几。
    :param date_str: 格式为YYYY-MM-DD
    :return: 中文星期几
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return "星期" + "日一二三四五六"[date_obj.weekday()]

def format_date(date: str) -> str:
    """
    格式化日期字符串，从YYYYMMDD转为YYYY-MM-DD。
    :param date: 8位日期字符串
    :return: 10位日期字符串
    """
    year, month, day = date[:4], date[4:6], date[6:]
    return f"{year}-{month}-{day}"

def fetch_ticket_prices(start_code: str, end_code: str) -> Dict[str, int]:
    """
    从携程API获取机票价格信息。
    :param start_code: 出发地机场代码
    :param end_code: 目的地机场代码
    :return: 日期-价格字典
    """
    url = f"https://flights.ctrip.com/itinerary/api/12808/lowestPrice?flightWay=Oneway&dcity={start_code}&acity={end_code}&direct=true&army=false"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('data', {}).get('oneWayPrice', [{}])[0]
    else:
        raise Exception(f"获取数据失败，状态码: {response.status_code}")

def filter_dates(data: Dict[str, int], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, int]:
    """
    筛选指定日期范围内的机票价格数据。
    :param data: 日期-价格字典
    :param start_date: 起始日期（YYYYMMDD）
    :param end_date: 结束日期（YYYYMMDD）
    :return: 过滤后的字典
    """
    if not start_date and not end_date:
        return data
    filtered_data = {}
    for date, price in data.items():
        if (not start_date or date >= start_date) and (not end_date or date <= end_date):
            filtered_data[date] = price
    return filtered_data

def get_airport_code(city_name: str, airport_codes: dict) -> Optional[str]:
    """
    获取城市对应的机场代码。
    :param city_name: 城市名
    :param airport_codes: 机场代码字典
    :return: 机场代码或None
    """
    return airport_codes.get(city_name)

def find_lowest_price(data: Dict[str, int]) -> Optional[Dict[str, Any]]:
    """
    查找数据中的最低价格及其对应日期。
    :param data: 日期-价格字典
    :return: {'date': 日期, 'price': 价格} 或 None
    """
    if not data:
        return None
    lowest_price = float('inf')
    lowest_date = None
    for date, price in data.items():
        if price < lowest_price:
            lowest_price = price
            lowest_date = date
    if lowest_date:
        return {"date": lowest_date, "price": lowest_price}
    return None 