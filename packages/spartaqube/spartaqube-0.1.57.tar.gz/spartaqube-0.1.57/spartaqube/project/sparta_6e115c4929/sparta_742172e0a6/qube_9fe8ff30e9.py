import re,os,json,requests
from datetime import datetime
from packaging.version import parse
from project.models import AppVersioning
from project.logger_config import logger
import pytz
UTC=pytz.utc
proxies_dict={'http':os.environ.get('http_proxy',None),'https':os.environ.get('https_proxy',None)}
def sparta_8ebd1017c8():0
def sparta_1cedff4abb():A='name';B='https://api.github.com/repos/SpartaQube/spartaqube-version/tags';C=requests.get(B,proxies=proxies_dict);D=json.loads(C.text);E=max(D,key=lambda t:parse(t[A]));return E[A]
def sparta_3dc5d494b6():A='https://spartaqube-version.pages.dev/latest_version.txt';B=requests.get(A,proxies=proxies_dict);return B.text.split('\n')[0]
def sparta_a8d20f981f():
	try:A='https://pypi.org/project/spartaqube/';B=requests.get(A,proxies=proxies_dict).text;C=re.search('<h1 class="package-header__name">(.*?)</h1>',B,re.DOTALL);D=C.group(1);E=D.strip().split('spartaqube ')[1];return E
	except:pass
def sparta_e326930263():
	B=os.path.dirname(__file__);C=os.path.dirname(B);D=os.path.dirname(C);E=os.path.dirname(D)
	try:
		with open(os.path.join(E,'app_version.json'),'r')as F:G=json.load(F);A=G['version']
	except:A='0.1.1'
	return A
def sparta_3cf1330e95():
	G='res'
	try:
		B=sparta_e326930263();A=sparta_3dc5d494b6();logger.debug(f"current_version: {B} and latest_version {A}");D=AppVersioning.objects.all();E=datetime.now().astimezone(UTC)
		if D.count()==0:AppVersioning.objects.create(last_available_version_pip=A,last_check_date=E)
		else:C=D[0];C.last_available_version_pip=A;C.last_check_date=E;C.save()
		return{'current_version':B,'latest_version':A,'b_update':not B==A,'humanDate':'A moment ago',G:1}
	except Exception as F:logger.debug('Exception versioning update');logger.debug(F);return{G:-1,'errorMsg':str(F)}