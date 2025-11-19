from django.urls import path
from . import views

app_name = 'instructorApp'

urlpatterns = [
    path('dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('course/<int:course_id>/create_assignment/', views.create_assignment, name='create_assignment'),
    # path('course/<int:course_id>/create_quiz/', views.create_quiz, name='create_quiz'),
    # path('quiz/<int:quiz_id>/add_question/', views.add_question, name='add_question'),
     path('instructor/courses/', views.instructor_courses, name='instructor_courses'),
    path('instructor/courses/add/', views.add_course, name='add_course'),
    path('instructor/courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('instructor/courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('add-quiz/', views.add_quiz, name='add_quiz'),
    path('add-question/', views.add_question, name='add_question'),
    path('assignments/', views.instructor_assignments, name='instructor_assignments'),
    path('assignments/add/', views.add_assignment, name='add_assignment'),
    path('assignments/<int:assignment_id>/submissions/', views.view_submissions, name='view_submissions'),
    path('students/', views.instructor_students, name='instructor_students'),
    path('students/', views.enrolled_students_view, name='enrolled_students'),

]
