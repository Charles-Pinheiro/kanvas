from activities.permissions import FacilitatorInstructorPermission
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from submissions.models import Submission
from submissions.serializers import SubmissionSerializer


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([FacilitatorInstructorPermission])
def grade_submission(request, submission_id=''):
    try:
        submission = Submission.objects.get(id=submission_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data

    submission.grade = data['grade']
    submission.save()

    serialized = SubmissionSerializer(submission)

    return Response(serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_submissions(request):

    if not request.user.is_staff and  not request.user.is_superuser:
        submissions = Submission.objects.filter(user_id=request.user.id)
        serialized = SubmissionSerializer(submissions, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    submissions = Submission.objects.all()
    serialized = SubmissionSerializer(submissions, many=True)
    return Response(serialized.data, status=status.HTTP_200_OK)
