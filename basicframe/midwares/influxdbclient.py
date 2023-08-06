import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "Sl4Mb6TgyMUis0ic74QWJnVV3G8k6Ic_FSAoRKgtndspoQIsYiKsNKCkPyFrZbIDzMQs6CSM8cvt22ZYmFiMUg=="
org = "ptking"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


bucket = "monitor"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

for value in range(1000000):
    point = (
        Point("measurement1")
        .tag("tagname1", "tagvalue1")
        .field("field1", value)
    )
    write_api.write(bucket=bucket, org="ptking", record=point)
    time.sleep(0.01)  # separate points by 1 second