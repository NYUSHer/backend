from urllib import request, parse

def login_test():
    test_data = {"email": "hibiki@gmail.com", "passwdtoken": "d077fac8-fe03-4178-844c-70b0cd44c9f9"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://127.0.0.1:8083/auth/login"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    #assert(response["status"] == True)
    #assert(data["username"] == )
    print(res)

def register_test():
    test_data = {"email": "hibiki@gmail.com", "username": "hibiki"}
    test_data_urlencode = parse.urlencode(test_data)
    test_data_urlencode = bytes(test_data_urlencode, "utf-8")
    requrl = "http://127.0.0.1:8083/auth/register"  # Adjust port
    req = request.Request(url=requrl, data=test_data_urlencode)
    res_data = request.urlopen(req)
    res = res_data.read()
    print(res)

login_test()