_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_6e115c4929.sparta_7e90ce45d3 import qube_9fb89acfae as qube_9fb89acfae
from project.sparta_6e115c4929.sparta_02e1308820 import qube_6b16dd5460 as qube_6b16dd5460
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_2b78ea6b23
@csrf_exempt
@sparta_2b78ea6b23
def sparta_4b4889bb2f(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_6b16dd5460.sparta_c5d7b2c056(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_9fb89acfae.sparta_4b4889bb2f(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_2b78ea6b23
def sparta_86048bf82b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9fb89acfae.sparta_c960b78e53(C,A.user);E=json.dumps(D);return HttpResponse(E)