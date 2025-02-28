_D='bCodeMirror'
_C='menuBar'
_B='windows'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 as qube_75fd5cec11
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_f07707f6fc
from project.sparta_484a14773c.sparta_174d7f1491 import qube_e464ab5335 as qube_e464ab5335
from project.sparta_484a14773c.sparta_fe12f7b7e4 import qube_2c42c6daa9 as qube_2c42c6daa9
def sparta_3085de03fe():
	A=platform.system()
	if A=='Windows':return _B
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_fc5a2c913f(request):
	B=request;D=B.GET.get('edit')
	if D is None:D='-1'
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=9;F=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(F);A[_D]=_A;A['edit_chart_id']=D
	def G(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	E=sparta_3085de03fe()
	if E==_B:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\dashboard"
	elif E=='linux':C=os.path.expanduser('~/SpartaQube/dashboard')
	elif E=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\dashboard')
	G(C);A['default_project_path']=C;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_c32ea3989b(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_288c3ace2f(A,B)
def sparta_288c3ace2f(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_2c42c6daa9.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_fc5a2c913f(B)
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=9;I=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(I);A[_D]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)