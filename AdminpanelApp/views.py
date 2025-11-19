from django.shortcuts import render,redirect,get_object_or_404
from .models import Course, Enrollment, Payment, Review, Instructor, UserDetails,User
from django.db.models import Avg
from django.contrib import messages


def admin_dash(request):
    total_courses = Course.objects.count()
    total_users = UserDetails.objects.count()
    total_instructors = Instructor.objects.count()
    total_enrollments = Enrollment.objects.count()
    total_payments = Payment.objects.count()
    average_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
    total_reviews = Review.objects.count()

    context = {
        'total_courses': total_courses,
        'total_users': total_users,
        'total_instructors': total_instructors,
        'total_enrollments': total_enrollments,
        'total_payments': total_payments,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
    }
    return render(request, 'admin_dash.html', context)



def manage_users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('AdminpanelApp:manage-users')

def promote_to_instructor(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if not hasattr(user, 'instructor_profile'):
        Instructor.objects.create(user=user, position='Instructor')
    return redirect('AdminpanelApp:manage-users')

def manage_instructors(request):
    instructors = Instructor.objects.select_related('user').all()
    return render(request, 'manage_instructors.html', {'instructors': instructors})

def view_instructor_profile(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'instructor_profile.html', {'instructor': instructor})

def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    user = instructor.user
    instructor.delete()
    user.delete()  # Optional: if you want to delete the user too
    messages.success(request, "Instructor deleted successfully.")
    return redirect('AdminpanelApp:manage-instructors')

def manage_courses(request):
    courses = Course.objects.select_related('instructor', 'category').all()
    return render(request, 'manage_courses.html', {'courses': courses})
