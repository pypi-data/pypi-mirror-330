_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='res'
_C='Content-Disposition'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_6e115c4929.sparta_5b7f3fefa4 import qube_f10fc8419f as qube_f10fc8419f
from project.sparta_6e115c4929.sparta_5b7f3fefa4 import qube_e517011b21 as qube_e517011b21
from project.sparta_6e115c4929.sparta_52c500c3d5 import qube_1cc729b952 as qube_1cc729b952
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_2b78ea6b23
@csrf_exempt
@sparta_2b78ea6b23
def sparta_4d08ed2ce9(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_f10fc8419f.sparta_3fb87aed47(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_7ea80326ae(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f10fc8419f.sparta_0d1af70bba(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_a2d50f3676(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f10fc8419f.sparta_efead3735b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_25f646104b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f10fc8419f.sparta_0d8bd0be8d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_ded117799e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e517011b21.sparta_0c87a26470(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_1f8aac58ee(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f10fc8419f.sparta_63f91bb232(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_2acdaa0ba8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f10fc8419f.sparta_26b3c47d14(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_0ed2b78228(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f10fc8419f.sparta_99cf6a13c0(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_8c18029abb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f10fc8419f.sparta_d12b3e94a0(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_ce306389a4(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_f10fc8419f.sparta_16e4bdd102(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_2b78ea6b23
def sparta_76554042b1(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_f10fc8419f.sparta_c405911f6f(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_2b78ea6b23
def sparta_573e93140f(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_f10fc8419f.sparta_59b4477d19(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A