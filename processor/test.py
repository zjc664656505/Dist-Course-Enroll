import requests
import json

print(requests.get("http://127.0.0.1:3000/records").content)
print(requests.get("http://127.0.0.1:3000/login?studentId=1&studentName=Yurun").content)
#print(json.loads(requests.get("http://127.0.0.1:3000/records").content))
print(requests.get("http://127.0.0.1:3000/records").content)
