"""onreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from onreview_app.views import views, auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.list),
    url(r'^post/(\d)+', views.post),
    url(r'^comment/(\d)+', views.comment),
    url(r'^add/$', views.add_post),
    url(r'^login/$', auth_views.login_request),
    url(r'^logout/$', auth_views.logout_request),
]
