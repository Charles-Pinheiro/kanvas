from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from courses.models import Course
from courses.permissions import InstructorPermission
from courses.serializers import (CoursePutNameSerializer,
                                 CoursePutUsersSerializer, CourseSerializer)


class CourseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [InstructorPermission]

    def post(self, request):
        data = request.data

        try:
            course = Course.objects.create(**data)
        except IntegrityError:
            return Response({'error': 'Course with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serialized = CourseSerializer(course)

        return Response(serialized.data, status=status.HTTP_201_CREATED)


    def get(self, request, course_id=''):
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                serialized = CourseSerializer(course)
                return Response(serialized.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'errors': 'invalid course_id'}, status=status.HTTP_404_NOT_FOUND)

        courses = Course.objects.all()
        serialized = CourseSerializer(courses, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


    def put(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serialized = CoursePutNameSerializer(data=data)
        serialized.is_valid(raise_exception=True)

        name = data['name']
        course.name = name
        course.save()

        serialized_return = CourseSerializer(course)

        return Response(serialized_return.data, status=status.HTTP_200_OK)


    def delete(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, InstructorPermission])
def update_students_in_course(request, course_id):

    data = request.data
    serialized_request = CoursePutUsersSerializer(data=data)
    serialized_request.is_valid(raise_exception=True)
    user_ids = data['user_ids']

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({'errors': 'invalid course_id'}, status=status.HTTP_404_NOT_FOUND)

    list_ids = []
    for id in user_ids:
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'errors': 'invalid user_id list'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_staff == True or user.is_superuser == True:
            return Response({'errors': 'Only students can be enrolled in the course.'}, status=status.HTTP_400_BAD_REQUEST)

        list_ids.append(user)

    course.users.set(list_ids)

    serialized = CourseSerializer(course)

    return Response(serialized.data)
