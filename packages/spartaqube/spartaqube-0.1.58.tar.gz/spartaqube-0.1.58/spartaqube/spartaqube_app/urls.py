from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_5370ebb1ef.sparta_e563c04907.qube_a612b6fbc2.sparta_c2d7c269ad'
handler500='project.sparta_5370ebb1ef.sparta_e563c04907.qube_a612b6fbc2.sparta_1326318a0d'
handler403='project.sparta_5370ebb1ef.sparta_e563c04907.qube_a612b6fbc2.sparta_8081702009'
handler400='project.sparta_5370ebb1ef.sparta_e563c04907.qube_a612b6fbc2.sparta_ef7f54d6ce'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]