from django.urls import path

from activities.views import ActivityView, submitting_activity


urlpatterns = [
    path('activities/', ActivityView.as_view()),
    path('activities/<int:activity_id>/', ActivityView.as_view()),
    path('activities/<int:activity_id>/submissions/', submitting_activity),
]
