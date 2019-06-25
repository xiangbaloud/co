from django.conf.urls import url, include
from django.urls import path
import django_eventstream
from . import views

urlpatterns = [
    path('', views.homepage, name='hp'),
    path('hp_run_testing', views.hp_run_testing),
    path('hp_checkout_git', views.hp_checkout_git),
    path('hp_gen_result_html', views.hp_gen_result_html),
    path('hp_chk_case', views.hp_chk_test_case),
    path('hp_user_upload', views.hp_user_upload),
    path('hp_restart_server', views.hp_restart_server),
]