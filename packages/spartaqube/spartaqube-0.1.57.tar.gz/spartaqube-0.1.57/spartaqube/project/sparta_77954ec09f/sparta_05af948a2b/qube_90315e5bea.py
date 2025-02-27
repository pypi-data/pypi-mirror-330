import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 as qube_9d6a4fd676
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_70235a51be
from project.sparta_6e115c4929.sparta_75ef90b243 import qube_63d9ee8418 as qube_63d9ee8418
from project.sparta_6e115c4929.sparta_60f8ddbc72 import qube_2208bfd19f as qube_2208bfd19f
def sparta_be18fe394d():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_836209627c(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_9d6a4fd676.sparta_6908dae5fe(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_9d6a4fd676.sparta_6908dae5fe(B);A['menuBar']=12;F=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)