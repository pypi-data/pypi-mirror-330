_S='is_spartaqube_developer_mode'
_R='json_data'
_Q='SET VENV DEVELOPER DEBUG > set_venv_developer'
_P='Darwin'
_O='windows'
_N='Windows'
_M='backend'
_L='kernelManagerUUID'
_K='notebookId'
_J='developerId'
_I=None
_H='dashboardId'
_G='projectPath'
_F='-1'
_E='errorMsg'
_D='env_name'
_C=True
_B=False
_A='res'
import os,sys,subprocess,shutil,getpass,platform,json,base64,zipfile,io,uuid
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
import pytz
UTC=pytz.utc
from project.models_spartaqube import Dashboard,DashboardShared,Developer,DeveloperShared,Notebook,NotebookShared,Kernel,KernelShared
from project.models import ShareRights
from project.sparta_484a14773c.sparta_88433fd91c import qube_353c7b61a4 as qube_353c7b61a4
from project.sparta_484a14773c.sparta_8bb3408009 import qube_f97f36df45 as qube_f97f36df45
from project.sparta_484a14773c.sparta_5aa07280e6.qube_2b5480aafc import sparta_45043f35a3,sparta_f255489c63
from project.sparta_484a14773c.sparta_f2ff0a56db import qube_532d53d6b9 as qube_532d53d6b9
from project.logger_config import logger
def sparta_3085de03fe():
	A=platform.system()
	if A==_N:return _O
	elif A=='Linux':return'linux'
	elif A==_P:return'mac'
	else:return
def sparta_3758e8bd51(user_obj):
	A=qube_353c7b61a4.sparta_0fac479d2e(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_375f47dfb0():
	B=sparta_3085de03fe()
	if B==_O:A=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\sq_venv"
	elif B=='linux':A=os.path.expanduser('~/SpartaQube/sq_venv')
	elif B=='mac':A=os.path.expanduser('~/Library/Application Support\\SpartaQube\\sq_venv')
	os.makedirs(A,exist_ok=_C);return A
def sparta_0b5cd39607(env_name):
	A=env_name;B=sparta_375f47dfb0()
	if sys.platform=='win32':C=os.path.join(B,A,'Scripts','pip.exe')
	else:C=os.path.join(B,A,'bin','pip')
	return C
def sparta_3e89c87e91(json_data,user_obj):A=sparta_375f47dfb0();B=[B for B in os.listdir(A)if os.path.isdir(os.path.join(A,B))];return{_A:1,'available_venvs':B}
def sparta_2f973d0dbe(json_data,user_obj):
	B=sparta_375f47dfb0();A=json_data[_D];C=os.path.join(B,A)
	try:
		subprocess.run([sys.executable,'-m','venv',C],check=_C);D=['cloudpickle']
		for E in D:
			F=sparta_0b5cd39607(A);G=f"pip install {E}";H=G.replace('pip',F);I=subprocess.Popen(H,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_C)
			for J in I.stdout:logger.debug(J)
		return{_A:1}
	except Exception as K:return{_A:-1,_E:f"Failed to create virtual environment with error {str(K)}"}
def sparta_ac1dd17a7b(json_data,user_obj):
	C=json_data;B=user_obj;F=C[_H];D=Dashboard.objects.filter(dashboard_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.dashboard_id;G=sparta_3758e8bd51(B)
		if len(G)>0:E=DashboardShared.objects.filter(Q(is_delete=0,user_group__in=G,dashboard__is_delete=0,dashboard=A)|Q(is_delete=0,user=B,dashboard__is_delete=0,dashboard=A))
		else:E=DashboardShared.objects.filter(is_delete=0,user=B,dashboard__is_delete=0,dashboard=A)
		H=_B
		if E.count()>0:
			J=E[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:K=C[_D];A.dashboard_venv=K;A.save()
	L=qube_532d53d6b9.sparta_161b865a56(C,B);return{_A:1}
def sparta_b1d663679d(json_data,user_obj):
	B=user_obj;E=json_data[_H];C=Dashboard.objects.filter(dashboard_id__startswith=E,is_delete=_B).all()
	if C.count()==1:
		A=C[C.count()-1];E=A.dashboard_id;F=sparta_3758e8bd51(B)
		if len(F)>0:D=DashboardShared.objects.filter(Q(is_delete=0,user_group__in=F,dashboard__is_delete=0,dashboard=A)|Q(is_delete=0,user=B,dashboard__is_delete=0,dashboard=A))
		else:D=DashboardShared.objects.filter(is_delete=0,user=B,dashboard__is_delete=0,dashboard=A)
		G=_B
		if D.count()>0:
			I=D[0];H=I.share_rights
			if H.is_admin or H.has_write_rights:G=_C
		if G:J=_I;A.dashboard_venv=J;A.save()
	return{_A:1}
def sparta_a3305d304c(json_data,user_obj):
	C=user_obj;A=json_data;D=A[_H];E=A[_J]
	if str(D)!=_F:sparta_b1d663679d(A,C)
	if str(E)!=_F:sparta_589a2eccaf(A,C)
	F=sparta_375f47dfb0();G=A[_D];H=os.path.join(F,G)
	try:shutil.rmtree(H);return{_A:1}
	except FileNotFoundError as B:return{_A:-1,_E:str(B)}
	except Exception as B:return{_A:-1,_E:str(B)}
def sparta_e81e1dd92e(json_data,user_obj):
	B=json_data[_D];C=sparta_0b5cd39607(B);A=[]
	try:
		D=subprocess.run([C,'list'],capture_output=_C,text=_C,check=_C);E=D.stdout.strip().splitlines()[2:]
		for F in E:G,H=F.split()[:2];A.append({'name':G,'version':H})
		return{_A:1,'libraries':A}
	except Exception as I:return{_A:-1,_E:str(I)}
def sparta_58f9d68fe4(env_name,project_path):
	A=os.path.join(project_path,'requirements.txt');B=sparta_0b5cd39607(env_name)
	try:
		with open(A,'w')as C:subprocess.run([B,'freeze'],stdout=C)
		return{_A:1}
	except Exception as D:return{_A:-1,_E:str(D)}
def sparta_4eca9ed64f(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug(_Q);logger.debug(B);F=B[_J];D=Developer.objects.filter(developer_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.developer_id;G=sparta_3758e8bd51(C)
		if len(G)>0:E=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=A)|Q(is_delete=0,user=C,developer__is_delete=0,developer=A))
		else:E=DeveloperShared.objects.filter(is_delete=0,user=C,developer__is_delete=0,developer=A)
		H=_B
		if E.count()>0:
			J=E[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:K=B[_D];A.developer_venv=K;A.save()
	L=qube_532d53d6b9.sparta_161b865a56(B,C);return{_A:1}
def sparta_589a2eccaf(json_data,user_obj):
	B=user_obj;E=json_data[_J];C=Developer.objects.filter(developer_id__startswith=E,is_delete=_B).all()
	if C.count()==1:
		A=C[C.count()-1];E=A.developer_id;F=sparta_3758e8bd51(B)
		if len(F)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=F,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=A)
		G=_B
		if D.count()>0:
			I=D[0];H=I.share_rights
			if H.is_admin or H.has_write_rights:G=_C
		if G:J=_I;A.developer_venv=J;A.save()
	return{_A:1}
def sparta_dba44f94b2(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug(_Q);logger.debug(B);F=B[_K];D=Notebook.objects.filter(notebook_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.notebook_id;G=sparta_3758e8bd51(C)
		if len(G)>0:E=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=C,notebook__is_delete=0,notebook=A))
		else:E=NotebookShared.objects.filter(is_delete=0,user=C,notebook__is_delete=0,notebook=A)
		H=_B
		if E.count()>0:
			J=E[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:K=B[_D];A.notebook_venv=K;A.save()
	L=qube_532d53d6b9.sparta_161b865a56(B,C);return{_A:1}
def sparta_f51e131946(json_data,user_obj):
	B=user_obj;E=json_data[_K];C=Notebook.objects.filter(notebook_id__startswith=E,is_delete=_B).all()
	if C.count()==1:
		A=C[C.count()-1];E=A.notebook_id;F=sparta_3758e8bd51(B)
		if len(F)>0:D=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=F,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=B,notebook__is_delete=0,notebook=A))
		else:D=NotebookShared.objects.filter(is_delete=0,user=B,notebook__is_delete=0,notebook=A)
		G=_B
		if D.count()>0:
			I=D[0];H=I.share_rights
			if H.is_admin or H.has_write_rights:G=_C
		if G:J=_I;A.notebook_venv=J;A.save()
	return{_A:1}
def sparta_19d5c37fde(json_data,user_obj):
	C=json_data;B=user_obj;from project.sparta_484a14773c.sparta_f2ff0a56db import qube_532d53d6b9 as J;F=C[_L];D=Kernel.objects.filter(kernel_manager_uuid__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.kernel_manager_uuid;G=sparta_3758e8bd51(B)
		if len(G)>0:E=KernelShared.objects.filter(Q(is_delete=0,user_group__in=G,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=B,kernel__is_delete=0,kernel=A))
		else:E=KernelShared.objects.filter(is_delete=0,user=B,kernel__is_delete=0,kernel=A)
		H=_B
		if E.count()>0:
			K=E[0];I=K.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:L=C[_D];A.kernel_venv=L;A.save()
	M=J.sparta_161b865a56(C,B);return{_A:1}
def sparta_c2ae87537b(json_data,user_obj):
	B=user_obj;E=json_data[_L];C=Kernel.objects.filter(kernel_manager_uuid__startswith=E,is_delete=_B).all()
	if C.count()==1:
		A=C[C.count()-1];E=A.kernel_manager_uuid;F=sparta_3758e8bd51(B)
		if len(F)>0:D=KernelShared.objects.filter(Q(is_delete=0,user_group__in=F,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=B,kernel__is_delete=0,kernel=A))
		else:D=KernelShared.objects.filter(is_delete=0,user=B,kernel__is_delete=0,kernel=A)
		G=_B
		if D.count()>0:
			I=D[0];H=I.share_rights
			if H.is_admin or H.has_write_rights:G=_C
		if G:J=_I;A.kernel_venv=J;A.save()
	return{_A:1}
def sparta_f37e86c3d6(json_data,user_obj):
	B=user_obj;A=json_data;logger.debug(_R);logger.debug(A);D=A[_H];E=A[_J];F=A[_K];G=A[_L]
	if str(D)!=_F:return sparta_a963da99b6(A,B)
	if str(E)!=_F:return sparta_92bad3e8da(A,B)
	if str(F)!=_F:return sparta_4d557bd0a5(A,B)
	if str(G)!=_F:return sparta_22325f7b77(A,B)
	H=A[_D];C=A[_G]
	if A[_S]:C=os.path.join(C,_M)
	return sparta_58f9d68fe4(H,C)
def sparta_a963da99b6(json_data,user_obj):
	C=user_obj;B=json_data;F=B[_H];J=B[_D];K=B[_G];D=Dashboard.objects.filter(dashboard_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.dashboard_id;G=sparta_3758e8bd51(C)
		if len(G)>0:E=DashboardShared.objects.filter(Q(is_delete=0,user_group__in=G,dashboard__is_delete=0,dashboard=A)|Q(is_delete=0,user=C,dashboard__is_delete=0,dashboard=A))
		else:E=DashboardShared.objects.filter(is_delete=0,user=C,dashboard__is_delete=0,dashboard=A)
		H=_B
		if E.count()>0:
			L=E[0];I=L.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:return sparta_58f9d68fe4(J,K)
	return{_A:1}
def sparta_92bad3e8da(json_data,user_obj):
	C=user_obj;B=json_data;G=B[_J];K=B[_D];D=B[_G];D=os.path.join(D,_M);E=Developer.objects.filter(developer_id__startswith=G,is_delete=_B).all()
	if E.count()==1:
		A=E[E.count()-1];G=A.developer_id;H=sparta_3758e8bd51(C)
		if len(H)>0:F=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=H,developer__is_delete=0,developer=A)|Q(is_delete=0,user=C,developer__is_delete=0,developer=A))
		else:F=DeveloperShared.objects.filter(is_delete=0,user=C,developer__is_delete=0,developer=A)
		I=_B
		if F.count()>0:
			L=F[0];J=L.share_rights
			if J.is_admin or J.has_write_rights:I=_C
		if I:return sparta_58f9d68fe4(K,D)
	return{_A:1}
def sparta_4d557bd0a5(json_data,user_obj):
	C=user_obj;B=json_data;F=B[_K];J=B[_D];K=B[_G];D=Notebook.objects.filter(notebook_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.developer_id;G=sparta_3758e8bd51(C)
		if len(G)>0:E=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=C,notebook__is_delete=0,notebook=A))
		else:E=NotebookShared.objects.filter(is_delete=0,user=C,notebook__is_delete=0,notebook=A)
		H=_B
		if E.count()>0:
			L=E[0];I=L.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:return sparta_58f9d68fe4(J,K)
	return{_A:1}
def sparta_22325f7b77(json_data,user_obj):
	A=json_data;from project.sparta_484a14773c.sparta_f2ff0a56db import qube_532d53d6b9 as B;C=A[_L];D=A[_D];E=A[_G];F=B.sparta_34df366b6a(user_obj,C)
	if F is _I:return sparta_58f9d68fe4(D,E)
	return{_A:1}
def sparta_c629763a22(json_data,user_obj):
	B=json_data;logger.debug(_R);logger.debug(B);E=B[_D];C=os.path.join(sparta_375f47dfb0(),E);logger.debug('venv_path');logger.debug(C);A=sparta_45043f35a3(B[_G])
	if B[_S]:A=os.path.join(A,_M)
	if not os.path.isdir(A):return{_A:-1,_E:f"The provided path '{A}' is not a valid directory."}
	D=platform.system()
	try:
		if D==_N:os.system(f'start cmd /K "cd /d {A} && {C}\\Scripts\\activate.bat"')
		elif D=='Linux':subprocess.run(['x-terminal-emulator','-e',f'bash -c "cd {A} && source {C}/bin/activate && exec bash"'],check=_C)
		elif D==_P:F=f'''
            tell application "Terminal"
                do script "cd {A} && source {C}/bin/activate"
                activate
            end tell
            ''';subprocess.run(['osascript','-e',F],check=_C)
		else:return{_A:-1,_E:'Unsupported operating system.'}
	except Exception as G:return{_A:-1,_E:f"Failed to open terminal and activate venv at '{A}': {G}"}
	return{_A:1}