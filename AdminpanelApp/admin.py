from django.contrib import admin
from .models import UserDetails, Category, Course, Instructor, Content,Enrollment,Feedback,Curriculum,Section,Lesson,Assignment,Submission


# Register your models here.

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('course', 'instructor', 'user', 'rating', 'created_at')
    search_fields = ('course__title', 'instructor__username', 'user__username')
admin.site.register(UserDetails)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Content)
admin.site.register(Enrollment)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Curriculum)
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    inlines = [LessonInline]
admin.site.register(Section,SectionAdmin)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(Submission)