from django.urls import path
from . import views

app_name = 'paymentapp'

urlpatterns = [


    path('order/<int:course_id>/', views.create_order, name='create_order'),
    path('success/', views.payment_success, name='payment_success'),
    path('error/', views.error_page, name='error_page'),
]
