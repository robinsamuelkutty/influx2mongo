from influxdb_client import InfluxDBClient
from pymongo import MongoClient
import os

#  InfluxDB Setup 
token = os.environ.get("INFLUXDB_TOKEN")  # you already exported this
org = "RescueLink"
url = "http://localhost:8086"
bucket = "testbucket"

influx_client = InfluxDBClient(url=url, token=token, org=org)
query_api = influx_client.query_api()

query = """
from(bucket: "testbucket")
|> range(start: -1h)
|> filter(fn: (r) => r._measurement == "measurement1")
"""

tables = query_api.query(query, org=org)

#  MongoDB Setup 
mongo_uri = "your mongodb atlas uri"
mongo_client = MongoClient(mongo_uri)
mongo_collection = mongo_client["influx_backup"]["sensor_data"]

# Transfer Data 
count = 0
for table in tables:
    for record in table.records:
        doc = {
            "measurement": record.get_measurement(),
            "field": record.get_field(),
            "value": record.get_value(),
            "tags": record.values,
            "time": str(record.get_time())
        }
        mongo_collection.insert_one(doc)
        count += 1

print(f"✅ {count} records inserted into MongoDB Atlas.")
