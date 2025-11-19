from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


    
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    phone = models.CharField(max_length=15,blank=True,null=True)
    house_name = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True)
    district = models.CharField(max_length=100,blank=True, null=True)
    pin_code = models.CharField(max_length=10,blank=True,null=True)
    country = models.CharField(max_length=100,blank= True,null= True)
    address = models.CharField(max_length=100,blank=True, null = True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)  
    enrolled_date = models.DateTimeField(blank=True, null=True) 
    
    def __str__(self):
        return f"{self.user.username}'s details"
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    long_description = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True, related_name='courses_instructor')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    what_you_will_learn = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    requirements = models.TextField()
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    features = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.reviews.all()  # Make sure Review model has related_name='reviews'
        if reviews.exists():
            return sum([review.rating for review in reviews]) / reviews.count()
        return 0

    def clean(self):
        if self.is_paid and self.price <= 0:
            raise ValidationError("Paid courses must have a price greater than 0.")


class Curriculum(models.Model):
    course = models.ForeignKey(Course, related_name='curriculum_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)  # URL of the video
    duration = models.DurationField(blank=True, null=True)  # Duration of the video
    locked = models.BooleanField(default=False)  # Whether the item is locked or not

    def __str__(self):
        return self.title

class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.timestamp}"


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    courses = models.ManyToManyField(Course, related_name='instructors', blank=True)  
    bio = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def average_rating(self):
        reviews = self.reviews.all()  # Make sure Review model has related_name='reviews'
        if reviews.exists():
            return sum([review.rating for review in reviews]) / reviews.count()
        return 0


class Review(models.Model):
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, related_name='reviews', on_delete=models.SET_NULL, null=True, blank=True)  # Optional if instructors can be rated
    rating = models.IntegerField()  # You might want to validate this field to ensure it's between 1-5, etc.
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who gave the review
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


    class Meta:
        ordering = ['-created_at']  # Most recent reviews first

    def __str__(self):
        if self.course:
            return f"Review by {self.user.username} for {self.course.title}"
        elif self.instructor:
            return f"Review by {self.user.username} for {self.instructor.name}"
        return f"Review by {self.user.username}"
    
    def clean(self):
        # Ensure that either course or instructor is filled, but not both
        if not self.course and not self.instructor:
            raise ValidationError("You must specify either a course or an instructor.")
        if self.course and self.instructor:
            raise ValidationError("You can review either a course or an instructor, not both.")

    def save(self, *args, **kwargs):
        # Call the clean method before saving the object
        self.clean()
        super().save(*args, **kwargs)


class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='content_files/', blank=True, null=True)
    

    def __str__(self):
        return self.title
    
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    
    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

   
    def __str__(self):
        return f"Payment for {self.course.title} by {self.user.username} - {self.payment_status}"

class Section(models.Model):
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()  # Optional: to control the order of sections

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    section = models.ForeignKey(Section, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.URLField()  # URL to the video
    duration = models.CharField(max_length=10)  # Duration of the video
    is_preview = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback from {self.user.username} for {self.instructor.user.username} on {self.course.title}"

class Assignment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    text_submission = models.TextField(null=True, blank=True)
    file_submission = models.FileField(upload_to="assignments/", null=True, blank=True)
    link_submission = models.URLField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment.title} by {self.student.username}"
    
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=255)
    description = models.TextField()

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
        ('TEXT', 'Text Answer'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    options = models.JSONField(blank=True, null=True)  # For storing multiple choice options
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"
    
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Completed' if self.completed else 'Incomplete'}"
    
class Doubt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doubts")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="doubts", null=True, blank=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name="doubts", null=True, blank=True)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Doubt by {self.user.username} on {self.course.title if self.course else 'Lesson'}"

class Answer(models.Model):
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name="answers")
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Answer by {self.answered_by.username} for {self.doubt}"
