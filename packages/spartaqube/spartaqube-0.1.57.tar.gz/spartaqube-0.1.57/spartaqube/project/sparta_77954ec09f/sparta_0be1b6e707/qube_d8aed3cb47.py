_O='Please send valid data'
_N='dist/project/auth/resetPasswordChange.html'
_M='captcha'
_L='password'
_K='POST'
_J=False
_I='login'
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 as qube_9d6a4fd676
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_70235a51be
from project.sparta_6e115c4929.sparta_e75895c000 import qube_10154d16cf as qube_10154d16cf
from project.sparta_5cad2eeda5.sparta_e084e5f78d import qube_5cf06519cf as qube_5cf06519cf
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_b4b318b4e9():return{'bHasCompanyEE':-1}
def sparta_d8da99d398(request):B=request;A=qube_9d6a4fd676.sparta_6908dae5fe(B);A[_C]=qube_9d6a4fd676.sparta_0645c490a6();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_70235a51be
def sparta_f98e5ddd99(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_d41bc7fa48(C,A)
def sparta_9537e3750c(request,redirectUrl):return sparta_d41bc7fa48(request,redirectUrl)
def sparta_d41bc7fa48(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_10154d16cf.sparta_a6c32dbccd(F):return sparta_d8da99d398(A)
				login(A,F);K,L=qube_9d6a4fd676.sparta_4b3b08a1c6();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_9d6a4fd676.sparta_6908dae5fe(A);B.update(qube_9d6a4fd676.sparta_33c063a7dc(A));B[_C]=qube_9d6a4fd676.sparta_0645c490a6();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_b4b318b4e9());return render(A,'dist/project/auth/login.html',B)
def sparta_e9677877de(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_70235a51be
def sparta_ec8decaaee(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_10154d16cf.sparta_8a21f1dfe6()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_10154d16cf.sparta_4d5ce19932(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_10154d16cf.sparta_b9fee72991(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_9d6a4fd676.sparta_6908dae5fe(A);C.update(qube_9d6a4fd676.sparta_33c063a7dc(A));C[_C]=qube_9d6a4fd676.sparta_0645c490a6();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_b4b318b4e9());return render(A,'dist/project/auth/registration.html',C)
def sparta_c05ff4d752(request):A=request;B=qube_9d6a4fd676.sparta_6908dae5fe(A);B[_C]=qube_9d6a4fd676.sparta_0645c490a6();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_a058427a9b(request,token):
	A=request;B=qube_10154d16cf.sparta_54d6c9acd0(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_9d6a4fd676.sparta_6908dae5fe(A);D[_C]=qube_9d6a4fd676.sparta_0645c490a6();return redirect(_I)
def sparta_11165e4252(request):logout(request);return redirect(_I)
def sparta_6b3aadd8ac(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_6e0dd48e14(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_641087fa44(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_10154d16cf.sparta_641087fa44(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_9d6a4fd676.sparta_6908dae5fe(A);C.update(qube_9d6a4fd676.sparta_33c063a7dc(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_9d6a4fd676.sparta_0645c490a6();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_9d6a4fd676.sparta_6908dae5fe(A);D.update(qube_9d6a4fd676.sparta_33c063a7dc(A));D[_C]=qube_9d6a4fd676.sparta_0645c490a6();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_b4b318b4e9());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_63f48b6ca2(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_10154d16cf.sparta_63f48b6ca2(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_9d6a4fd676.sparta_6908dae5fe(D);A.update(qube_9d6a4fd676.sparta_33c063a7dc(D));A[_C]=qube_9d6a4fd676.sparta_0645c490a6();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_b4b318b4e9());return render(D,_N,A)