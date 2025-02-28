_O='serialized_data'
_N='has_access'
_M='plot_name'
_L='plot_chart_id'
_K='dist/project/plot-db/plotDB.html'
_J='edit_chart_id'
_I='edit'
_H='plot_db_chart_obj'
_G=False
_F='login'
_E='-1'
_D='bCodeMirror'
_C='menuBar'
_B=None
_A=True
import json,base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 as qube_75fd5cec11
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_f07707f6fc
from project.sparta_484a14773c.sparta_174d7f1491 import qube_e464ab5335 as qube_e464ab5335
from project.sparta_484a14773c.sparta_fe12f7b7e4 import qube_2c42c6daa9 as qube_2c42c6daa9
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name=_F)
def sparta_5038789351(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=7;D=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name=_F)
def sparta_a9382a7cce(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=10;D=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name=_F)
def sparta_b49d3ffb39(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=11;D=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name=_F)
def sparta_13a6998a4d(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_e464ab5335.sparta_0419b083f7(C,A.user);D=not E[_N]
	if D:return sparta_5038789351(A)
	B=qube_75fd5cec11.sparta_2e0feef849(A);B[_C]=7;F=qube_75fd5cec11.sparta_62dea9d26b(A.user);B.update(F);B[_D]=_A;B[_L]=C;G=E[_H];B[_M]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_f07707f6fc
def sparta_7039e8c704(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return plot_widget_func(A,B)
@csrf_exempt
@sparta_f07707f6fc
def sparta_a7edfe4242(request,dashboard_id,id,password):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	C=base64.b64decode(password).decode();return plot_widget_func(A,B,dashboard_id=dashboard_id,dashboard_password=C)
@csrf_exempt
@sparta_f07707f6fc
def sparta_9dada5af95(request,widget_id,session_id,api_token_id):return plot_widget_func(request,widget_id,session_id)
def plot_widget_func(request,plot_chart_id,session=_E,dashboard_id=_E,token_permission='',dashboard_password=_B):
	K='token_permission';I=dashboard_id;H=plot_chart_id;G='res';E=token_permission;D=request;C=_G
	if H is _B:C=_A
	else:
		B=qube_e464ab5335.sparta_05ef136fbc(H,D.user);F=B[G]
		if F==-1:C=_A
	if C:
		if I!=_E:
			B=qube_2c42c6daa9.has_plot_db_access(I,H,D.user,dashboard_password);F=B[G]
			if F==1:E=B[K];C=_G
	if C:
		if len(E)>0:
			B=qube_e464ab5335.sparta_527b97a490(E);F=B[G]
			if F==1:C=_G
	if C:return sparta_5038789351(D)
	A=qube_75fd5cec11.sparta_2e0feef849(D);A[_C]=7;L=qube_75fd5cec11.sparta_62dea9d26b(D.user);A.update(L);A[_D]=_A;J=B[_H];A['b_require_password']=0 if B[G]==1 else 1;A[_L]=J.plot_chart_id;A[_M]=J.name;A['session']=str(session);A['is_dashboard_widget']=1 if I!=_E else 0;A['is_token']=1 if len(E)>0 else 0;A[K]=str(E);return render(D,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
def sparta_021ce7a309(request,token):return plot_widget_func(request,plot_chart_id=_B,token_permission=token)
@csrf_exempt
@sparta_f07707f6fc
def sparta_1f08f38e5f(request):B=request;A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=7;C=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(C);A[_D]=_A;A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name=_F)
def sparta_2b452eeaf7(request,id):
	K=',\n    ';B=request;C=id;F=_G
	if C is _B:F=_A
	else:G=qube_e464ab5335.sparta_0419b083f7(C,B.user);F=not G[_N]
	if F:return sparta_5038789351(B)
	L=qube_e464ab5335.sparta_cc395eb74c(G[_H]);D='';H=0
	for(E,I)in L.items():
		if H>0:D+=K
		if I==1:D+=f"{E}=input_{E}"
		else:M=str(K.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{M}]"
		H+=1
	J=f"'{C}'";N=f"\n    {J}\n";O=f"Spartaqube().get_widget({N})";P=f"\n    {J},\n    {D}\n";Q=f"Spartaqube().plot({P})";A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=7;R=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(R);A[_D]=_A;A[_L]=C;S=G[_H];A[_M]=S.name;A['plot_data_cmd']=O;A['plot_data_cmd_inputs']=Q;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_f07707f6fc
def sparta_21cb2bb26b(request,json_vars_html):B=request;A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=7;C=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(C);A[_D]=_A;A.update(json.loads(json_vars_html));A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotAPI.html',A)