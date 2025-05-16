from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from mcp.server.fastmcp import FastMCP
from utils import mcp_response, get_week, format_date, fetch_ticket_prices, filter_dates, get_airport_code, find_lowest_price

# 初始化FastMCP服务器，端口20001
mcp = FastMCP(port=20001)

# MCP main prompt, concise and professional for LLMs
MCP_PROMPT = (
    "This MCP server exposes the following tools for querying real-time flight ticket information between major Chinese cities. "
    "Each tool is annotated with @mcp.tool and returns a standardized JSON object: {success: bool, data: object/list, error: string or null}. "
    "All city names must be in Chinese (e.g., '北京', '上海'). "
    "If a date range is required and not provided, it defaults to today and today+10 days. "
    "Error details are always provided in the 'error' field if a call fails. "
    "Available tools: "
    "- list_supported_cities(): List all supported cities. "
    "- get_ticket_price_by_date(start_city, end_city, date): Query ticket price for a specific date (YYYYMMDD). "
    "- get_all_ticket_prices(start_city, end_city, start_date, end_date): Query all ticket prices in a date range. "
    "- get_lowest_ticket_price(start_city, end_city, start_date, end_date): Query the lowest ticket price in a date range. "
    "- get_round_trip_prices(start_city, end_city, start_date, end_date): Query round-trip ticket prices in a date range."
)

# Register the main prompt (fixed decorator usage)
@mcp.prompt()
def main_prompt() -> str:
    """
    Main prompt for LLMs and tool consumers. Concisely describes all @mcp.tool capabilities, input/output schema, and error handling in English.
    """
    return MCP_PROMPT


AIRPORT_CODES = {
        '北京':'BJS', '上海':'SHA', '广州':'CAN', '深圳':'SZX', '成都':'CTU', '杭州':'HGH', '武汉':'WUH', '西安':'SIA', '重庆':'CKG', '青岛':'TAO', '长沙':'CSX', '南京':'NKG', '厦门':'XMN', '昆明':'KMG', '大连':'DLC', '天津':'TSN', '郑州':'CGO', '三亚':'SYX', '济南':'TNA', '福州':'FOC', '阿勒泰':'AAT', '阿克苏':'AKU', '鞍山':'AOG', '安庆':'AQG', '安顺':'AVA', '阿拉善左旗':'AXF', '中国澳门':'MFM', '阿里':'NGQ', '阿拉善右旗':'RHT', '阿尔山':'YIE', '巴中':'BZX', '百色':'AEB', '包头':'BAV', '毕节':'BFJ', '北海':'BHY', '北京(大兴国际机场)':'BJS,PKX', '北京(首都国际机场)':'BJS,PEK', '博乐':'BPL', '保山':'BSD', '白城':'DBC', '布尔津':'KJI', '白山':'NBS', '巴彦淖尔':'RLK', '昌都':'BPX', '承德':'CDE', '常德':'CGD', '长春':'CGQ', '朝阳':'CHG', '赤峰':'CIF', '长治':'CIH', '沧源':'CWJ', '常州':'CZX', '池州':'JUH', '大同':'DAT', '达州':'DAX', '稻城':'DCY', '丹东':'DDG', '迪庆':'DIG', '大理':'DLU', '敦煌':'DNH', '东营':'DOY', '大庆':'DQA', '德令哈':'HXD', '鄂尔多斯':'DSN', '额济纳旗':'EJN', '恩施':'ENH', '二连浩特':'ERL', '阜阳':'FUG', '抚远':'FYJ', '富蕴':'FYN', '果洛':'GMQ', '格尔木':'GOQ', '广元':'GYS', '固原':'GYU', '中国高雄':'KHH', '赣州':'KOW', '贵阳':'KWE', '桂林':'KWL', '红原':'AHJ', '海口':'HAK', '河池':'HCJ', '邯郸':'HDG', '黑河':'HEK', '呼和浩特':'HET', '合肥':'HFE', '淮安':'HIA', '怀化':'HJJ', '海拉尔':'HLD', '哈密':'HMI', '衡阳':'HNY', '哈尔滨':'HRB', '和田':'HTN', '花土沟':'HTT', '中国花莲':'HUN', '霍林郭勒':'HUO', '惠州':'HUZ', '汉中':'HZG', '黄山':'TXN', '呼伦贝尔':'XRQ', '中国嘉义':'CYI', '景德镇':'JDZ', '加格达奇':'JGD', '嘉峪关':'JGN', '井冈山':'JGS', '金昌':'JIC', '九江':'JIU', '荆门':'JM1', '佳木斯':'JMU', '济宁':'JNG', '锦州':'JNZ', '建三江':'JSJ', '鸡西':'JXA', '九寨沟':'JZH', '中国金门':'KNH', '揭阳':'SWA', '库车':'KCA', '康定':'KGT', '喀什':'KHG', '凯里':'KJH', '库尔勒':'KRL', '克拉玛依':'KRY', '黎平':'HZH', '澜沧':'JMJ', '龙岩':'LCX', '临汾':'LFQ', '兰州':'LHW', '丽江':'LJG', '荔波':'LLB', '吕梁':'LLV', '临沧':'LNJ', '陇南':'LNL', '六盘水':'LPF', '拉萨':'LXA', '洛阳':'LYA', '连云港':'LYG', '临沂':'LYI', '柳州':'LZH', '泸州':'LZO', '林芝':'LZY', '芒市':'LUM', '牡丹江':'MDG', '中国马祖':'MFK', '绵阳':'MIG', '梅州':'MXZ', '中国马公':'MZG', '满洲里':'NZH', '漠河':'OHE', '南昌':'KHN', '中国南竿':'LZN', '南充':'NAO', '宁波':'NGB', '宁蒗':'NLH', '南宁':'NNG', '南阳':'NNY', '南通':'NTG', '攀枝花':'PZI', '普洱':'SYM', '琼海':'BAR', '秦皇岛':'BPE', '祁连':'HBQ', '且末':'IQM', '庆阳':'IQN', '黔江':'JIQ', '泉州':'JJN', '衢州':'JUZ', '齐齐哈尔':'NDG', '日照':'RIZ', '日喀则':'RKZ', '若羌':'RQA', '神农架':'HPG', '莎车':'QSZ', '沈阳':'SHE', '石河子':'SHF', '石家庄':'SJW', '上饶':'SQD', '三明':'SQJ', '十堰':'WDS', '邵阳':'WGN', '松原':'YSQ', '台州':'HYN', '中国台中':'RMQ', '塔城':'TCG', '腾冲':'TCZ', '铜仁':'TEN', '通辽':'TGO', '天水':'THQ', '吐鲁番':'TLQ', '通化':'TNH', '中国台南':'TNN', '中国台北':'TPE', '中国台东':'TTT', '唐山':'TVS', '太原':'TYN', '五大连池':'DTU', '乌兰浩特':'HLH', '乌兰察布':'UCB', '乌鲁木齐':'URC', '潍坊':'WEF', '威海':'WEH', '文山':'WNH', '温州':'WNZ', '乌海':'WUA', '武夷山':'WUS', '无锡':'WUX', '梧州':'WUZ', '万州':'WXN', '乌拉特中旗':'WZQ', '巫山':'WSK', '兴义':'ACX', '夏河':'GXH', '中国香港':'HKG', '西双版纳':'JHG', '新源':'NLT', '忻州':'WUT', '信阳':'XAI', '襄阳':'XFN', '西昌':'XIC', '锡林浩特':'XIL', '西宁':'XNN', '徐州':'XUZ', '延安':'ENY', '银川':'INC', '伊春':'LDS', '永州':'LLF', '榆林':'UYN', '宜宾':'YBP', '运城':'YCU', '宜春':'YIC', '宜昌':'YIH', '伊宁':'YIN', '义乌':'YIW', '营口':'YKH', '延吉':'YNJ', '烟台':'YNT', '盐城':'YNZ', '扬州':'YTY', '玉树':'YUS', '岳阳':'YYA', '张家界':'DYG', '舟山':'HSN', '扎兰屯':'NZL', '张掖':'YZY', '昭通':'ZAT', '湛江':'ZHA', '中卫':'ZHY', '张家口':'ZQZ', '珠海':'ZUH', '遵义':'ZYI'
        # 确保添加了所有需要的城市和机场代码
    }

# MCP工具函数区（全部原子化、结构化返回）

@mcp.tool(name="list_supported_cities", description="获取所有支持的城市")
def tool_list_supported_cities() -> Dict[str, Any]:
    """
    获取所有支持的城市。
    :return: {success, data: {cities: [...]}, error}
    """
    return mcp_response(True, {"cities": list(AIRPORT_CODES.keys())})

@mcp.tool(name="get_ticket_price_by_date", description="查询指定日期的机票价格")
def tool_get_ticket_price_by_date(start_city: str, end_city: str, date: str) -> Dict[str, Any]:
    """
    查询指定日期的机票价格。
    :param start_city: 出发城市
    :param end_city: 到达城市
    :param date: 查询日期（YYYYMMDD）
    :return: {success, data: {...}, error}
    """
    start_code = get_airport_code(start_city, AIRPORT_CODES)
    end_code = get_airport_code(end_city, AIRPORT_CODES)
    if not start_code or not end_code:
        return mcp_response(False, None, f"请确认输入的城市名称是否正确，未找到{'出发城市' if not start_code else '到达城市'}对应的机场代码")
    try:
        ticket_data = fetch_ticket_prices(start_code, end_code)
        if date not in ticket_data:
            return mcp_response(False, None, f"未找到从 {start_city} 到 {end_city} 在 {date} 的机票价格信息")
        price = ticket_data[date]
        formatted_date = format_date(date)
        weekday = get_week(formatted_date)
        return mcp_response(True, {
            "departure_city": start_city,
            "arrival_city": end_city,
            "date": formatted_date,
            "weekday": weekday,
            "price": price
        })
    except Exception as e:
        return mcp_response(False, None, f"查询失败: {str(e)}")

# 获取默认日期区间（今天~今天+10天）
def get_default_date_range():
    today = datetime.now()
    start = today.strftime('%Y%m%d')
    end = (today + timedelta(days=10)).strftime('%Y%m%d')
    return start, end

@mcp.tool(name="get_all_ticket_prices", description="查询区间内所有机票价格")
def tool_get_all_ticket_prices(start_city: str, end_city: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """
    查询区间内所有机票价格。
    :param start_city: 出发城市
    :param end_city: 到达城市
    :param start_date: 起始日期（YYYYMMDD）
    :param end_date: 结束日期（YYYYMMDD）
    :return: {success, data: {...}, error}
    """
    if not start_date or not end_date:
        start_date, end_date = get_default_date_range()
    start_code = get_airport_code(start_city, AIRPORT_CODES)
    end_code = get_airport_code(end_city, AIRPORT_CODES)
    if not start_code or not end_code:
        return mcp_response(False, None, f"请确认输入的城市名称是否正确，未找到{'出发城市' if not start_code else '到达城市'}对应的机场代码")
    try:
        ticket_data = fetch_ticket_prices(start_code, end_code)
        filtered_data = filter_dates(ticket_data, start_date, end_date)
        if not filtered_data:
            return mcp_response(False, None, f"未找到从 {start_city} 到 {end_city} 在指定日期范围内的机票价格信息")
        result = []
        for date, price in filtered_data.items():
            formatted_date = format_date(date)
            weekday = get_week(formatted_date)
            result.append({
                "date": formatted_date,
                "weekday": weekday,
                "price": price
            })
        return mcp_response(True, {
            "departure_city": start_city,
            "arrival_city": end_city,
            "tickets": result
        })
    except Exception as e:
        return mcp_response(False, None, f"查询失败: {str(e)}")

@mcp.tool(name="get_lowest_ticket_price", description="查询区间内最低价格机票")
def tool_get_lowest_ticket_price(start_city: str, end_city: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """
    查询区间内最低价格机票。
    :param start_city: 出发城市
    :param end_city: 到达城市
    :param start_date: 起始日期（YYYYMMDD）
    :param end_date: 结束日期（YYYYMMDD）
    :return: {success, data: {...}, error}
    """
    if not start_date or not end_date:
        start_date, end_date = get_default_date_range()
    start_code = get_airport_code(start_city, AIRPORT_CODES)
    end_code = get_airport_code(end_city, AIRPORT_CODES)
    if not start_code or not end_code:
        return mcp_response(False, None, f"请确认输入的城市名称是否正确，未找到{'出发城市' if not start_code else '到达城市'}对应的机场代码")
    try:
        ticket_data = fetch_ticket_prices(start_code, end_code)
        filtered_data = filter_dates(ticket_data, start_date, end_date)
        lowest = find_lowest_price(filtered_data)
        if not lowest:
            return mcp_response(False, None, f"未找到从 {start_city} 到 {end_city} 在指定日期范围内的最低价格机票")
        formatted_date = format_date(lowest["date"])
        weekday = get_week(formatted_date)
        return mcp_response(True, {
            "departure_city": start_city,
            "arrival_city": end_city,
            "date": formatted_date,
            "weekday": weekday,
            "price": lowest["price"]
        })
    except Exception as e:
        return mcp_response(False, None, f"查询失败: {str(e)}")

@mcp.tool(name="get_round_trip_prices", description="查询往返机票价格")
def tool_get_round_trip_prices(start_city: str, end_city: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """
    查询往返机票价格。
    :param start_city: 出发城市
    :param end_city: 到达城市
    :param start_date: 起始日期（YYYYMMDD）
    :param end_date: 结束日期（YYYYMMDD）
    :return: {success, data: {...}, error}
    """
    if not start_date or not end_date:
        start_date, end_date = get_default_date_range()
    start_code = get_airport_code(start_city, AIRPORT_CODES)
    end_code = get_airport_code(end_city, AIRPORT_CODES)
    if not start_code or not end_code:
        return mcp_response(False, None, f"请确认输入的城市名称是否正确，未找到{'出发城市' if not start_code else '到达城市'}对应的机场代码")
    try:
        outbound_data = fetch_ticket_prices(start_code, end_code)
        return_data = fetch_ticket_prices(end_code, start_code)
        filtered_outbound = filter_dates(outbound_data, start_date, end_date)
        filtered_return = filter_dates(return_data, start_date, end_date)
        outbound_list = []
        for date, price in filtered_outbound.items():
            formatted_date = format_date(date)
            weekday = get_week(formatted_date)
            outbound_list.append({
                "date": formatted_date,
                "weekday": weekday,
                "price": price
            })
        return_list = []
        for date, price in filtered_return.items():
            formatted_date = format_date(date)
            weekday = get_week(formatted_date)
            return_list.append({
                "date": formatted_date,
                "weekday": weekday,
                "price": price
            })
        return mcp_response(True, {
            "departure_city": start_city,
            "arrival_city": end_city,
            "outbound_tickets": outbound_list,
            "return_tickets": return_list
        })
    except Exception as e:
        return mcp_response(False, None, f"查询失败: {str(e)}")

# 启动MCP服务器
if __name__ == "__main__":
    mcp.run(transport='streamable-http')
