from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'login_success/$', views.login_success, name='login_success'),
    url(r'dashbord/$', views.dashbord, name='dashbord'),
    url(r'after_login/$', views.after_login, name='after_login'),
    url(r'save/$', views.save, name='save'),
    url(r'update/$', views.update, name='update'),
    url(r'start_flash/$', views.start_flash, name='start_flash'),
    
    #url(r'update_dashbord/$', views.update_dashbord, name='update_dashbord')
]