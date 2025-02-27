_M='%Y-%m-%d %H:%M:%S'
_L='created_time_str'
_K='workspace_variables'
_J='app.settings'
_I='venvName'
_H='kernelType'
_G='created_time'
_F='kernel_manager_uuid'
_E='name'
_D='-1'
_C='kernelManagerUUID'
_B='res'
_A=None
import os,sys,gc,json,base64,shutil,zipfile,io,uuid,cloudpickle
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC=pytz.utc
from django.contrib.humanize.templatetags.humanize import naturalday
from project.sparta_6e115c4929.sparta_acc02e4304.qube_7588e90133 import IPythonKernel as IPythonKernel
from project.sparta_6e115c4929.sparta_cf4e6e64e0.qube_fd6518ecaf import sparta_1f4d8fdfb5,sparta_b9a80cefc0,sparta_b1c82099aa
class SqKernelManager:
	def __init__(A,kernel_manager_uuid,type,name,user,user_kernel=_A,project_folder=_A,notebook_exec_id=_D,dashboard_exec_id=_D,venv_name=_A):
		C=user_kernel;B=user;A.kernel_manager_uuid=kernel_manager_uuid;A.type=type;A.name=name;A.user=B;A.kernel_user_logged=B;A.project_folder=project_folder
		if C is _A:C=B
		A.user_kernel=C;A.venv_name=venv_name;A.notebook_exec_id=notebook_exec_id;A.dashboard_exec_id=dashboard_exec_id;A.is_init=False;A.created_time=datetime.now()
	def create_kernel(A,django_settings_module=_A):
		if A.notebook_exec_id!=_D:A.user_kernel=sparta_b9a80cefc0(A.notebook_exec_id)
		if A.dashboard_exec_id!=_D:A.user_kernel=sparta_b1c82099aa(A.dashboard_exec_id)
		B=sparta_1f4d8fdfb5(A.user_kernel);A.ipython_kernel=IPythonKernel(api_key=B,django_settings_module=django_settings_module,project_folder=A.project_folder)
		if A.venv_name is not _A:A.ipython_kernel.activate_venv(A.venv_name)
		settings.GLOBAL_KERNEL_MANAGER[A.kernel_manager_uuid]=A
def sparta_7dafd3fdae(kernel_manager_obj):return kernel_manager_obj.ipython_kernel.get_kernel_memory_size()
def sparta_db59845487(kernel_manager_obj):return kernel_manager_obj.ipython_kernel.list_workspace_variables()
def sparta_b258446937(user_obj,kernel_manager_uuid):
	A=kernel_manager_uuid
	if A in settings.GLOBAL_KERNEL_MANAGER:
		B=settings.GLOBAL_KERNEL_MANAGER[A]
		if B.user==user_obj:return B
def sparta_5c6f6b98d4(user_obj,kernel_manager_uuid):
	A=sparta_b258446937(user_obj,kernel_manager_uuid)
	if A is not _A:return A.ipython_kernel
def sparta_1e6c849eae(json_data,user_obj):
	E=user_obj;A=json_data;G=A[_C];B=int(A[_H]);H=A.get(_E,'undefined');C=A.get('fullpath',_A);I=A.get('notebookExecId',_D);J=A.get('dashboardExecId',_D);D=A.get(_I,'')
	if len(D)==0:D=_A
	if C is not _A:C=os.path.dirname(C)
	F=SqKernelManager(G,B,H,E,user_kernel=E,project_folder=C,notebook_exec_id=I,dashboard_exec_id=J,venv_name=D)
	if B==3 or B==4 or B==5:F.create_kernel(django_settings_module=_J)
	else:F.create_kernel()
	return{_B:1}
def sparta_2f9da6b84b(json_data,user_obj):
	D=user_obj;B=json_data[_C];E=sparta_5c6f6b98d4(D,B)
	if E is not _A:
		A=settings.GLOBAL_KERNEL_MANAGER[B];C=A.type;F=A.name;G=A.project_folder;H=A.notebook_exec_id;I=A.dashboard_exec_id;J=A.user_kernel;K=A.venv_name;settings.GLOBAL_KERNEL_MANAGER[B]=_A;gc.collect();A=SqKernelManager(B,C,F,D,user_kernel=J,project_folder=G,notebook_exec_id=H,dashboard_exec_id=I,venv_name=K)
		if C==3 or C==4 or C==5:A.create_kernel(django_settings_module=_J)
		else:A.create_kernel()
	return{_B:1}
def sparta_609037b11d(json_data,user_obj):
	A=json_data
	if _C in A:
		C=A[_C];D=A['env_name'];B=sparta_5c6f6b98d4(user_obj,C)
		if B is not _A:B.activate_venv(D)
	return{_B:1}
def sparta_aa6cf78931(json_data,user_obj):
	B=json_data[_C];A=sparta_b258446937(user_obj,B)
	if A is not _A:C=sparta_7dafd3fdae(A);D=A.ipython_kernel;E=D.list_workspace_variables();return{_B:1,'kernel':{_K:E,_F:B,'kernel_size':C,'type':A.type,_E:A.name,_L:str(A.created_time.strftime(_M)),_G:naturalday(parser.parse(str(A.created_time)))}}
	return{_B:-1}
def sparta_91bf5424a3(json_data,user_obj):
	B=json_data;D=B[_C];C=B['varName'];A=sparta_5c6f6b98d4(user_obj,D)
	if A is not _A:A.get_workspace_variable(C);E=A.get_kernel_variable_repr(C);return{_B:1,'htmlReprDict':E}
	return{_B:-1}
def sparta_3c9fd44ec5(json_data,user_obj):
	A=json_data;D=A[_C];B=sparta_b258446937(user_obj,D)
	if B is not _A:
		C=A.get(_E,_A)
		if C is not _A:B.name=C
	return{_B:1}
def sparta_612586cbcd(json_data,user_obj):
	H='b_require_workspace_variables';D=user_obj;C=json_data;I=C['b_require_size'];J=C[H];K=C[H];L=[A for(B,A)in settings.GLOBAL_KERNEL_MANAGER.items()if A.user==D];E=[]
	if K:from project.sparta_6e115c4929.sparta_2add38e938 import qube_6f3e0ed78d as M;E=M.sparta_79ace01bf6(D)
	B=[]
	for A in L:
		F=_A
		if I:F=sparta_7dafd3fdae(A)
		G=[]
		if J:G=sparta_db59845487(A)
		B.append({_F:A.kernel_manager_uuid,_K:G,'type':A.type,_E:A.name,_L:str(A.created_time.strftime(_M)),_G:naturalday(parser.parse(str(A.created_time))),'size':F,'isStored':True if A.kernel_manager_uuid in E else False})
	if len(B)>0:B=sorted(B,key=lambda x:x[_G])
	return{_B:1,'kernels':B}
def sparta_480b6e178b(json_data,user_obj):from project.sparta_6e115c4929.sparta_2add38e938 import qube_6f3e0ed78d as B;A=B.sparta_75fd077d49(user_obj);C=list(settings.GLOBAL_KERNEL_MANAGER.keys());A=[A for A in A if A[_F]not in C];return{_B:1,'kernel_library':A}
def sparta_d93dcb6682(json_data,user_obj):
	A=json_data[_C];B=sparta_5c6f6b98d4(user_obj,A)
	if B is not _A:del settings.GLOBAL_KERNEL_MANAGER[A]
	return{_B:1}
def sparta_13151136bb(json_data,user_obj):
	A=[A for(A,B)in settings.GLOBAL_KERNEL_MANAGER.items()if B.user==user_obj]
	for B in A:del settings.GLOBAL_KERNEL_MANAGER[B]
	return{_B:1}
def sparta_9e50660852(json_data,user_obj):
	D=user_obj;C=json_data;E=C[_C];from project.sparta_6e115c4929.sparta_2add38e938 import qube_6f3e0ed78d as H;A=H.sparta_6c944993a7(D,E)
	if A is not _A:
		F=A.kernel_venv
		if F is _A:F=''
		C={_H:100,_C:E,_E:A.name,_I:F};G=sparta_1e6c849eae(C,D)
		if G[_B]==1:
			if A.is_static_variables:
				B=A.kernel_variables
				if B is not _A:
					I=sparta_5c6f6b98d4(D,E);B=cloudpickle.loads(B)
					for(J,K)in B.items():L=io.BytesIO(K);M=cloudpickle.load(L);I.set_workspace_variable(J,M)
		return G
	return{_B:-1}
def sparta_2a78ef2600(json_data,user_obj):return{_B:1}