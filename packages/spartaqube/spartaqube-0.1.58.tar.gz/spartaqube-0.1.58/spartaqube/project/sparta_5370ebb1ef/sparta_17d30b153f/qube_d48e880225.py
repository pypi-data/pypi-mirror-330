from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 as qube_75fd5cec11
from project.models import UserProfile
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_f07707f6fc
from project.sparta_5370ebb1ef.sparta_ea1f4b0daa.qube_b3acc58fb8 import sparta_839aacc89f
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_146565c122(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_75fd5cec11.sparta_2e0feef849(B);A.update(qube_75fd5cec11.sparta_62dea9d26b(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_839aacc89f());return render(B,'dist/project/auth/settings.html',A)