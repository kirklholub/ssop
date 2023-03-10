""" sites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from sites.views import getattrs, index, project_ldg, showattrs, attrsjwt, demoapp_python, demoapp_authorization, oops, connections_by_project, firewxtb, firewxoops

app_name = 'sites'

urlpatterns = [
    path('', index, name='index'),
    path('project_ldg/<str:projectname>/', project_ldg, name='project_ldg'),
    path('getattrs/<str:access_token>/', getattrs, name='getattrs'),
    path('showattrs/<str:access_token>/', showattrs, name='showattrs'),
    path('attrsjwt/<str:access_token>/', attrsjwt, name='attrsjwt'),
    path('demoapp_python/', demoapp_python, name='demoapp_python'),
    path('demoapp_authorization/', demoapp_authorization, name='demoapp_authorization'),
    path('connections_by_project/', connections_by_project, name='connections_by_project'),
    path('firewxtb/', firewxtb, name='firewxtb'),
    path('firewxoops/', firewxoops, name='firewxoops'),
]

