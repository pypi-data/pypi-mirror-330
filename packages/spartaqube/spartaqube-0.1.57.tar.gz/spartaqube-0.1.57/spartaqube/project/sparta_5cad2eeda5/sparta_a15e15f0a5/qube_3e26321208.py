_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_6e115c4929.sparta_72abe172fc import qube_828bded42e as qube_828bded42e
from project.sparta_6e115c4929.sparta_72abe172fc import qube_fdb976f8d0 as qube_fdb976f8d0
from project.sparta_6e115c4929.sparta_60f8ddbc72 import qube_2208bfd19f as qube_2208bfd19f
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_2b78ea6b23,sparta_d3c5037e12
@csrf_exempt
def sparta_b559b3d0ee(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_b559b3d0ee(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_c4d0b2f4b4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_c4d0b2f4b4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_fb85a621b8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_fb85a621b8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_39fd401726(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_39fd401726(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_f10eb50285(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_f10eb50285(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_8367967b4c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_8367967b4c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_bbba454112(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_bbba454112(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_5d8705784f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_5d8705784f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_bef5df62e8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_bef5df62e8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_c055fb56c1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.sparta_c055fb56c1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_1707b2c094(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_828bded42e.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_9fde3c647a(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_828bded42e.sparta_9fde3c647a(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_27117ef347(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_2990a0499f(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_962fb273f2(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_2990a0499f(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_828bded42e.sparta_16e4bdd102(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_2b78ea6b23
def sparta_2c87cfeb2a(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_828bded42e.sparta_59b4477d19(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_02ef4555de(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_02ef4555de(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_72a0e3bbab(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_72a0e3bbab(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_741b5b4c95(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_741b5b4c95(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_250089e4c8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_250089e4c8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_567a8d6c97(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_567a8d6c97(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_6fe7d9adf9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_6fe7d9adf9(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_c285791eac(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_c285791eac(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_ac0f2cae52(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_ac0f2cae52(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_dc61438118(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_dc61438118(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_5dc7848723(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_5dc7848723(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_4b54d76ac3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_4b54d76ac3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_26078e714b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_26078e714b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_22fa590e97(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_22fa590e97(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
@sparta_d3c5037e12
def sparta_c8fdd10f85(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fdb976f8d0.sparta_c8fdd10f85(C,A.user);E=json.dumps(D);return HttpResponse(E)