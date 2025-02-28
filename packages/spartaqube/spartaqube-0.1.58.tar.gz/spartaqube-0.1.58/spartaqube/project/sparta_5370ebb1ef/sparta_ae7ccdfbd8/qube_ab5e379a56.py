import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 as qube_75fd5cec11
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_f07707f6fc
from project.sparta_484a14773c.sparta_174d7f1491 import qube_e464ab5335 as qube_e464ab5335
from project.sparta_484a14773c.sparta_fe12f7b7e4 import qube_2c42c6daa9 as qube_2c42c6daa9
def sparta_3085de03fe():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_83cf711dc1(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_75fd5cec11.sparta_2e0feef849(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_75fd5cec11.sparta_2e0feef849(B);A['menuBar']=12;F=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)