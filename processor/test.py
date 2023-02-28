import requests
import json
print(requests.get("http://127.0.0.1:3000/insert?classId=0&student=pp").content)
print(json.loads(requests.get("http://127.0.0.1:3000/records").content))
