from django.urls import path
from . import views

app_name = 'learnerApp'

urlpatterns = [
    path('learner_dash/',views.learner_dash,name='learner_dash'),
    path('search/', views.search_courses, name='search_courses'),
    path('courses/', views.course, name='course_list'), 
    path('category/',views.categories,name='category'),
    path('profile/',views.profile,name='profile'),
    path('course_detail/<int:course_id>/',views.course_detail,name='course_detail'),
    path('instructor/<int:id>/',views.instructor_detail, name='instructor_detail'),
    path('course/<int:course_id>/', views.lectures, name='lectures'),
    path('submit_review/', views.submit_review_for_lecture, name='submit_review_for_lecture'),
    path('profile/create/',views.create_or_update_profile,name='create_or_update'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('payment/<int:course_id>/', views.payment_page, name='payment_page'),
    path('course/<int:course_id>/enroll_free/', views.enroll_free, name='enroll_free'),
    path("ask-doubt/<int:course_id>/", views.ask_doubt, name="ask_doubt"),
    path('submit-assignment/<int:assignment_id>/',views.submit_assignment, name='submit_assignment'),

    
    
]