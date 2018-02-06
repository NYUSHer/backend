from urllib import request, parse

def login_test():
    test_data = {"email": "masaki@gmail.com", "passwdtoken": "e27bbaa25e61:c28d7a9a8d9fde8a82008d54b38dab981d6730be"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://0.0.0.0:8084/auth/login"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    #assert(response["status"] == True)
    #assert(data["username"] == )
    print(res)

def register_test():
    test_data = {"email": "gg@gmail.com", "username": "gg", "passwdtoken": "ghashed_password"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://0.0.0.0:8084/auth/register"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    print(res)

def auth_test():
    test_data = {"user_id": 1, "user_token":"3b355d73-9bfd-45bf-943e-91a05f3eb932"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://0.0.0.0:8084/auth/authtest"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    print(res)


auth_test()
