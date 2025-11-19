from django.urls import path
from . import views

app_name= 'AdminpanelApp'

urlpatterns = [
    path('admin_dash/', views.admin_dash, name='admin-dash'),
    path('users/', views.manage_users, name='manage-users'),
    path('users/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle-user-status'),
    path('users/promote/<int:user_id>/', views.promote_to_instructor, name='promote-user'),
    # path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    # path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    # path('courses/', views.manage_courses, name='manage-courses'),
    # path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    # path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    # path('enrollments/', views.manage_enrollments, name='manage-enrollments'),
    # path('payments/', views.manage_payments, name='manage-payments'),
    # path('reviews/', views.manage_reviews, name='manage-reviews'),
    # path('categories/', views.manage_categories, name='manage-categories'),
    path('instructors/', views.manage_instructors, name='manage-instructors'),
    path('instructors/<int:instructor_id>/',views.view_instructor_profile, name='view-instructor-profile'),
    path('instructors/delete/<int:instructor_id>/',views.delete_instructor, name='delete-instructor'),


    # path('reports/', views.view_reports, name='view-reports'),
    # path('settings/', views.admin_settings, name='admin-settings'),
  
]
