from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'patient_landing$', views.patient_landing),
    url(r'home$', views.home),
    url(r'login_html$', views.login_html),
    url(r'login_method$', views.login_method),
    url(r'register_html$', views.register_html),
    # url(r'update_health/(?P<number>\d)$', views.update_health),
    url(r'update_health$', views.update_health),
    url(r'registration_method$', views.registration_method),
    url(r'dashboard_html$', views.dashboard_html),
    url(r'that_info_html$', views.that_info_html),
    url(r'edit_profile_html$', views.edit_profile_html),
    url(r'logout$', views.logout),
    url(r'about$', views.about),
    url(r'update_health$', views.update_health)
]
