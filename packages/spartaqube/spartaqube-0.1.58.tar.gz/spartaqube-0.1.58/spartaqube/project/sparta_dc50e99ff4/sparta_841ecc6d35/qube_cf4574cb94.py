import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_484a14773c.sparta_53174f097f import qube_3e48869bf3 as qube_3e48869bf3
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_0389256417,sparta_adbbe5ebe9
@csrf_exempt
@sparta_0389256417
def sparta_4cb02703e8(request):A=request;B=json.loads(A.body);C=json.loads(B['jsonData']);D=qube_3e48869bf3.sparta_4cb02703e8(C,A.user);E=json.dumps(D);return HttpResponse(E)