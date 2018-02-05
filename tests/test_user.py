from urllib import request, parse

def login_test():
    test_data = {"email": "gg@gmail.com", "passwdtoken": "ghashed_password"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://127.0.0.1:8084/auth/login"  # Adjust port
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
    requrl = "http://127.0.0.1:8084/auth/register"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    print(res)


login_test()