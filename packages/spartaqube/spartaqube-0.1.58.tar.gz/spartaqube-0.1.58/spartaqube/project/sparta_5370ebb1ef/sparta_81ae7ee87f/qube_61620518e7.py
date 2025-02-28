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
import project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 as qube_75fd5cec11
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_f07707f6fc
from project.sparta_484a14773c.sparta_f2ff0a56db import qube_532d53d6b9 as qube_532d53d6b9
from project.sparta_484a14773c.sparta_0b1182bbde import qube_be549b6d29 as qube_be549b6d29
def sparta_3085de03fe():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_7ded011b3d(request):A=request;B=qube_75fd5cec11.sparta_2e0feef849(A);B[_B]=-1;C=qube_75fd5cec11.sparta_62dea9d26b(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_0c0c4c7f49(request,kernel_manager_uuid):
	E=kernel_manager_uuid;D=True;B=request;F=False
	if E is None:F=D
	else:
		G=qube_532d53d6b9.sparta_34df366b6a(B.user,E)
		if G is None:F=D
	if F:return sparta_7ded011b3d(B)
	def I(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=D)
	H=sparta_3085de03fe()
	if H==_A:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif H=='linux':C=os.path.expanduser('~/SpartaQube/kernel')
	elif H=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	I(C);J=os.path.join(C,E);I(J);K=os.path.join(J,'main.ipynb')
	if not os.path.exists(K):
		L=qube_be549b6d29.sparta_dde01738ca()
		with open(K,'w')as M:M.write(json.dumps(L))
	A=qube_75fd5cec11.sparta_2e0feef849(B);A['default_project_path']=C;A[_B]=-1;N=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(N);A['kernel_name']=G.name;A['kernelManagerUUID']=G.kernel_manager_uuid;A['bCodeMirror']=D;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)