import re
import subprocess
from influxdb import InfluxDBClient

response = subprocess.Popen('/usr/bin/speedtest', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload =  re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)

ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)

speed_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "RaspberryPi"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping)
        }
    }
]
client = InfluxDBClient('localhost', 8086, 'speedmonitor', 'Azertyu1', 'internetspeed')

client.write_points(speed_data)
