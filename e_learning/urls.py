"""
URL configuration for e_learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from homeapp import views as home_views  # Adjust import as per your app structure

urlpatterns = [
    path('admin/', admin.site.urls),
    path('siteadmin/', include('AdminpanelApp.urls',namespace='AdminpanelApp')),
    path('instructor/', include('instructorApp.urls',namespace='instructorApp')),
    path('learner/', include('learnerApp.urls',namespace='learnerApp')),
    path('payment/',include('paymentapp.urls',namespace='payment')),
    path('', home_views.home, name='home'),  # Assuming 'home_views' is imported correctly
    path('admin_dash/', home_views.admin_dashboard, name='admin'),
    path('instructor_dash/', home_views.instructor_dashboard, name='instructor'),
    path('learner_dash/', home_views.learner_dashboard, name='learner'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', home_views.login_view, name='login'),
    path('logout/', home_views.logout_view, name='logout'),
    path('signup/',home_views.sign_up,name='signup'),
    path('reset/',home_views.Resethome,name='reset'),
    path('passwordreset/',home_views.ResetPassword,name='passwordreset'),
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

