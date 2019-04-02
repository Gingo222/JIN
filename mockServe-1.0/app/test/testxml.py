from suds.client import Client
import logging

client = Client("http://%s:%s/?wsdl" % ('127.0.0.1', 8002))

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
ret = client.service.helloGingo("xml1", cache=None)
print ret
