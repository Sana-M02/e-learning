
from django.urls import path
from . import views

app_name = 'homeapp'

urlpatterns = [

    path('', views.home, name='home'),
    path('admin_dash/', views.admin_dashboard, name='admin'),
    path('instructor_dash/', views.instructor_dashboard, name='instructor'),
    path('learner_dash/', views.learner_dashboard, name='learner'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.sign_up, name='signup'),
    path('reset/',views.Resethome,name='reset'),
    path('passwordreset/',views.ResetPassword,name='passwordreset'),
    
]

