import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_484a14773c.sparta_3f50db5747 import qube_5ffca09007 as qube_5ffca09007
from project.sparta_484a14773c.sparta_074ed274f8.qube_910775047c import sparta_0389256417
@csrf_exempt
@sparta_0389256417
def sparta_3f3b3d3e2d(request):G='api_func';F='key';E='utf-8';A=request;C=A.body.decode(E);C=A.POST.get(F);D=A.body.decode(E);D=A.POST.get(G);B=dict();B[F]=C;B[G]=D;H=qube_5ffca09007.sparta_3f3b3d3e2d(B,A.user);I=json.dumps(H);return HttpResponse(I)