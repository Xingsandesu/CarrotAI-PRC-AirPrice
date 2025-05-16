# CarrotAI-PRC-AirPrice

> 🚄 **中国机票实时优惠信息查询MCP服务**

---

## 🌟 项目亮点
- 查询中国主要城市间的实时机票价格、区间最低价和往返票价
- 支持城市列表、指定日期、区间查询
- Streamable-HTTP 支持
- 部署简单，开箱即用

---

## ℹ️ 项目简介
CarrotAI-PRC-AirPrice 是一个基于 [MCP（Model Context Protocol）](https://modelcontextprotocol.io/introduction) 协议的机票价格查询服务，专为AI大模型和智能体生态设计。它可实时查询中国主要城市间的机票价格，支持最低价、往返票、区间查询等多种场景，适合集成到各类AI应用、对话机器人、智能助手等系统。

- **赞助商**：Power By [金桐树](https://jintongshu.com/)
- **广告**：强烈推荐体验更强大的AI Agent平台 👉 [CarrotAI](https://github.com/Xingsandesu/CarrotAI)

---

## 🚀 功能一览

### 1. 支持的API工具
- `get_ticket_price_by_date(start_city, end_city, date)`
    - 查询指定日期的机票价格
- `get_all_ticket_prices(start_city, end_city, start_date, end_date)`
    - 查询区间内所有机票价格
- `get_lowest_ticket_price(start_city, end_city, start_date, end_date)`
    - 查询区间内最低价格机票
- `get_round_trip_prices(start_city, end_city, start_date, end_date)`
    - 查询往返机票价格

### 2. 典型用法示例
- 查询北京到上海的机票价格
- 查询上海到北京的机票价格
- 查询北京到上海的往返机票价格
- 查询北京到上海本周最低机票价
- 查询北京到广州5月1日的机票价格

---

## 🛠️ 安装与运行

### 1. 环境要求
- Python >= 3.12

### 2. 安装依赖
```bash
uv sync
```

### 3. 启动服务
```bash
uv run main.py
```
默认监听端口：`20001`

---

## 🤖 集成到萝卜AI（CarrotAI）

只需三步，即可在[萝卜AI](https://github.com/Xingsandesu/CarrotAI)平台上使用本服务：
1. 启动本服务（见上文）
2. 将 `airprice.json` 文件复制到 CarrotAI 的 `backend/config/app/` 目录下
3. 重启后端

CarrotAI 会自动识别并集成该MCP服务，无需额外配置。

---

## 📄 协议与版权

- 本项目采用 [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)

---

## 💬 反馈与贡献

欢迎提交 Issue、PR 或建议！

---

## 🔗 相关链接
- [CarrotAI (萝卜AI) 官方仓库](https://github.com/Xingsandesu/CarrotAI)
- [MCP 协议与生态](https://github.com/punkpeye/awesome-mcp-clients)
- [金桐树](https://jintongshu.com/)

--- 