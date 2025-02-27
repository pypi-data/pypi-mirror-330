_M='bPublicUser'
_L='developer_name'
_K='developer_id'
_J='b_require_password'
_I='developer_obj'
_H='windows'
_G='default_project_path'
_F='bCodeMirror'
_E='menuBar'
_D='dist/project/homepage/homepage.html'
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
from django.conf import settings as conf_settings
import project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 as qube_9d6a4fd676
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_70235a51be
from project.sparta_6e115c4929.sparta_59dd45b58c import qube_c98a8b9a45 as qube_c98a8b9a45
def sparta_be18fe394d():
	A=platform.system()
	if A=='Windows':return _H
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_957a2ffbcc(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_9d6a4fd676.sparta_6908dae5fe(B);return render(B,_D,A)
	qube_c98a8b9a45.sparta_da80d02029();A=qube_9d6a4fd676.sparta_6908dae5fe(B);A[_E]=12;E=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(E);A[_F]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_be18fe394d()
	if D==_H:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\developer"
	elif D=='linux':C=os.path.expanduser('~/SpartaQube/developer')
	elif D=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\developer')
	F(C);A[_G]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_9dc5df0959(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_9d6a4fd676.sparta_6908dae5fe(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_c98a8b9a45.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_957a2ffbcc(B)
	A=qube_9d6a4fd676.sparta_6908dae5fe(B);A[_E]=12;H=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_8c6fbe72e3(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_9d6a4fd676.sparta_6908dae5fe(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_c98a8b9a45.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_957a2ffbcc(B)
	A=qube_9d6a4fd676.sparta_6908dae5fe(B);A[_E]=12;H=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_6aa93b5e97(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)