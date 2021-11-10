from django.urls import path
from .views import create_course, update_name_course, update_students_in_course

urlpatterns = [
    path('courses/', create_course),
    path('courses/<int:course_id>/', update_name_course),
    path('courses/<int:course_id>/registrations/', update_students_in_course),
]