_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_484a14773c.sparta_93477150a0 import qube_e2b3976991 as qube_e2b3976991
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_0389256417
@csrf_exempt
@sparta_0389256417
def sparta_f9b84d1b21(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e2b3976991.sparta_f9b84d1b21(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_c5934efbc6(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_e2b3976991.sparta_c5934efbc6(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_0389256417
def sparta_dfe745746d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_e2b3976991.sparta_dfe745746d(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_0389256417
def sparta_1431cc8482(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e2b3976991.sparta_1431cc8482(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_643beb64ad(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e2b3976991.sparta_643beb64ad(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0389256417
def sparta_9140d348af(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e2b3976991.sparta_9140d348af(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_3ea2ffab60(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_e2b3976991.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_0389256417
def sparta_ae011c73ff(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e2b3976991.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_b8cdd8d83b(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_e2b3976991.sparta_b8cdd8d83b(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_a7a01f84ff(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e2b3976991.sparta_a7a01f84ff(A,C);E=json.dumps(D);return HttpResponse(E)