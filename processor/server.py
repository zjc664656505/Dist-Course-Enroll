import sys
import json
import requests
from flask import Flask, request, jsonify
from multiprocessing import Lock
import threading
import config
app = Flask(__name__)
server = None

######
# records = {
#           Max: "20"
#           students: [
#            {"name" : "john", "id" : "123"}
#            ]
#           }
#####

class Server:
    def __init__(self, serverId):
        self.serverId = serverId
        ass = requests.get("http://" + config.balancer_ip + ":" + config.balancer_port + "/up?serverId=" + str(serverId))
        assignment = json.loads(ass.content)

        self.url = "http://" + config.backend_addr + "/api"
        self.records = None
        self.locks = {}
        self.reconfig(str(assignment[0]), str(assignment[1]))

    def reconfig(self, low, high):
        url = self.url + "/info"

        content = requests.get(url, verify=False).content
        records = json.loads(content)

        l = int(low)
        h = int(high)

        print(l)
        print(h)

        self.records = {}
        self.locks = {}
        for k in records.keys():
            id = int(k)

            if l <= id < h:
                students = [stu["name"] for stu in records[k]["student"]]
                ids = [stu["id"] for stu in records[k]["student"]]

                self.records[k] = {
                    "student": students,
                    "id": ids,
                    "Max": records[k]["Max"]
                }
                self.locks[k] = Lock()
        print(self.records)

def insert_thread(classId, studentId, studentName):
    with server.locks[classId]:
        if server.records[classId]["id"].count(studentId) != 0:
            return jsonify({'error': 'already registered'})
        server.records[classId]["id"].append(studentId)
        server.records[classId]["student"].append(studentName)
        url = server.url + "/add/" + str(studentId) + "/" + classId
        # send to backend
        requests.get(url, verify=False)


@app.route('/insert', methods=['GET'])
def insert_record():
    classId = request.args.get('classId')
    studentId = int(request.args.get('studentId'))
    student = request.args.get('studentName')

    current = len(server.records[classId]["id"])
    if current < config.quick_response_ratio * server.records[classId]["Max"]\
            and server.records[classId]["id"].count(studentId) == 0:
        print("quick response", flush=True)
        # start thread for actual insertion
        threading.Thread(target=insert_thread, args=(classId, studentId, student)).start()

        # quick response with success
        return jsonify({'success': 'success'})

    print("slow response", flush=True)
    with server.locks[classId]:
        cls = server.records[classId]
        if len(cls["student"]) >= int(cls["Max"]):
            return jsonify({'error': 'class is full'})
        print(cls["id"].count(studentId))
        if cls["id"].count(studentId) != 0:
            return jsonify({'error': 'already registered'})
        server.records[classId]["id"].append(studentId)
        server.records[classId]["student"].append(student)
        url = server.url + "/add/" + studentId + "/" + classId
        # send to backend
        requests.get(url, verify=False)

        return jsonify({'success': 'success'})


@app.route('/delete', methods=['GET'])
def delete_record():
    classId = request.args.get('classId')
    studentId = int(request.args.get('studentId'))
    student = request.args.get('studentName')

    with server.locks[classId]:
        cls = server.records[classId]
        if cls["id"].count(studentId) == 0:
            return jsonify({'error': 'did not enroll this class'})

        server.records[classId]["student"].remove(student)
        server.records[classId]["id"].remove(studentId)
        url = server.url + "/delete/" + str(studentId) + "/" + classId

        # send to backend
        requests.get(url, verify=False)

        return jsonify({'success': 'success'})


@app.route('/reconfig', methods=['GET'])
def reconfig():
    first = request.args.get('first')
    second = request.args.get('second')

    server.reconfig(first, second)

    return jsonify({'success': 'success'})


@app.route('/records', methods=['GET'])
def get_record():
    records = []

    for k, cls in server.records.items():
        for idx, name in enumerate(cls["student"]):
            records.append([cls["id"][idx], name, k])

    return jsonify(records)


if __name__ == '__main__':
    serverId = int(sys.argv[1])
    server = Server(serverId)
    app.run(host=config.server_ips[serverId], port=config.server_ports[serverId], threaded=True)
