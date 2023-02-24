import json

import config
import requests

print(requests.get("http://localhost:3000/delete?classId=0&student=pp").content)
print(json.loads(requests.get("http://localhost:3000/records").content))
