_U='projectPath'
_T='kernelSize'
_S='kernelVenv'
_R='kernel_size'
_Q='main_ipynb_fullpath'
_P='kernel_manager_uuid'
_O='main.ipynb'
_N='-kernel__last_update'
_M='kernel_cpkl_unpicklable'
_L='windows'
_K='luminoLayout'
_J='description'
_I='slug'
_H='is_static_variables'
_G=False
_F='unpicklable'
_E='name'
_D='kernelManagerUUID'
_C='res'
_B=True
_A=None
import os,sys,gc,json,base64,shutil,zipfile,io,uuid,subprocess,cloudpickle,platform,getpass
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC=pytz.utc
from django.contrib.humanize.templatetags.humanize import naturalday
from project.sparta_484a14773c.sparta_88433fd91c import qube_353c7b61a4 as qube_353c7b61a4
from project.models_spartaqube import Kernel,KernelShared,ShareRights
from project.sparta_484a14773c.sparta_db5c65c546.qube_6f21764141 import IPythonKernel as IPythonKernel
from project.sparta_484a14773c.sparta_5aa07280e6.qube_2b5480aafc import sparta_45043f35a3,sparta_f255489c63
from project.sparta_484a14773c.sparta_af861405ca.qube_f89769ea9f import sparta_c17142f1a4,sparta_a500ed5a10,sparta_a2b887365b,sparta_a86421c511
from project.sparta_484a14773c.sparta_5aa07280e6.qube_1b962f541a import sparta_f0e24d00e7,sparta_fa8168e869
from project.sparta_484a14773c.sparta_cf2c26801e.qube_3818061d71 import sparta_f3e34e8081
from project.logger_config import logger
def sparta_3085de03fe():
	A=platform.system()
	if A=='Windows':return _L
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_78038dc6f6():
	A=sparta_3085de03fe()
	if A==_L:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif A=='linux':B=os.path.expanduser('~/SpartaQube/kernel')
	elif A=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	return B
def sparta_3758e8bd51(user_obj):
	A=qube_353c7b61a4.sparta_0fac479d2e(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_daa3223651(user_obj,kernel_manager_uuid):from project.sparta_484a14773c.sparta_f2ff0a56db import qube_532d53d6b9 as B;E=B.sparta_34df366b6a(user_obj,kernel_manager_uuid);A=B.sparta_687f58d463(E);logger.debug('get_cloudpickle_kernel_variables res_dict');logger.debug(A);C=A['picklable'];logger.debug('kernel_cpkl_picklable');logger.debug(type(C));logger.debug("res_dict['unpicklable']");logger.debug(type(A[_F]));D=cloudpickle.loads(A[_F]);logger.debug(_M);logger.debug(type(D));return C,D
def sparta_10fc480b5b(user_obj):
	I='%Y-%m-%d';C=user_obj;J=sparta_78038dc6f6();D=sparta_3758e8bd51(C)
	if len(D)>0:B=KernelShared.objects.filter(Q(is_delete=0,user_group__in=D,kernel__is_delete=0)|Q(is_delete=0,user=C,kernel__is_delete=0))
	else:B=KernelShared.objects.filter(Q(is_delete=0,user=C,kernel__is_delete=0))
	if B.count()>0:B=B.order_by(_N)
	E=[]
	for F in B:
		A=F.kernel;K=F.share_rights;G=_A
		try:G=str(A.last_update.strftime(I))
		except:pass
		H=_A
		try:H=str(A.date_created.strftime(I))
		except Exception as L:logger.debug(L)
		M=os.path.join(J,A.kernel_manager_uuid,_O);E.append({_P:A.kernel_manager_uuid,_E:A.name,_I:A.slug,_J:A.description,_Q:M,_R:A.kernel_size,'has_write_rights':K.has_write_rights,'last_update':G,'date_created':H})
	return E
def sparta_660060270e(user_obj):
	B=user_obj;C=sparta_3758e8bd51(B)
	if len(C)>0:A=KernelShared.objects.filter(Q(is_delete=0,user_group__in=C,kernel__is_delete=0)|Q(is_delete=0,user=B,kernel__is_delete=0))
	else:A=KernelShared.objects.filter(Q(is_delete=0,user=B,kernel__is_delete=0))
	if A.count()>0:A=A.order_by(_N);return[A.kernel.kernel_manager_uuid for A in A]
	return[]
def sparta_f90696fcf0(user_obj,kernel_manager_uuid):
	B=user_obj;D=Kernel.objects.filter(kernel_manager_uuid=kernel_manager_uuid).all()
	if D.count()>0:
		A=D[0];E=sparta_3758e8bd51(B)
		if len(E)>0:C=KernelShared.objects.filter(Q(is_delete=0,user_group__in=E,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=B,kernel__is_delete=0,kernel=A))
		else:C=KernelShared.objects.filter(is_delete=0,user=B,kernel__is_delete=0,kernel=A)
		F=_G
		if C.count()>0:
			H=C[0];G=H.share_rights
			if G.is_admin or G.has_write_rights:F=_B
		if F:return A
def sparta_9196dc00f8(json_data,user_obj):
	D=user_obj;from project.sparta_484a14773c.sparta_f2ff0a56db import qube_532d53d6b9 as I;A=json_data[_D];B=I.sparta_34df366b6a(D,A)
	if B is _A:return{_C:-1,'errorMsg':'Kernel not found'}
	E=sparta_78038dc6f6();J=os.path.join(E,A,_O);K=B.venv_name;F=_A;G=_G;H=_G;C=sparta_f90696fcf0(D,A)
	if C is not _A:G=_B;F=C.lumino_layout;H=C.is_static_variables
	return{_C:1,'kernel':{'basic':{'is_kernel_saved':G,_H:H,_P:A,_E:B.name,'kernel_venv':K,'kernel_type':B.type,'project_path':E,_Q:J},'lumino':{'lumino_layout':F}}}
def sparta_4cb1ca3e06(json_data,user_obj):
	D=user_obj;A=json_data;logger.debug('Save notebook');logger.debug(A);logger.debug(A.keys());L=A['isKernelSaved']
	if L:return sparta_09ccd08de5(A,D)
	C=datetime.now().astimezone(UTC);G=A[_D];M=A[_K];N=A[_E];O=A[_J];E=sparta_78038dc6f6();E=sparta_45043f35a3(E);H=A[_H];P=A.get(_S,_A);Q=A.get(_T,0);B=A.get(_I,'')
	if len(B)==0:B=A[_E]
	I=slugify(B);B=I;J=1
	while Kernel.objects.filter(slug=B).exists():B=f"{I}-{J}";J+=1
	K=_A;F=[]
	if H:K,F=sparta_daa3223651(D,G)
	R=Kernel.objects.create(kernel_manager_uuid=G,name=N,slug=B,description=O,is_static_variables=H,lumino_layout=M,project_path=E,kernel_venv=P,kernel_variables=K,kernel_size=Q,date_created=C,last_update=C,last_date_used=C,spartaqube_version=sparta_f3e34e8081());S=ShareRights.objects.create(is_admin=_B,has_write_rights=_B,has_reshare_rights=_B,last_update=C);KernelShared.objects.create(kernel=R,user=D,share_rights=S,is_owner=_B,date_created=C);logger.debug(_M);logger.debug(F);return{_C:1,_F:F}
def sparta_09ccd08de5(json_data,user_obj):
	F=user_obj;A=json_data;logger.debug('update_kernel_notebook');logger.debug(A);D=A[_D];B=sparta_f90696fcf0(F,D)
	if B is not _A:
		K=datetime.now().astimezone(UTC);D=A[_D];L=A[_K];M=A[_E];N=A[_J];E=A[_H];O=A.get(_S,_A);P=A.get(_T,0);C=A.get(_I,'')
		if len(C)==0:C=A[_E]
		G=slugify(C);C=G;H=1
		while Kernel.objects.filter(slug=C).exists():C=f"{G}-{H}";H+=1
		E=A[_H];I=_A;J=[]
		if E:I,J=sparta_daa3223651(F,D)
		B.name=M;B.description=N;B.slug=C;B.kernel_venv=O;B.kernel_size=P;B.is_static_variables=E;B.kernel_variables=I;B.lumino_layout=L;B.last_update=K;B.save()
	return{_C:1,_F:J}
def sparta_beed01926d(json_data,user_obj):0
def sparta_b6033d20b9(json_data,user_obj):A=sparta_45043f35a3(json_data[_U]);return sparta_f0e24d00e7(A)
def sparta_a0fd855a63(json_data,user_obj):A=sparta_45043f35a3(json_data[_U]);return sparta_fa8168e869(A)
def sparta_90fa61ed23(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug('SAVE LYUMINO LAYOUT KERNEL NOTEBOOK');logger.debug('json_data');logger.debug(B);I=B[_D];E=Kernel.objects.filter(kernel_manager_uuid=I).all()
	if E.count()>0:
		A=E[0];F=sparta_3758e8bd51(C)
		if len(F)>0:D=KernelShared.objects.filter(Q(is_delete=0,user_group__in=F,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=C,kernel__is_delete=0,kernel=A))
		else:D=KernelShared.objects.filter(is_delete=0,user=C,kernel__is_delete=0,kernel=A)
		G=_G
		if D.count()>0:
			J=D[0];H=J.share_rights
			if H.is_admin or H.has_write_rights:G=_B
		if G:K=B[_K];A.lumino_layout=K;A.save()
	return{_C:1}
def sparta_11ebe78660(json_data,user_obj):
	from project.sparta_484a14773c.sparta_f2ff0a56db import qube_532d53d6b9 as A;C=json_data[_D];B=A.sparta_34df366b6a(user_obj,C)
	if B is not _A:D=A.sparta_5a97002a94(B);return{_C:1,_R:D}
	return{_C:-1}
def sparta_a7f0369da9(json_data,user_obj):
	B=json_data[_D];A=sparta_f90696fcf0(user_obj,B)
	if A is not _A:A.is_delete=_B;A.save()
	return{_C:1}