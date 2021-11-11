from django.urls import path
from .views import CourseView, update_students_in_course

urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/<int:course_id>/', CourseView.as_view()),
    path('courses/<int:course_id>/registrations/', update_students_in_course),
]
