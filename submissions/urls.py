from django.urls import path

from submissions.views import grade_submission, list_submissions


urlpatterns = [
    path('submissions/', list_submissions),
    path('submissions/<int:submission_id>/', grade_submission),
]
