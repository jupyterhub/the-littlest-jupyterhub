import requests

def test_hub_up():
    r = requests.get('http://127.0.0.1')
    r.raise_for_status()
