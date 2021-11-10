from rest_framework import serializers


class CourseUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    users = CourseUserSerializer(many=True)


class CoursePutNameSerializer(serializers.Serializer):
    name = serializers.CharField()


class CoursePutUsersSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())
