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
import project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 as qube_9d6a4fd676
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_70235a51be
from project.sparta_6e115c4929.sparta_9bdc526091 import qube_1df776dd86 as qube_1df776dd86
def sparta_be18fe394d():
	A=platform.system()
	if A=='Windows':return _G
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_557fe49d2d(request):
	C=request;A=qube_9d6a4fd676.sparta_6908dae5fe(C);A[_D]=13;E=qube_9d6a4fd676.sparta_ec1b2d1f1a(C.user);A.update(E);A[_E]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_be18fe394d()
	if D==_G:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\notebook"
	elif D=='linux':B=os.path.expanduser('~/SpartaQube/notebook')
	elif D=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\notebook')
	F(B);A[_F]=B;return render(C,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_3c2cb138fa(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_1df776dd86.sparta_5bb304e308(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_557fe49d2d(B)
	A=qube_9d6a4fd676.sparta_6908dae5fe(B);A[_D]=12;H=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_ddfffbacb0(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_1df776dd86.sparta_5bb304e308(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_557fe49d2d(B)
	A=qube_9d6a4fd676.sparta_6908dae5fe(B);A[_D]=12;H=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)