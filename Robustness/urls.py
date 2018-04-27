from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'login_success/$', views.login_success, name='login_success'),
    url(r'after_login/$', views.after_login, name='after_login'),
    url(r'update/$', views.update, name='update')
]