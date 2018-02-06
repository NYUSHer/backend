from urllib import request, parse

def sendmail_test():
    requrl = "http://0.0.0.0:8084/post/sendmail"  # Adjust port
    req = request.Request(url=requrl)
    res_data = request.urlopen(req)
    res = res_data.read()
    print(res)

sendmail_test()