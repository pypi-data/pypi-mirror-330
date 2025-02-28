import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_f4d2d161ee.sparta_e6a5142dce import qube_4aac0093b6,qube_fd51281b16,qube_4a5943d757,qube_309a9c73ad,qube_2a89124f4b,qube_4c61d0989d,qube_d2aadcc66f,qube_a8f2a8ffa5,qube_4b24fcc255
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
def sparta_2029e29ca9(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_2029e29ca9(qube_4aac0093b6.StatusWS)),url('ws/notebookWS',sparta_2029e29ca9(qube_fd51281b16.NotebookWS)),url('ws/wssConnectorWS',sparta_2029e29ca9(qube_4a5943d757.WssConnectorWS)),url('ws/pipInstallWS',sparta_2029e29ca9(qube_309a9c73ad.PipInstallWS)),url('ws/gitNotebookWS',sparta_2029e29ca9(qube_2a89124f4b.GitNotebookWS)),url('ws/xtermGitWS',sparta_2029e29ca9(qube_4c61d0989d.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_2029e29ca9(qube_d2aadcc66f.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_2029e29ca9(qube_a8f2a8ffa5.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_2029e29ca9(qube_4b24fcc255.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)