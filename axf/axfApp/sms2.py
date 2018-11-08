#-*- coding:utf-8 -*-
import http.client
import urllib
host  = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"
account  = "C22733402"
password = "9652df308ba18d252cd28b1fa83addff"

def send_sms(text, mobile):
    params = urllib.parse.urlencode({'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' })
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str 

if __name__ == '__main__':

    mobile = "18500648122"

    text = "您的验证码是：678901。请不要把验证码泄露给其他人。"

    print(send_sms(text, mobile))