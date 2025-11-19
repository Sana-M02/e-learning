from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.utils import timezone
from AdminpanelApp.models import Course, Enrollment, Doubt, Submission, Assignment,Instructor,Review,LoginActivity
from .forms import AssignmentForm, QuizForm, QuestionForm,CourseForm
from django.contrib import messages
from django.urls import reverse


@login_required
def instructor_dashboard(request):
    try:
        instructor = Instructor.objects.get(user=request.user)
    except Instructor.DoesNotExist:
        return render(request, 'error.html', {'message': 'Instructor profile not found'})

    # Fix many-to-many references
    total_courses = Course.objects.filter(instructors=instructor).count()
    enrolled_students = Enrollment.objects.filter(course__instructors=instructor).count()
    avg_rating = Review.objects.filter(course__instructors=instructor).aggregate(Avg('rating'))['rating__avg'] or 0
    submitted_assignments = Submission.objects.filter(assignment__course__instructors=instructor)

    # Debug prints
    print("Instructor:", instructor)
    print("Total Courses:", total_courses)
    print("Enrollments:", enrolled_students)
    print("Submitted Assignments:", submitted_assignments.count())

    context = {
        'total_courses': total_courses,
        'enrolled_students': enrolled_students,
        'avg_rating': round(avg_rating, 2),
        'submitted_assignments': submitted_assignments,
    }

    return render(request, 'instructor_dash.html', context)



@login_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            return redirect('instructorApp:instructor_dashboard')
    else:
        form = AssignmentForm()
    return render(request, 'create_assignment.html', {'form': form, 'course': course})


@login_required
def instructor_assignments(request):
    try:
        instructor = Instructor.objects.get(user=request.user)
    except Instructor.DoesNotExist:
        return render(request, 'error.html', {'message': 'Instructor profile not found'})

    assignments = Assignment.objects.filter(course__instructor=instructor).order_by('-due_date')
    return render(request, 'assignments.html', {
        'assignments': assignments
    })


@login_required
def add_assignment(request):
    try:
        instructor = Instructor.objects.get(user=request.user)
    except Instructor.DoesNotExist:
        messages.error(request, "You are not registered as an Instructor.")
        return redirect('instructorApp:instructor_dashboard')

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.save()
            messages.success(request, "Assignment added successfully!")
            return redirect('instructorApp:instructor_assignments')
    else:
        form = AssignmentForm()

    form.fields['course'].queryset = Course.objects.filter(instructor=instructor)
    return render(request, 'instructor/create_assignment.html', {'form': form})

@login_required
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if assignment.course.instructor.user != request.user:
        return render(request, 'error.html', {'message': 'Access denied.'})

    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'view_submission.html', {
        'assignment': assignment,
        'submissions': submissions
    })


def add_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructor_dashboard') 
    else:
        form = QuizForm()
    return render(request, 'instructorApp/add_quiz.html', {'form': form})

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructor_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'instructorApp/add_question.html', {'form': form})




@login_required
def instructor_courses(request):
    instructor = get_object_or_404(Instructor, user=request.user)
    courses = Course.objects.filter(instructor=instructor)
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def add_course(request):
    instructor = get_object_or_404(Instructor, user=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = instructor
            course.save()
            return redirect('instructorApp:instructor_courses')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor__user=request.user)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        return redirect('instructor_courses')
    return render(request, 'course_form.html', {'form': form})

@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect('instructor_courses')
    return render(request, 'confirm_delete.html', {
        'object': course,
        'object_name': 'course',
        'cancel_url': reverse('instructor_courses')
    })


@login_required
def instructor_students(request):
    instructor = request.user.instructor_profile

    courses = Course.objects.filter(instructor=instructor)
    enrollments = Enrollment.objects.filter(course__in=courses).select_related('user', 'course')

    
    for enrollment in enrollments:
        login_record = LoginActivity.objects.filter(user=enrollment.user).order_by('-timestamp').first()
        enrollment.last_login = login_record.timestamp if login_record else None

    context = {
        'enrollments': enrollments
    }
    return render(request, 'students.html', context)

@login_required
def enrolled_students_view(request):
    try:
        instructor = Instructor.objects.get(user=request.user)
    except Instructor.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not registered as an instructor.'})

    # Get students enrolled in this instructor’s courses
    enrollments = Enrollment.objects.filter(course__instructor=instructor).select_related('student', 'course')

    context = {
        'enrollments': enrollments
    }
    return render(request, 'instructorApp/enrolled_students.html', context)
