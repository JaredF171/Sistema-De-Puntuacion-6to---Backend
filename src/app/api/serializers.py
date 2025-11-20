from rest_framework import serializers


class EvaluationAnswerSerializer(serializers.Serializer):
    criterion_id = serializers.IntegerField()
    score = serializers.IntegerField()
    comment = serializers.CharField(allow_blank=True, allow_null=True, required=False)


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    admin_id = serializers.IntegerField()


class EvaluationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    event_id = serializers.IntegerField()
    evaluated_user_id = serializers.IntegerField()
    evaluator_user_id = serializers.IntegerField()
    type = serializers.CharField(default="360", required=False)
    created_at = serializers.DateTimeField(required=False)
    answers = EvaluationAnswerSerializer(many=True)
from rest_framework import serializers


class EvaluationAnswerSerializer(serializers.Serializer):
    criterion_id = serializers.IntegerField()
    score = serializers.IntegerField()
    comment = serializers.CharField(allow_blank=True, allow_null=True, required=False)


class EvaluationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    event_id = serializers.IntegerField()
    evaluated_user_id = serializers.IntegerField()
    evaluator_user_id = serializers.IntegerField()
    type = serializers.CharField(required=False, default="360")
    created_at = serializers.DateTimeField(required=False)
    answers = EvaluationAnswerSerializer(many=True)


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    admin_id = serializers.IntegerField()
