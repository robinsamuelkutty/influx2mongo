#  InfluxDB to MongoDB Atlas Connector

> A simple Python project to insert time-series data into InfluxDB (OSS 2.x) and back it up to MongoDB Atlas — perfect for IoT, analytics, or personal monitoring projects.

---

## 📌 What is this?

This project shows how to:
- Set up **InfluxDB OSS 2.x** locally (with UI and token support)
- Write and query **time-series data** using Python
- Store/backup that data into **MongoDB Atlas**

---

## 🧰 Tech Stack

| Tool       | Purpose                          |
|------------|----------------------------------|
| InfluxDB OSS 2.x | Time-series database (local) |
| MongoDB Atlas    | Cloud document DB (backup)   |
| Python           | Data pipeline logic          |
| influxdb-client  | Python client for InfluxDB   |
| pymongo          | Python client for MongoDB    |

---

## ⚙️ Step-by-Step Setup

### 🔷 Step 1: Install InfluxDB OSS 2.x Locally

Go to 👉 [https://portal.influxdata.com/downloads](https://portal.influxdata.com/downloads)

➡ Scroll down to **InfluxDB OSS 2.x**  
➡ Choose your OS and download:

- **Windows** → `.zip installer`
- **Linux/macOS** → `.tar.gz` or install via `apt/yum`

🧭 After install:

- Run `influxd`
- Open browser: `http://localhost:8086`
- Create:
  - Organization (e.g. `RescueLink`)
  - Bucket (e.g. `sensor-data`)
  - All-Access Token (copy it!)

---

### 🔷 Step 2: Set Token in Terminal

In PowerShell:
```powershell
$env:INFLUXDB_TOKEN = "<your_token_here>"
```
## 🔷 Step 3: Install Dependencies

```bash
pip install influxdb-client pymongo
```
## 🔷Step 4: Insert Data into InfluxDB
```bash
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Set token, org, and URL
token = os.environ.get("INFLUXDB_TOKEN")
org = "RescueLink"
url = "http://localhost:8086"
bucket = "sensor-data"

# Initialize client
write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Create a data point
point = (
    Point("weather")
    .tag("location", "Cochin")
    .field("temperature", 29)
    .field("humidity", 82)
    .time(time.time_ns(), WritePrecision.NS)
)

write_api.write(bucket=bucket, org=org, record=point)
print("✅ Dummy data written to InfluxDB.")
```
##🔷 Step 5: Query Data from InfluxDB
```bash
query_api = write_client.query_api()

query = """
from(bucket: "sensor-data")
|> range(start: -1h)
|> filter(fn: (r) => r._measurement == "weather")
"""

tables = query_api.query(query, org="RescueLink")

for table in tables:
    for record in table.records:
        print("Measurement:", record.get_measurement())
        print("Field:", record.get_field())
        print("Value:", record.get_value())
        print("Time:", record.get_time())
        print("Tags:", record.values)
        print("------")
```
## Use the influx_to_mongodb.py
## these all steps are explained very well in the localhost:8086 -> python section
