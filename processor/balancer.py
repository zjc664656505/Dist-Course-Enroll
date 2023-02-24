import json
import random
import sys

import requests
from flask import Flask, request, jsonify
import config
app = Flask(__name__)
Assignment = [(0, 3), (3, 6), (6, 10)]
Alive = 7

def get_server(classId):
    serverIndex = -1
    for index, assign in enumerate(Assignment):
        if assign is not None and assign[0] <= classId < assign[1]:
            serverIndex = index
            break

    if serverIndex == -1:
        return -1, ""

    url = "http://" + config.server_ips[serverIndex] + ":" + config.server_ports[serverIndex]
    return serverIndex, url


def reconfig(serverId=None):
    global Assignment
    global Alive
    if Alive == 7:
        Assignment = [(0, 3), (3, 6), (6, 10)]
    elif Alive == 6:
        Assignment = [None, (0, 5), (5, 10)]
    elif Alive == 5:
        Assignment = [(0, 5), None, (5, 10)]
    elif Alive == 4:
        Assignment = [None, None, (0, 10)]
    elif Alive == 3:
        Assignment = [(0, 5), (5, 10), None]
    elif Alive == 2:
        Assignment = [None, (0, 10), None]
    elif Alive == 1:
        Assignment = [(0, 10), None, None]

    print("New assignment: " + str(Assignment), flush=True)
    # send reconfig to servers
    for index, assign in enumerate(Assignment):
        if assign is not None and index != serverId:
            _, url = get_server(assign[0])
            url += "/reconfig?first="+str(assign[0])+"&second="+str(assign[1])
            requests.get(url, verify=False)
    print("Reconfiguration finished", flush=True)

def operate_record(classId, student, mode):
    global Alive
    serverId, url = get_server(classId)
    if serverId == -1:
        return jsonify({'error': 'wrong classId'})

    url += "/" + mode + "?classId=" + str(classId) + "&student=" + student

    try:
        return requests.get(url, verify=False, timeout=2).content
    except:
        print("server " + str(serverId) + " failed", flush=True)
        Alive -= 1 << serverId
        reconfig()
        serverId, url = get_server(classId)
        url += "/" + mode + "?classId=" + str(classId) + "&student=" + student
        return requests.get(url, verify=False).content


@app.route('/insert', methods=['GET'])
def insert_record():
    classId = int(request.args.get('classId'))
    student = request.args.get('student')

    return operate_record(classId, student, "insert")


@app.route('/delete', methods=['GET'])
def delete_record():
    classId = int(request.args.get('classId'))
    student = request.args.get('student')

    return operate_record(classId, student, "delete")

@app.route('/up', methods=['GET'])
def server_up():
    global Alive
    serverId = int(request.args.get('serverId'))
    bit = 1 << serverId
    if Alive & bit == 0:
        Alive += bit
        print("server" + str(serverId) + " joined", flush=True)
        reconfig(serverId)

    return jsonify(Assignment[serverId])

@app.route('/records', methods=['GET'])
def get_record():
    records = []
    for index, assign in enumerate(Assignment):
        if assign is not None:
            _, url = get_server(assign[0])
            url += "/records"
            records += json.loads(requests.get(url, verify=False).content)

    return jsonify(records)

# For testing only
@app.route('/list', methods=['GET'])
def list_all():
    first = request.args.get('first')
    second = request.args.get('second')

    records = {}
    for i in range(int(first), int(second)):
        cls = {"classId": str(i), "max": random.randint(20, 40), "students": ["john"]}
        records[str(i)] = cls

    return jsonify(records)

if __name__ == '__main__':
    app.run(host=config.balancer_ip, port=config.balancer_port)
