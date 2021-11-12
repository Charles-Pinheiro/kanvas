from rest_framework import serializers

from submissions.serializers import SubmissionSerializer


class ActivitySerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField()
    points = serializers.FloatField()
    submissions = SubmissionSerializer(many=True)


class ActivityPUTSerializer(serializers.Serializer):

    title = serializers.CharField()
    points = serializers.FloatField()
