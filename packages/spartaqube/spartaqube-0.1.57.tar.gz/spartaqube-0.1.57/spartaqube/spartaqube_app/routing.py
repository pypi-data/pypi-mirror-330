import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_a3a543928a.sparta_78b07076a0 import qube_77796988b0,qube_3f9f6ac960,qube_d98075a529,qube_43c7131df9,qube_c2c666809f,qube_c1b4af78dc,qube_db814ee9d1,qube_0afd23b122,qube_af5d4020a7
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
def sparta_966a9241a7(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_966a9241a7(qube_77796988b0.StatusWS)),url('ws/notebookWS',sparta_966a9241a7(qube_3f9f6ac960.NotebookWS)),url('ws/wssConnectorWS',sparta_966a9241a7(qube_d98075a529.WssConnectorWS)),url('ws/pipInstallWS',sparta_966a9241a7(qube_43c7131df9.PipInstallWS)),url('ws/gitNotebookWS',sparta_966a9241a7(qube_c2c666809f.GitNotebookWS)),url('ws/xtermGitWS',sparta_966a9241a7(qube_c1b4af78dc.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_966a9241a7(qube_db814ee9d1.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_966a9241a7(qube_0afd23b122.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_966a9241a7(qube_af5d4020a7.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)