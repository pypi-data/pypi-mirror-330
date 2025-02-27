_B='menuBar'
_A='windows'
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import FileResponse,Http404
from urllib.parse import unquote
import project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 as qube_9d6a4fd676
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_70235a51be
from project.sparta_6e115c4929.sparta_7db1c861ca import qube_ae0645fdeb as qube_ae0645fdeb
from project.sparta_6e115c4929.sparta_72abe172fc import qube_726ce0372b as qube_726ce0372b
def sparta_be18fe394d():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_8db6820aee(request):A=request;B=qube_9d6a4fd676.sparta_6908dae5fe(A);B[_B]=-1;C=qube_9d6a4fd676.sparta_ec1b2d1f1a(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_6a105e443d(request,kernel_manager_uuid):
	E=kernel_manager_uuid;D=True;B=request;F=False
	if E is None:F=D
	else:
		G=qube_ae0645fdeb.sparta_e2a720c602(B.user,E)
		if G is None:F=D
	if F:return sparta_8db6820aee(B)
	def I(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=D)
	H=sparta_be18fe394d()
	if H==_A:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif H=='linux':C=os.path.expanduser('~/SpartaQube/kernel')
	elif H=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	I(C);J=os.path.join(C,E);I(J);K=os.path.join(J,'main.ipynb')
	if not os.path.exists(K):
		L=qube_726ce0372b.sparta_78ef41812f()
		with open(K,'w')as M:M.write(json.dumps(L))
	A=qube_9d6a4fd676.sparta_6908dae5fe(B);A['default_project_path']=C;A[_B]=-1;N=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(N);A['kernel_name']=G.name;A['kernelManagerUUID']=G.kernel_manager_uuid;A['bCodeMirror']=D;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)