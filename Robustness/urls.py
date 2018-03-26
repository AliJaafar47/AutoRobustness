from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'login_success/$', views.login_success, name='login_success')
]