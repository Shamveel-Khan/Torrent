import requests

tracker = 'http://127.0.0.1:5005'

while True:
    cmd = input("input: ").strip().upper()

    if cmd=='Q':
        break
    elif cmd=='GET':
        path = input("Path: ").strip()
        r=requests.get(tracker+path)
        print(f"code: {r.status_code}, text{r.text}")

    elif cmd == "POST":
        path = input("path (e.g. /seed): ").strip()
        key1 = input("key1 name (e.g. filename): ").strip()
        val1 = input(f"{key1}: ").strip()
        key2 = input("key2 name (e.g. peername): ").strip()
        val2 = input(f"{key2}: ").strip()
        r = requests.post(tracker + path, json={key1: val1, key2: val2})
        print(r.status_code, r.text)

    else:
        print("unknown")
