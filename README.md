[简体中文 | Chinese](./README.zh-CN.md)

# CarrotAI-PRC-AirPrice

> 🚄 **Real-time Flight Ticket Price Query MCP Service for China**

---

## 🌟 Highlights
- Query real-time flight ticket prices, lowest prices in a range, and round-trip prices between major Chinese cities
- Support for city list, specific date, and date range queries
- Streamable-HTTP support
- Easy deployment, out-of-the-box

---

## ℹ️ Overview
CarrotAI-PRC-AirPrice is a flight ticket price query service based on the [MCP (Model Context Protocol)](https://modelcontextprotocol.io/introduction), designed for AI large models and agent ecosystems. It can query real-time flight ticket prices between major Chinese cities, support lowest price, round-trip, and range queries, and is suitable for integration into various AI applications, chatbots, and intelligent assistants.

- **Sponsor**: Power By [JinTongShu](https://jintongshu.com/)
- **Ad**: Highly recommend the powerful AI Agent platform 👉 [CarrotAI](https://github.com/Xingsandesu/CarrotAI)

---

## 🚀 Features

### 1. Supported API Tools
- `get_ticket_price_by_date(start_city, end_city, date)`
    - Query ticket price for a specific date
- `get_all_ticket_prices(start_city, end_city, start_date, end_date)`
    - Query all ticket prices in a date range
- `get_lowest_ticket_price(start_city, end_city, start_date, end_date)`
    - Query the lowest ticket price in a date range
- `get_round_trip_prices(start_city, end_city, start_date, end_date)`
    - Query round-trip ticket prices

### 2. Typical Usage Scenarios
- Query flight price from Beijing to Shanghai
- Query flight price from Shanghai to Beijing
- Query round-trip ticket price from Beijing to Shanghai
- Query the lowest ticket price this week from Beijing to Shanghai
- Query ticket price from Beijing to Guangzhou on May 1st

---

## 🛠️ Installation & Running

### 1. Requirements
- Python >= 3.12

### 2. Install dependencies
```bash
uv sync
```

### 3. Start the service
```bash
uv run main.py
```
Default port: `20001`

---

## 🤖 Integrate with CarrotAI

Just 3 steps to use this service on the [CarrotAI](https://github.com/Xingsandesu/CarrotAI) platform:
1. Start this service (see above)
2. Copy the `airprice.json` file to the `backend/config/app/` directory of CarrotAI
3. Restart the backend

CarrotAI will automatically detect and integrate this MCP service, no extra configuration needed.

---

## 📄 License & Copyright

- This project is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)

---

## 💬 Feedback & Contribution

Issues, PRs, and suggestions are welcome!

---

## 🔗 Related Links
- [CarrotAI Official Repository](https://github.com/Xingsandesu/CarrotAI)
- [MCP Protocol & Ecosystem](https://github.com/punkpeye/awesome-mcp-clients)
- [JinTongShu](https://jintongshu.com/)

---
