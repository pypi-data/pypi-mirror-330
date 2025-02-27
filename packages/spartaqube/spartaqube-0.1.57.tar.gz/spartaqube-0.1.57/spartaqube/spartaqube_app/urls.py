from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_77954ec09f.sparta_23c17e5c9b.qube_dc701281ab.sparta_1c38a45a45'
handler500='project.sparta_77954ec09f.sparta_23c17e5c9b.qube_dc701281ab.sparta_756850c16a'
handler403='project.sparta_77954ec09f.sparta_23c17e5c9b.qube_dc701281ab.sparta_7bf8d1e106'
handler400='project.sparta_77954ec09f.sparta_23c17e5c9b.qube_dc701281ab.sparta_a134a24fef'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]