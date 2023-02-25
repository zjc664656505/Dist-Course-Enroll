import sys
import json
import requests
from flask import Flask, request, jsonify
import config
app = Flask(__name__)
server = None

######
# records = {
#           max: "20"
#           students: ["john", "peter"]
#           }
#####

class Server:
    def __init__(self, serverId):
        self.serverId = serverId
        ass = requests.get("http://" + config.balancer_ip + ":" + config.balancer_port + "/up?serverId=" + str(serverId))
        self.assignment = json.loads(ass.content)

        self.url = "http://" + config.backend_addr
        url = self.url + "/list?low=" + str(self.assignment[0]) + "&high=" + str(self.assignment[1])
        
        content = requests.get(url, verify=False).content
        self.records = json.loads(content)


@app.route('/insert', methods=['GET'])
def insert_record():
    classId = request.args.get('classId')
    student = request.args.get('student')

    cls = server.records[classId]
    if len(cls["students"]) >= int(cls["max"]):
        return jsonify({'error': 'class is full'})

    if cls["students"].count(student) != 0:
        return jsonify({'error': 'already enrolled'})

    server.records[classId]["students"].append(student)
    url = server.url + "/insert?classId=" + classId + "&student=" + student

    # send to backend
    # requests.get(url, verify=False)

    return jsonify({'success': 'success'})


@app.route('/delete', methods=['GET'])
def delete_record():
    classId = request.args.get('classId')
    student = request.args.get('student')

    cls = server.records[classId]
    if cls["students"].count(student) == 0:
        return jsonify({'error': 'did not enroll this class'})

    server.records[classId]["students"].remove(student)
    url = server.url + "/delete?classId=" + classId + "&student=" + student

    # send to backend
    # requests.get(url, verify=False)

    return jsonify({'success': 'success'})


@app.route('/reconfig', methods=['GET'])
def reconfig():
    first = request.args.get('first')
    second = request.args.get('second')

    url = server.url + "/list?low=" + first + "&high=" + second
    server.records = json.loads(requests.get(url, verify=False).content)

    return jsonify({'success': 'success'})


@app.route('/records', methods=['GET'])
def get_record():
    records = []

    for idx, cls in server.records.items():
        for stu in cls["students"]:
            records.append([idx, stu])

    return jsonify(records)


if __name__ == '__main__':
    serverId = int(sys.argv[1])
    server = Server(serverId)
    app.run(host=config.server_ips[serverId], port=config.server_ports[serverId])
