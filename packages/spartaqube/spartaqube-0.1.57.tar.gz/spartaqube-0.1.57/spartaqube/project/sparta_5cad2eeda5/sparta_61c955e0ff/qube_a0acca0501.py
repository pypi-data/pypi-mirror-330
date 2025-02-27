import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_6e115c4929.sparta_d594bfd5a5 import qube_9a48145309 as qube_9a48145309
from project.sparta_6e115c4929.sparta_e75895c000.qube_10154d16cf import sparta_2b78ea6b23
@csrf_exempt
@sparta_2b78ea6b23
def sparta_21400bc07f(request):G='api_func';F='key';E='utf-8';A=request;C=A.body.decode(E);C=A.POST.get(F);D=A.body.decode(E);D=A.POST.get(G);B=dict();B[F]=C;B[G]=D;H=qube_9a48145309.sparta_21400bc07f(B,A.user);I=json.dumps(H);return HttpResponse(I)