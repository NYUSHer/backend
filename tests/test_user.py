from urllib import request, parse

test_data = {"email": "masaki@gmail.com", "passwordtoken": "rqemnwer341"}

test_data_urlencode = parse.urlencode(test_data)
test_data_urlencode = bytes(test_data_urlencode, "utf-8")

requrl = "http://127.0.0.1:5010/auth/login"

req = request.Request(url=requrl, data=test_data_urlencode)

res_data = request.urlopen(req)

res = res_data.read()

print(res)