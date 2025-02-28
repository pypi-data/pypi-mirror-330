_V='kernels'
_U='CommandLine'
_T='%Y-%m-%d %H:%M:%S'
_S='created_time'
_R='created_time_str'
_Q='workspace_variables'
_P='app.settings'
_O='venvName'
_N='kernelType'
_M='Windows'
_L='kernel_process_obj'
_K='spawnKernel.py'
_J='port'
_I='PPID'
_H='kernel_manager_uuid'
_G='name'
_F='-1'
_E=False
_D='kernelManagerUUID'
_C=True
_B='res'
_A=None
import os,sys,gc,socket,subprocess,threading,platform,psutil,zmq,json,base64,shutil,zipfile,io,uuid,cloudpickle
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC=pytz.utc
from django.contrib.humanize.templatetags.humanize import naturalday
from project.models import KernelProcess
from project.sparta_484a14773c.sparta_db5c65c546.qube_6f21764141 import IPythonKernel as IPythonKernel
from project.sparta_484a14773c.sparta_af861405ca.qube_f89769ea9f import sparta_a500ed5a10,sparta_a2b887365b,sparta_a86421c511
from project.sparta_484a14773c.sparta_f2ff0a56db.qube_59d77a0a81 import SenderKernel
from project.logger_config import logger
def sparta_edb6bc032c():
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as A:A.bind(('',0));return A.getsockname()[1]
class SqKernelManager:
	def __init__(A,kernel_manager_uuid,type,name,user,user_kernel=_A,project_folder=_A,notebook_exec_id=_F,dashboard_exec_id=_F,venv_name=_A):
		C=user_kernel;B=user;A.kernel_manager_uuid=kernel_manager_uuid;A.type=type;A.name=name;A.user=B;A.kernel_user_logged=B;A.project_folder=project_folder
		if C is _A:C=B
		A.user_kernel=C;A.venv_name=venv_name;A.notebook_exec_id=notebook_exec_id;A.dashboard_exec_id=dashboard_exec_id;A.is_init=_E;A.created_time=datetime.now()
	def create_kernel(A,django_settings_module=_A):
		if A.notebook_exec_id!=_F:A.user_kernel=sparta_a2b887365b(A.notebook_exec_id)
		if A.dashboard_exec_id!=_F:A.user_kernel=sparta_a86421c511(A.dashboard_exec_id)
		G=os.path.dirname(__file__);H=sparta_a500ed5a10(A.user_kernel);C=sparta_edb6bc032c();I=sys.executable;J=A.venv_name if A.venv_name is not _A else _F
		def L(pipe):
			for A in iter(pipe.readline,''):logger.debug(A,end='')
			pipe.close()
		F=os.environ.copy();F['ZMQ_PROCESS']='1';logger.debug(f"SPAWN PYTHON KERNEL {C}");K=subprocess.Popen([I,_K,str(H),str(C),J],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_C,cwd=G,env=F);D=K.pid;E=datetime.now().astimezone(UTC);B=sparta_34df366b6a(A.user,A.kernel_manager_uuid)
		if B is _A:B=KernelProcess.objects.create(kernel_manager_uuid=A.kernel_manager_uuid,port=C,pid=D,date_created=E,user=A.user,name=A.name,type=A.type,notebook_exec_id=A.notebook_exec_id,dashboard_exec_id=A.dashboard_exec_id,venv_name=A.venv_name,project_folder=A.project_folder,last_update=E)
		else:B.port=C;B.pid=D;B.pid=D;B.name=A.name;B.type=A.type;B.notebook_exec_id=A.notebook_exec_id;B.dashboard_exec_id=A.dashboard_exec_id;B.venv_name=A.venv_name;B.project_folder=A.project_folder;B.last_update=E;B.save()
		return{_B:1,_L:B}
def sparta_5a97002a94(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_size()
def sparta_41815931ac(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_workspace_variables()
def sparta_b0432a343f(kernel_process_obj,venv_name):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_activate_venv(venv_name)
def sparta_cc903b0fc8(kernel_process_obj,kernel_varname):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_variable_repr(kernel_varname)
def sparta_93e2d0e95e(kernel_process_obj,var_name,var_value):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_set_workspace_variable(var_name,var_value)
def set_workspace_cloudpickle_variables(kernel_process_obj,cloudpickle_kernel_variables):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_set_workspace_cloudpickle_variables(cloudpickle_kernel_variables)
def sparta_687f58d463(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_cloudpickle_kernel_variables()
def sparta_8ebd7afce3(pid):
	logger.debug('Force Kill Process now from kernel manager')
	if platform.system()==_M:return sparta_1ee15a5b7f(pid)
	else:return sparta_47b55d537a(pid)
def sparta_1ee15a5b7f(pid):
	try:subprocess.run(['taskkill','/F','/PID',str(pid)],check=_C,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError:logger.debug(f"Failed to kill process {pid}. It may not exist.")
def sparta_47b55d537a(pid):
	try:subprocess.run(['kill','-9',str(pid)],check=_C,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError:logger.debug(f"Failed to kill process {pid}. It may not exist.")
def sparta_520fecc253(kernel_process_obj):A=kernel_process_obj.pid;sparta_8ebd7afce3(A)
def sparta_34df366b6a(user_obj,kernel_manager_uuid):
	A=KernelProcess.objects.filter(user=user_obj,kernel_manager_uuid=kernel_manager_uuid,is_delete=_E)
	if A.count()>0:return A[0]
def sparta_219e721c90(json_data,user_obj,b_return_model=_E):
	E=user_obj;A=json_data;logger.debug('Create new kernel');logger.debug(A);H=A[_D];B=int(A[_N]);I=A.get(_G,'undefined');C=A.get('fullpath',_A);J=A.get('notebookExecId',_F);K=A.get('dashboardExecId',_F);D=A.get(_O,'')
	if len(D)==0:D=_A
	if C is not _A:C=os.path.dirname(C)
	F=SqKernelManager(H,B,I,E,user_kernel=E,project_folder=C,notebook_exec_id=J,dashboard_exec_id=K,venv_name=D)
	if B==3 or B==4 or B==5:G=F.create_kernel(django_settings_module=_P)
	else:G=F.create_kernel()
	if b_return_model:return G
	return{_B:1}
def sparta_e9337fa846(json_data,user_obj):
	C=user_obj;D=json_data[_D];A=sparta_34df366b6a(C,D)
	if A is not _A:
		sparta_520fecc253(A);B=A.type;F=A.name;G=A.project_folder;H=A.notebook_exec_id;I=A.dashboard_exec_id;J=A.user_kernel;K=A.venv_name;E=SqKernelManager(D,B,F,C,user_kernel=J,project_folder=G,notebook_exec_id=H,dashboard_exec_id=I,venv_name=K)
		if B==3 or B==4 or B==5:E.create_kernel(django_settings_module=_P)
		else:E.create_kernel()
	return{_B:1}
def sparta_161b865a56(json_data,user_obj):
	A=json_data
	if _D in A:
		C=A[_D];D=A['env_name'];B=sparta_34df366b6a(user_obj,C)
		if B is not _A:sparta_b0432a343f(B,D)
	return{_B:1}
def sparta_acf1bf6fa8(json_data,user_obj):
	B=json_data[_D];A=sparta_34df366b6a(user_obj,B)
	if A is not _A:C=sparta_5a97002a94(A);D=sparta_41815931ac(A);return{_B:1,'kernel':{_Q:D,_H:B,'kernel_size':C,'type':A.type,_G:A.name,_R:str(A.date_created.strftime(_T)),_S:naturalday(parser.parse(str(A.date_created)))}}
	return{_B:-1}
def sparta_3cf1154a03(json_data,user_obj):
	A=json_data;C=A[_D];D=A['varName'];B=sparta_34df366b6a(user_obj,C)
	if B is not _A:E=sparta_cc903b0fc8(B,D);return{_B:1,'htmlReprDict':E}
	return{_B:-1}
def sparta_55e2ab8d10(json_data,user_obj):
	C=json_data;D=C[_D];A=sparta_34df366b6a(user_obj,D)
	if A is not _A:
		B=C.get(_G,_A)
		if B is not _A:A.name=B;A.save();sparta_93e2d0e95e(A,_G,B)
	return{_B:1}
def sparta_2a67a1e6f7():
	if platform.system()==_M:return sparta_466e995e34()
	else:return sparta_532111114c()
def sparta_466e995e34():
	try:
		D=subprocess.run('wmic process where "name=\'python.exe\'" get ProcessId,ParentProcessId,CommandLine /FORMAT:CSV',shell=_C,capture_output=_C,text=_C);C=[];E=D.stdout.splitlines()
		for F in E[2:]:
			A=F.split(',')
			if len(A)<4:continue
			B=A[1].strip();G=A[2].strip();H=A[3].strip();I=B.split(' ')
			if _K in B:C.append({'PID':G,_I:H,_U:B,_J:I[3]})
		return C
	except Exception as J:logger.debug(f"Error finding parent process of spawnKernel.py: {J}");return[]
def sparta_532111114c():
	try:
		D=subprocess.run("ps -eo pid,ppid,command | grep '[s]pawnKernel.py'",shell=_C,capture_output=_C,text=_C);A=[];E=D.stdout.strip().split('\n')
		for F in E:
			B=F.strip().split(maxsplit=2)
			if len(B)<3:continue
			G,H,C=B;I=C.split(' ');A.append({'PID':G,_I:H,_U:C,_J:I[3]})
		return A
	except Exception as J:logger.debug(f"Error finding parent process of spawnKernel.py: {J}");return[]
def sparta_4f0a461fdf(json_data,user_obj):
	I='b_require_workspace_variables';C=user_obj;B=json_data;J=B.get('b_require_size',_E);K=B.get(I,_E);L=B.get(I,_E);D=[]
	if L:from project.sparta_484a14773c.sparta_c88ea4c8a4 import qube_d4c8e1df42 as M;D=M.sparta_660060270e(C)
	N=sparta_2a67a1e6f7();E=[(A[_I],A[_J])for A in N];O=KernelProcess.objects.filter(pid__in=[A[0]for A in E],port__in=[A[1]for A in E],user=C).distinct();F=[]
	for A in O:
		G=_A
		if J:G=sparta_5a97002a94(A)
		H=[]
		if K:H=sparta_41815931ac(A)
		F.append({_H:A.kernel_manager_uuid,_Q:H,'type':A.type,_G:A.name,_R:str(A.date_created.strftime(_T)),_S:naturalday(parser.parse(str(A.date_created))),'size':G,'isStored':_C if A.kernel_manager_uuid in D else _E})
	return{_B:1,_V:F}
def sparta_cf3375560c(json_data,user_obj):
	B=user_obj;from project.sparta_484a14773c.sparta_c88ea4c8a4 import qube_d4c8e1df42 as D;A=D.sparta_10fc480b5b(B);C=sparta_4f0a461fdf(json_data,B)
	if C[_B]==1:E=C[_V];F=[A[_H]for A in E];A=[A for A in A if A[_H]not in F];return{_B:1,'kernel_library':A}
	return{_B:-1}
def sparta_0abdd0c015(json_data,user_obj):
	B=json_data[_D];A=sparta_34df366b6a(user_obj,B)
	if A is not _A:sparta_520fecc253(A)
	return{_B:1}
def sparta_117f6ae298(json_data,user_obj):
	A=KernelProcess.objects.filter(user=user_obj,is_delete=_E)
	if A.count()>0:
		for B in A:sparta_520fecc253(B)
	return{_B:1}
def sparta_13818beb33(json_data,user_obj):
	C=user_obj;B=json_data;D=B[_D];from project.sparta_484a14773c.sparta_c88ea4c8a4 import qube_d4c8e1df42 as I;G=I.sparta_f90696fcf0(C,D);A=sparta_34df366b6a(C,D)
	if A is not _A:
		E=A.venv_name
		if E is _A:E=''
		B={_N:100,_D:D,_G:A.name,_O:E};F=sparta_219e721c90(B,C,_C)
		if F[_B]==1:
			A=F[_L]
			if G.is_static_variables:
				H=G.kernel_variables
				if H is not _A:set_workspace_cloudpickle_variables(A,H)
		return{_B:F[_B]}
	return{_B:-1}
def sparta_635bdab10e(json_data,user_obj):return{_B:1}