import requests


def login():
    url = "http://localhost:5000/staff/login"
    data = {"s_username": "andrew32", "s_password": "password123"}
    response = requests.post(url, json=data)
    print(response.content)


def logout():
    url = "http://localhost:5000/staff/logout"
    response = requests.get(url)
    print(response.raw)


login()
# import time
# time.sleep(2)
# logout()
