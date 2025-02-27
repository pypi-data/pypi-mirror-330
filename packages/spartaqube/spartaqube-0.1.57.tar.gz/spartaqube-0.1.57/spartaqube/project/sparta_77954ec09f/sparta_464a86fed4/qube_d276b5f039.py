from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_70235a51be
from project.sparta_6e115c4929.sparta_02e1308820 import qube_6b16dd5460 as qube_6b16dd5460
from project.models import UserProfile
import project.sparta_a3a543928a.sparta_9510f50e2d.qube_9d6a4fd676 as qube_9d6a4fd676
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_098c678324(request):
	E='avatarImg';B=request;A=qube_9d6a4fd676.sparta_6908dae5fe(B);A['menuBar']=-1;F=qube_9d6a4fd676.sparta_ec1b2d1f1a(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_70235a51be
@login_required(redirect_field_name='login')
def sparta_1c591c83f0(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_098c678324(A)