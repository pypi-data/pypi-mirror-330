_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_484a14773c.sparta_c876e82228 import qube_6f32d38a85 as qube_6f32d38a85
from project.sparta_484a14773c.sparta_16c4b9ee2e import qube_67d3865db3 as qube_67d3865db3
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_0389256417
@csrf_exempt
@sparta_0389256417
def sparta_23879af141(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_67d3865db3.sparta_6480a6f058(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_6f32d38a85.sparta_23879af141(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_0389256417
def sparta_a5e4733b9d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6f32d38a85.sparta_90f4a579fe(C,A.user);E=json.dumps(D);return HttpResponse(E)