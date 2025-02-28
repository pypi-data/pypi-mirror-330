_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_484a14773c.sparta_0b1182bbde import qube_5204246baf as qube_5204246baf
from project.sparta_484a14773c.sparta_0b1182bbde import qube_5280ee6490 as qube_5280ee6490
from project.sparta_484a14773c.sparta_fe12f7b7e4 import qube_2c42c6daa9 as qube_2c42c6daa9
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_0389256417,sparta_975aa49770
@csrf_exempt
def sparta_4cdf97181b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_4cdf97181b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_491fd9b4e6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_491fd9b4e6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_11e9f54019(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_11e9f54019(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_169a489525(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_169a489525(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_d08bc38098(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_d08bc38098(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_9a0729fb6b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_9a0729fb6b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_db35536cf4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_db35536cf4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_fd9cd535aa(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_fd9cd535aa(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_b04eed283c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_b04eed283c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_e24ba712f9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.sparta_e24ba712f9(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_c945cddeab(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5204246baf.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_858fc22d2e(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_5204246baf.sparta_858fc22d2e(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_a087a59406(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_57b08e818c(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_0389256417
def sparta_6001adbcc8(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_57b08e818c(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_5204246baf.sparta_a72f2289e5(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_0389256417
def sparta_2b506dc80f(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_5204246baf.sparta_d15988f9cd(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_3e89c87e91(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_3e89c87e91(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_2f973d0dbe(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_2f973d0dbe(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_ac1dd17a7b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_ac1dd17a7b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_dba44f94b2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_dba44f94b2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_19d5c37fde(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_19d5c37fde(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_4eca9ed64f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_4eca9ed64f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_b1d663679d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_b1d663679d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_f51e131946(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_f51e131946(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_c2ae87537b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_c2ae87537b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_589a2eccaf(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_589a2eccaf(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_a3305d304c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_a3305d304c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_e81e1dd92e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_e81e1dd92e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_f37e86c3d6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_f37e86c3d6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
@sparta_975aa49770
def sparta_c629763a22(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5280ee6490.sparta_c629763a22(C,A.user);E=json.dumps(D);return HttpResponse(E)