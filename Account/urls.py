from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('logout/', log_out, name='logout'),
    path('reg/', registration_page, name='reg'),
    path('prof/', prof_page, name='prof'),
    path('forget_pass/', forget_pass, name='forget_pass'),
]
