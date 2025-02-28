import json,base64,asyncio,subprocess,uuid,os,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_484a14773c.sparta_88433fd91c import qube_353c7b61a4 as qube_353c7b61a4
from project.sparta_484a14773c.sparta_b7c52b6e7f import qube_824936dc46
from project.sparta_484a14773c.sparta_174d7f1491 import qube_de9f73339e as qube_de9f73339e
from project.sparta_484a14773c.sparta_b7c52b6e7f.qube_c3c81d82c4 import Connector as Connector
from project.logger_config import logger
def sparta_3f3b3d3e2d(json_data,user_obj):
	D='key';A=json_data;logger.debug('Call autocompelte api');logger.debug(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_263fb7c2e9(B)
	return{'res':1,'output':C,D:B}
def sparta_263fb7c2e9(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";H={'http':os.environ.get('http_proxy',None),'https':os.environ.get('https_proxy',None)};C=requests.get(G,proxies=H)
	try:
		if int(C.status_code)==200:
			I=json.loads(C.text);D=I['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]