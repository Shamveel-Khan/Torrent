from flask import Flask, request, jsonify, abort
import threading
import requests
import json
import os

app = Flask(__name__)

os.makedirs("data", exist_ok=True)
if os.path.exists("data/data.json"):
    with open("data/data.json", "r") as f:
        files_ref = json.load(f)
else:
    files_ref = {
        'abc.txt': [
            {'peername': 'p1.txt', 'ip': '127.0.0.1', 'port': 8001}
        ]
    }
    with open("data/data.json", "w") as f:
        json.dump(files_ref, f, indent=4)

@app.route('/need/<filename>', methods=['GET'])
def need(filename):
    if filename not in files_ref:
        abort(404)
    return jsonify(files_ref[filename])

@app.route('/seed', methods=['POST'])
def seed():
    data = request.get_json()
    filename = data['filename']
    peername = data['peername']
    ip = data['ip']
    port = data['port']

    peer_info = {"peername": peername, "ip": ip, "port": port}

    if filename not in files_ref:
        files_ref[filename] = []

    files_ref[filename] = [p for p in files_ref[filename] if p.get('peername') != peername]

    files_ref[filename].append(peer_info)

    with open("data/data.json", "w") as f:
        json.dump(files_ref, f, indent=4)

    return jsonify({"ok": True, "message": f"{peername} is now seeding {filename}"}), 200

def run_server():
    app.run(host="127.0.0.1", port=5005, debug=False, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()

    tracker = 'http://127.0.0.1:5005'

    while True:
        cmd = input("input: ").strip().upper()

        if cmd=='Q':
            break
        elif cmd=='GET':
            path = input("Path: ").strip()
            r=requests.get(tracker+path)
            print(f"code: {r.status_code}, text: {r.text}")

        elif cmd == "POST":
            path = input("path (e.g. /seed): ").strip()
            key1 = input("key1 name (e.g. filename): ").strip()
            val1 = input(f"{key1}: ").strip()
            key2 = input("key2 name (e.g. peername): ").strip()
            val2 = input(f"{key2}: ").strip()
            key3 = input("key3 name (e.g ip): ").strip()
            val3 = input(f"{key3}: ").strip()
            key4 = input("key4 name (e.g port): ").strip()
            val4 = input(f"{key4}: ").strip()
            r = requests.post(tracker + path, json={key1: val1, key2: val2, key3: val3, key4: val4})
            print(r.status_code, r.text)

        else:
            print("unknown")