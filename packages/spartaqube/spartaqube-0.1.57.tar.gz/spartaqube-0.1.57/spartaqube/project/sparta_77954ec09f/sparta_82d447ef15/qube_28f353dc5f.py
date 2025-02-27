_D='bCodeMirror'
_C='menuBar'
_B='windows'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 as qube_9d6a4fd676
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_70235a51be
from project.sparta_6e115c4929.sparta_75ef90b243 import qube_63d9ee8418 as qube_63d9ee8418
from project.sparta_6e115c4929.sparta_60f8ddbc72 import qube_2208bfd19f as qube_2208bfd19f
def sparta_be18fe394d():
	A=platform.system()
	if A=='Windows':return _B
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_7e651fd867(request):
	B=request;D=B.GET.get('edit')
	if D is None:D='-1'
	A=qube_9d6a4fd676.sparta_6908dae5fe(B);A[_C]=9;F=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(F);A[_D]=_A;A['edit_chart_id']=D
	def G(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	E=sparta_be18fe394d()
	if E==_B:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\dashboard"
	elif E=='linux':C=os.path.expanduser('~/SpartaQube/dashboard')
	elif E=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\dashboard')
	G(C);A['default_project_path']=C;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_f98c46ee03(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_a4469f41ab(A,B)
def sparta_a4469f41ab(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_2208bfd19f.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_7e651fd867(B)
	A=qube_9d6a4fd676.sparta_6908dae5fe(B);A[_C]=9;I=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(I);A[_D]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)