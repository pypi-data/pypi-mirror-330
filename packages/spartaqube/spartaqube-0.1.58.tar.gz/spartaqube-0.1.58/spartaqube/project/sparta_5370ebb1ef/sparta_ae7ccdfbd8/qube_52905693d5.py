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
import project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 as qube_75fd5cec11
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_f07707f6fc
from project.sparta_484a14773c.sparta_9e33bcb61d import qube_9ace2206e4 as qube_9ace2206e4
def sparta_3085de03fe():
	A=platform.system()
	if A=='Windows':return _H
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_7d865d16f5(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_75fd5cec11.sparta_2e0feef849(B);return render(B,_D,A)
	qube_9ace2206e4.sparta_ef7df956ed();A=qube_75fd5cec11.sparta_2e0feef849(B);A[_E]=12;E=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(E);A[_F]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_3085de03fe()
	if D==_H:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\developer"
	elif D=='linux':C=os.path.expanduser('~/SpartaQube/developer')
	elif D=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\developer')
	F(C);A[_G]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_22bc8eeeb5(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_75fd5cec11.sparta_2e0feef849(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_9ace2206e4.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_7d865d16f5(B)
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_E]=12;H=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_93f2c297ed(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_75fd5cec11.sparta_2e0feef849(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_9ace2206e4.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_7d865d16f5(B)
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_E]=12;H=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_5c5b9a249b(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)