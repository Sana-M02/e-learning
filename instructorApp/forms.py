from django import forms
from AdminpanelApp.models import Assignment, Quiz, Question,Course

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course','title', 'instructions', 'due_date' ]

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'correct_answer']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']