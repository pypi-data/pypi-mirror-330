_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_6e115c4929.sparta_e75895c000 import qube_10154d16cf as qube_10154d16cf
from project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 import sparta_ee4337ba55
from project.logger_config import logger
@csrf_exempt
def sparta_b9fee72991(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_10154d16cf.sparta_b9fee72991(B)
@csrf_exempt
def sparta_0ea995da3d(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_ffd0476193(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_602916adc9(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)