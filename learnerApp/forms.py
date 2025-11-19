# forms.py
from django import forms
from AdminpanelApp.models import UserDetails,Enrollment,Feedback,Review,Doubt

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['phone', 'house_name', 'state', 'district', 'pin_code', 'country', 'profile_picture','address']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        
        model = Enrollment
        fields =['user','course']


class FreeEnrollmentForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        label="First Name",
        max_length=100
    )
    last_name = forms.CharField(
        required=True,
        label="Last Name",
        max_length=100
    )
    email = forms.EmailField(
        required=True,
        label="Email Address"
    )
    phone_number = forms.CharField(
        required=False,
        label="Phone Number",
        max_length=15,
        help_text="Optional: Include your phone number for further communication."
    )
    confirm_enrollment = forms.BooleanField(
        required=True,
        label="I confirm that I want to enroll in this course."
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Rate the Course',
            'comment': 'Your Review',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['instructor', 'rating', 'comment']
        widgets = {
            'instructor': forms.HiddenInput(),  # Optionally hide this if instructor is set automatically
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),  # Rating out of 5
        }




class DoubtForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ["question","lesson"]
