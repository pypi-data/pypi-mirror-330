import os,json,base64,json
def sparta_be18fe394d():A=os.path.dirname(__file__);B=os.path.dirname(A);return json.loads(open(B+'/platform.json').read())['PLATFORM']
def base64ToString(b):return base64.b64decode(b).decode('utf-8')
def stringToBase64(s):return base64.b64encode(s.encode('utf-8'))