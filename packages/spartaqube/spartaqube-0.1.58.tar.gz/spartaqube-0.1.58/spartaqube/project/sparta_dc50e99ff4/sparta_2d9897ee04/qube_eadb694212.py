_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_484a14773c.sparta_074ed274f8 import qube_910775047c as qube_910775047c
from project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 import sparta_ed1ea5fed9
from project.logger_config import logger
@csrf_exempt
def sparta_beb01333b9(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_910775047c.sparta_beb01333b9(B)
@csrf_exempt
def sparta_5400f6eb40(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_633a3163c8(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_0caa4f47ae(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)