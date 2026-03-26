import requests

def verify_service():
    try:
        r = requests.get("http://localhost:80")
        return r.status_code == 200
    except:
        return False
