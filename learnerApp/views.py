from django.shortcuts import render,redirect,get_object_or_404
from AdminpanelApp.models import Course,Category,Content,Review,Submission
from django.contrib.auth.decorators import login_required
from AdminpanelApp.models import UserDetails,Instructor,Enrollment,Section,Assignment,Quiz,Lesson
from .forms import UserDetailsForm,FreeEnrollmentForm,CourseReviewForm,DoubtForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def learner_dash(request):
    categories = Category.objects.all()
    courses = Course.objects.all()
    assignments = Assignment.objects.all()
    quizzes = Quiz.objects.all()

    
    search_query = request.GET.get('search', '')

    
    category_filter = request.GET.get('category')
    if category_filter:
        courses = courses.filter(category__name=category_filter)

    
    if search_query:
        courses = courses.filter(title__icontains=search_query)

    context = {
        'courses': courses,
        'categories': categories,
        'assignments': assignments,
        'quizzes': quizzes
    }

    return render(request, 'learnerApp/learner_dash.html', context)

def search_courses(request):
    query = request.GET.get('search')
    if query:
        
        courses = Course.objects.filter(title__icontains=query)
        if courses.exists():
            
            return redirect('learnerApp:course_detail', course_id=courses.first().id)
        else:
            
            return render(request, 'search_no_results.html', {'query': query})
    else:
        return redirect('home')

def course(request):
    courses= Course.objects.all()
    return render(request,'courses.html',{'courses' : courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    total_students = Enrollment.objects.filter(course=course).count()
    curriculum_items = course.curriculum_items.all()
    user_enrolled = False

    if request.user.is_authenticated:
        user_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    return render(request, 'course_detail.html', {
        'course': course,
        'total_students': total_students,
        'curriculum_items': curriculum_items,
        'user_enrolled': user_enrolled
    })

def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'learner_dash.html', context)


@login_required
def profile(request):

    userdetails, created = UserDetails.objects.get_or_create(user=request.user)
    
    
    enrollments = Enrollment.objects.select_related('course').filter(user=request.user)
    
    
    return render(request, 'profile.html', {
        'enrollments': enrollments,
        'userdetails': userdetails
    })

def instructor_detail(request, instructor_id):
    instructor = Instructor.objects.get(id=instructor_id)
    instructor_reviews = instructor.instructor_reviews.all()  
    return render(request, 'instructor_detail.html', {
        'instructor': instructor,
        'instructor_reviews': instructor_reviews
    })

def lectures(request, course_id):

    course = get_object_or_404(Course, id=course_id)
    

    sections = Section.objects.filter(course=course).order_by('order')
    
    context = {
        'course': course,
        'sections': sections,
    }
    
    return render(request, 'lectures.html', context)




@csrf_exempt
def submit_review_for_lecture(request):
    if request.method == 'POST':
        lecture_id = request.POST.get('lecture_id')
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        user = request.user

        try:
            content = Content.objects.get(id=lecture_id)
        except Content.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Lecture not found'}, status=404)

        
        review, created = Review.objects.update_or_create(
            content=content,
            user=user,
            defaults={'rating': rating, 'comment': comment}
        )

        course = content.course
        average_rating = course.average_rating()

        return JsonResponse({'status': 'success', 'average_rating': average_rating})

    return JsonResponse({'status': 'error'}, status=400)


def create_or_update_profile(request):
    try:
        user_details, created = UserDetails.objects.get_or_create(user=request.user)
    except IntegrityError:
        return redirect(' update_profile' )
    
    if request.method == 'POST':
        form = UserDetailsForm(request.POST, request.FILES, instance=user_details)
        if form.is_valid():
            user_details = form.save(commit=False)
            user_details.user = request.user
            user_details.save()
            return redirect('learnerApp:profile')
    else:
        form = UserDetailsForm(instance= user_details)

    return render(request, 'update_profile.html', {'form': form})




def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if course.is_paid:
        
        return redirect('payment_page', course_id=course.id)
    else:
        
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        if created:
            
            return redirect('course_detail', course_id=course.id)
        else:
            
            return redirect('course_detail', course_id=course.id)
        
def payment_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if course.price > 0:
        
        return redirect(reverse('payment:create_order', args=[course_id]))

    
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        return redirect('course_detail', course_id=course.id)
    else:
        return redirect('course_detail', course_id=course.id)

def enroll_free(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_paid=False)

    if request.method == 'POST':
        form = FreeEnrollmentForm(request.POST)
        if form.is_valid():
            
            if Enrollment.objects.filter(user=request.user, course=course).exists():
                messages.info(request, 'You are already enrolled in this course.')
                return redirect('learnerApp:lectures', course_id=course.id)

            
            Enrollment.objects.create(user=request.user, course=course)

            
            profile, created = UserDetails.objects.get_or_create(user=request.user)
        
            profile.phone = form.cleaned_data.get('phone', profile.phone)
            profile.address = form.cleaned_data.get('address', profile.address)
            profile.save()

            messages.success(request, f'You have successfully enrolled in {course.title}!')
            return redirect('learnerApp:lectures', course_id=course.id)  
    else:
        form = FreeEnrollmentForm()

    return render(request, 'enroll_free.html', {'form': form, 'course': course})

def submit_course_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseReviewForm()
    return render(request, 'course_review.html', {'form': form, 'course': course})


@login_required
def ask_doubt(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = DoubtForm(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.user = request.user
            doubt.course = course

            
            lesson_id = request.POST.get("lesson_id")
            if lesson_id:
                try:
                    lesson = Lesson.objects.get(id=lesson_id)
                    doubt.lesson = lesson
                except Lesson.DoesNotExist:
                    pass

            doubt.save()
            messages.success(request, "Your doubt has been submitted.")
            return redirect("learnerApp:lectures", course_id=course_id)
    else:
        form = DoubtForm()

    return render(request, "ask_doubt.html", {
        "form": form,
        "course": course
    })



@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST':
        submission_type = request.POST.get('submission_type')
        text = request.POST.get('text_submission') if submission_type == 'text' else None
        file = request.FILES.get('file_submission') if submission_type == 'file' else None
        link = request.POST.get('link_submission') if submission_type == 'link' else None

        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            text_submission=text,
            file_submission=file,
            link_submission=link,
        )
        messages.success(request, "Assignment submitted successfully!")
        return redirect('learnerApp:course_detail', course_id=assignment.course.id)
