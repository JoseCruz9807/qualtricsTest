from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import urllib
import sys
import requests
import os
import simplejson as json

def getReponse(d,dataCenter,apiToken):
    responseId = d['ResponseID']
    surveyId = d['SurveyID']

    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
       }

    url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/responses/{2}".format(dataCenter,surveyId,responseId)

    
    rsp = requests.get(url, headers=headers)
    print(rsp.json())


def parsey(c):
    x=c.decode().split("&")
    d = {}
    for i in x:
        a,b = i.split("=")
        d[a] = b

    d['CompletedDate'] = urllib.parse.unquote(d['CompletedDate'])

    return d

class Handler(BaseHTTPRequestHandler):

  # GET
  def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length)
        d = parsey(post_data)

        try:
           apiToken = os.environ.get('apiKey', None)#os.environ['APIKEY']
           dataCenter = os.environ.get('dataCenter', None)#os.environ['DATACENTER']
        except KeyError:
            print("set environment variables APIKEY and DATACENTER")
            sys.exit(2)

        getReponse(d,dataCenter,apiToken)
 
def run():

  print('starting server...')
  my_ip=str(requests.get('http://ip.42.pl/raw').text)
  print(my_ip)
  print(os.environ.get('port', None))
  print(os.environ.get('dataCenter', None))
  print(os.environ.get('apiKey', None))
  server_address = (my_ip, int(float(os.environ.get('port', None))))
 
  httpd = HTTPServer(server_address, Handler)
  print('running server...')
  httpd.serve_forever()
 

try: 
    run()
except KeyboardInterrupt:
    sys.exit(0)
