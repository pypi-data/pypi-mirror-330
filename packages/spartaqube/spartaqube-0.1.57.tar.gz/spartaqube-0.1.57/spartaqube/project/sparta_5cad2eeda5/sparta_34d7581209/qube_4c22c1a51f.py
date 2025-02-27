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
from project.sparta_6e115c4929.sparta_d259733db6 import qube_04ef89247d as qube_04ef89247d
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_2b78ea6b23
@csrf_exempt
@sparta_2b78ea6b23
def sparta_9db1382230(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_04ef89247d.sparta_9db1382230(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_388ee84553(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_04ef89247d.sparta_388ee84553(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_115d344830(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_04ef89247d.sparta_115d344830(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_98a819caa4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_04ef89247d.sparta_98a819caa4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_8a11c9bf3d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_04ef89247d.sparta_8a11c9bf3d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_1e550a8c4d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_04ef89247d.sparta_1e550a8c4d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_3db4806f22(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_04ef89247d.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_a52a7c70f1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_04ef89247d.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_f111ea13c5(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_04ef89247d.sparta_f111ea13c5(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_cc434c2424(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_04ef89247d.sparta_cc434c2424(A,C);E=json.dumps(D);return HttpResponse(E)