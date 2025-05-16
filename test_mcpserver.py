from utils import mcp_response
from main import (
    tool_get_airport_code, tool_list_supported_cities, tool_get_ticket_price_by_date,
    tool_get_all_ticket_prices, tool_get_lowest_ticket_price, tool_get_round_trip_prices, AIRPORT_CODES
)

# MCP服务器健康检查与返回结构测试工具

def _check_tool(tool_func, *args, **kwargs):
    """
    内部测试函数，调用tool并检查返回结构。
    :return: (tool名, 是否通过, 错误信息, 返回内容)
    """
    try:
        result = tool_func(*args, **kwargs)
        if not isinstance(result, dict):
            return tool_func.__name__, False, "返回值不是dict", result
        if not all(k in result for k in ("success", "data", "error")):
            return tool_func.__name__, False, "缺少必要字段(success, data, error)", result
        return tool_func.__name__, True, None, result
    except Exception as e:
        return tool_func.__name__, False, str(e), None

# 典型测试参数
CITY_A = "北京"
CITY_B = "上海"
TEST_DATE = "202505020"

# 分别测试每个MCP工具

def test_get_airport_code():
    return _check_tool(tool_get_airport_code, CITY_A)

def test_list_supported_cities():
    return _check_tool(tool_list_supported_cities)

def test_get_ticket_price_by_date():
    return _check_tool(tool_get_ticket_price_by_date, CITY_A, CITY_B, TEST_DATE)

def test_get_all_ticket_prices():
    return _check_tool(tool_get_all_ticket_prices, CITY_A, CITY_B)

def test_get_lowest_ticket_price():
    return _check_tool(tool_get_lowest_ticket_price, CITY_A, CITY_B)

def test_get_round_trip_prices():
    return _check_tool(tool_get_round_trip_prices, CITY_A, CITY_B)

# 汇总所有测试

def run_all_tests():
    tests = [
        test_get_airport_code,
        test_list_supported_cities,
        test_get_ticket_price_by_date,
        test_get_all_ticket_prices,
        test_get_lowest_ticket_price,
        test_get_round_trip_prices
    ]
    results = {}
    for test in tests:
        name, passed, err, result = test()
        results[name] = {"pass": passed, "error": err, "result": result}
    all_pass = all(v["pass"] for v in results.values())
    return mcp_response(all_pass, results, None if all_pass else "部分MCP工具返回结构不合规")

if __name__ == "__main__":
    import pprint
    pprint.pprint(run_all_tests()) 