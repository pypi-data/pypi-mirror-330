import os,sys,shutil,simplejson as json,datetime
from pathlib import Path
from datetime import datetime
from spartaqube_app.path_mapper_obf import sparta_dd73beab70
from project.logger_config import logger
main_api=sparta_dd73beab70()['api']
sys.path.insert(0,main_api)
from spartaqube_utils import is_scalar,safe_to_json,rename_duplicate_columns,convert_dataframe_to_json,convert_to_dataframe,convert_to_dataframe_func
def sparta_fb8244f3ba(path):
	with open(path,'a'):os.utime(path,None)
def sparta_aa4b3515e2(path):A=Path(path).resolve();return str(A)
def sparta_ed386396f8(textOutputArr):
	A=textOutputArr
	try:A=[A for A in A if len(A)>0];A=[A for A in A if A!='Welcome to SpartaQube API'];A=[A for A in A if A!="<span style='color:#0ab70a'>You are logged</span>"];A=[A for A in A if A!='You are logged']
	except Exception as B:pass
	return A
def sparta_737a06c12a(input2JsonEncode,dateFormat=None):
	C=dateFormat;import numpy as B
	class D(json.JSONEncoder):
		def default(E,obj):
			A=obj
			if isinstance(A,B.integer):return int(A)
			if isinstance(A,B.floating):return float(A)
			if isinstance(A,B.ndarray):return A.tolist()
			if isinstance(A,datetime.datetime):
				if C is not None:return A.strftime(C)
				else:return str(A)
			return super(D,E).default(A)
	A=json.dumps(input2JsonEncode,ignore_nan=True,cls=D);return A
def sparta_c16080fa22(path):
	A=path
	try:os.rmdir(A)
	except:
		try:os.system('rmdir /S /Q "{}"'.format(A))
		except:
			try:shutil.rmtree(A)
			except:
				try:os.remove(A)
				except:pass
def sparta_282eab3904(file_path):
	A=file_path
	try:os.remove(A);logger.debug(f"File '{A}' has been deleted.")
	except Exception as B:
		try:os.unlink(A);logger.debug(f"File '{A}' has been forcefully deleted.")
		except Exception as B:logger.debug(f"An error occurred while deleting the file: {B}")