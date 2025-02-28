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
import project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 as qube_75fd5cec11
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_f07707f6fc
from project.sparta_484a14773c.sparta_074ed274f8 import qube_910775047c as qube_910775047c
from project.sparta_dc50e99ff4.sparta_2d9897ee04 import qube_eadb694212 as qube_eadb694212
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_839aacc89f():return{'bHasCompanyEE':-1}
def sparta_72a215fc0b(request):B=request;A=qube_75fd5cec11.sparta_2e0feef849(B);A[_C]=qube_75fd5cec11.sparta_72ad9303fc();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_f07707f6fc
def sparta_fad3310e4a(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_2960335b2f(C,A)
def sparta_3bb20ac8af(request,redirectUrl):return sparta_2960335b2f(request,redirectUrl)
def sparta_2960335b2f(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_910775047c.sparta_3e57821fe7(F):return sparta_72a215fc0b(A)
				login(A,F);K,L=qube_75fd5cec11.sparta_c9fd29b952();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_75fd5cec11.sparta_2e0feef849(A);B.update(qube_75fd5cec11.sparta_ffb32fb778(A));B[_C]=qube_75fd5cec11.sparta_72ad9303fc();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_839aacc89f());return render(A,'dist/project/auth/login.html',B)
def sparta_43d1848c28(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_f07707f6fc
def sparta_a2e3d412b0(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_910775047c.sparta_0e610efeb5()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_910775047c.sparta_674576dfe3(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_910775047c.sparta_beb01333b9(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_75fd5cec11.sparta_2e0feef849(A);C.update(qube_75fd5cec11.sparta_ffb32fb778(A));C[_C]=qube_75fd5cec11.sparta_72ad9303fc();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_839aacc89f());return render(A,'dist/project/auth/registration.html',C)
def sparta_0e07eda005(request):A=request;B=qube_75fd5cec11.sparta_2e0feef849(A);B[_C]=qube_75fd5cec11.sparta_72ad9303fc();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_64a1bc5a7d(request,token):
	A=request;B=qube_910775047c.sparta_4f627e7c7d(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_75fd5cec11.sparta_2e0feef849(A);D[_C]=qube_75fd5cec11.sparta_72ad9303fc();return redirect(_I)
def sparta_d5baa7cf41(request):logout(request);return redirect(_I)
def sparta_eb17922d6a(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_0097a68db8(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_9ecfd6d434(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_910775047c.sparta_9ecfd6d434(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_75fd5cec11.sparta_2e0feef849(A);C.update(qube_75fd5cec11.sparta_ffb32fb778(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_75fd5cec11.sparta_72ad9303fc();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_75fd5cec11.sparta_2e0feef849(A);D.update(qube_75fd5cec11.sparta_ffb32fb778(A));D[_C]=qube_75fd5cec11.sparta_72ad9303fc();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_839aacc89f());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_6d3b76c222(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_910775047c.sparta_6d3b76c222(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_75fd5cec11.sparta_2e0feef849(D);A.update(qube_75fd5cec11.sparta_ffb32fb778(D));A[_C]=qube_75fd5cec11.sparta_72ad9303fc();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_839aacc89f());return render(D,_N,A)