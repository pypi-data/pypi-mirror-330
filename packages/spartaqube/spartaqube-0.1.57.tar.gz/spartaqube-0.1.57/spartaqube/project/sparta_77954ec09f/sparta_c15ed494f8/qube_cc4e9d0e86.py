from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 as qube_9d6a4fd676
from project.models import UserProfile
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_70235a51be
from project.sparta_77954ec09f.sparta_0be1b6e707.qube_d8aed3cb47 import sparta_b4b318b4e9
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_556acf6a0d(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_9d6a4fd676.sparta_6908dae5fe(B);A.update(qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_b4b318b4e9());return render(B,'dist/project/auth/settings.html',A)