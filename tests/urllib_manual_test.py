import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urllib import request, parse


def login_test():
    test_data = {"email": "lihongyigg@163.com", "passwdtoken": "NYUSHer_by_email_login"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://localhost:8080/auth/login"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    #assert(response["status"] == True)
    #assert(data["username"] == )
    print(res)


def register_test():
    test_data = {"email": "hl2752@nyu.edu", "username": "maxee", "passwdtoken": "202cb962ac59075b964b07152d234b70"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://0.0.0.0:8080/auth/register"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    print(res)


def set_test():
    test_data = {"user_id": 1, "user_token":"3a5c1331-9445-4ff3-b3f6-d1527c02c7f5"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://0.0.0.0:8084/auth/authtest"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    print(res)
