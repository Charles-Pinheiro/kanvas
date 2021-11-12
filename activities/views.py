from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from activities.models import Activity
from activities.permissions import FacilitatorInstructorPermission, StudentPermission
from activities.serializers import ActivityPUTSerializer, ActivitySerializer
from submissions.serializers import SubmissionSerializer


class ActivityView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [FacilitatorInstructorPermission]

    def post(self, request):
        data = request.data

        try:
            activity = Activity.objects.create(**data)
        except IntegrityError:
            return Response({'error': 'Activity with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serialized = ActivitySerializer(activity)

        return Response(serialized.data, status=status.HTTP_201_CREATED)


    def get(self, request):
        activities = Activity.objects.all()
        serialized = ActivitySerializer(activities, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


    def put(self, request, activity_id=''):
        try:
            activity = Activity.objects.get(id=activity_id)
        except Activity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if activity.submissions.count():
            return Response({'error': 'You can not change an Activity with submissions'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        serialized = ActivityPUTSerializer(data=data)
        serialized.is_valid(raise_exception=True)

        title = data['title']
        points = data['points']
        activity.title = title
        activity.points = points
        activity.save()

        serialized_return = ActivitySerializer(activity)

        return Response(serialized_return.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([StudentPermission, IsAuthenticated])
def submitting_activity(request, activity_id=''):
    try:
        activity = Activity.objects.get(id=activity_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data

    if 'grade' in data:
        data.pop('grade')

    data['user_id'] = request.user.id
    data['activity_id'] = activity.id
    submission = activity.submissions.create(**data)

    serialized = SubmissionSerializer(submission)

    return Response(serialized.data)
