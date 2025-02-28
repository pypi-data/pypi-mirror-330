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
from project.sparta_484a14773c.sparta_0ba50b6cba import qube_3d0ead9195 as qube_3d0ead9195
from project.sparta_484a14773c.sparta_0ba50b6cba import qube_06bcd87648 as qube_06bcd87648
from project.sparta_484a14773c.sparta_5aa07280e6 import qube_2b5480aafc as qube_2b5480aafc
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_0389256417
@csrf_exempt
@sparta_0389256417
def sparta_c3efff2457(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_3d0ead9195.sparta_da8222fb67(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_0389256417
def sparta_801d6d9024(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3d0ead9195.sparta_e0fe873a22(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_21a847503f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3d0ead9195.sparta_17bb066d61(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_281db9b7de(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3d0ead9195.sparta_448bc65252(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_68ca1a290d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_06bcd87648.sparta_6a8f69b3da(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_7d6b5b5e0a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3d0ead9195.sparta_dd43124580(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_262e721760(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3d0ead9195.sparta_6b50f2137a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_5a77fed63e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3d0ead9195.sparta_ed3ab50740(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_6e2ca6dc30(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3d0ead9195.sparta_f52ab8f572(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_6265a173da(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_3d0ead9195.sparta_a72f2289e5(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_0389256417
def sparta_b9e6f5f7da(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_3d0ead9195.sparta_323c1bde93(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_0389256417
def sparta_aaac733abc(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_3d0ead9195.sparta_d15988f9cd(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A