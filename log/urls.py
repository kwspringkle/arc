from django.urls import path
from django.views.generic import TemplateView
from . import views 

app_name = 'log'

urlpatterns = [
    path('', views.render_home, name='home_page'),
    path('login/', views.render_login, name='login_page'),
    path('sys/login/', views.custom_login_view, name='login'),
    path('sys/logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name="signup"),
]