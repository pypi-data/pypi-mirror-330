_L='bPublicUser'
_K='notebook_name'
_J='notebook_id'
_I='b_require_password'
_H='notebook_obj'
_G='windows'
_F='default_project_path'
_E='bCodeMirror'
_D='menuBar'
_C='res'
_B=None
_A=True
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
from project.sparta_484a14773c.sparta_5515f22550 import qube_86195f802e as qube_86195f802e
def sparta_3085de03fe():
	A=platform.system()
	if A=='Windows':return _G
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_de94bc333a(request):
	C=request;A=qube_75fd5cec11.sparta_2e0feef849(C);A[_D]=13;E=qube_75fd5cec11.sparta_62dea9d26b(C.user);A.update(E);A[_E]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_3085de03fe()
	if D==_G:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\notebook"
	elif D=='linux':B=os.path.expanduser('~/SpartaQube/notebook')
	elif D=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\notebook')
	F(B);A[_F]=B;return render(C,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_88c540f963(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_86195f802e.sparta_29c263add2(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_de94bc333a(B)
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_D]=12;H=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_9f7eecb9a5(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_86195f802e.sparta_29c263add2(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_de94bc333a(B)
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_D]=12;H=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)