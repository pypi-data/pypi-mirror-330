from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_f07707f6fc
from project.sparta_484a14773c.sparta_16c4b9ee2e import qube_67d3865db3 as qube_67d3865db3
from project.models import UserProfile
import project.sparta_f4d2d161ee.sparta_71327ad382.qube_75fd5cec11 as qube_75fd5cec11
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_69080032d2(request):
	E='avatarImg';B=request;A=qube_75fd5cec11.sparta_2e0feef849(B);A['menuBar']=-1;F=qube_75fd5cec11.sparta_62dea9d26b(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_f07707f6fc
@login_required(redirect_field_name='login')
def sparta_3019eaee1f(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_69080032d2(A)