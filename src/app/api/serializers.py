from rest_framework import serializers


class EvaluationAnswerSerializer(serializers.Serializer):
    criterion_id = serializers.IntegerField()
    score = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(allow_blank=True, allow_null=True, required=False)


class EvaluationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    event_id = serializers.IntegerField()
    evaluated_user_id = serializers.IntegerField()
    evaluator_user_id = serializers.IntegerField()
    type = serializers.CharField(required=False, default="360")
    created_at = serializers.DateTimeField(required=False)
    answers = EvaluationAnswerSerializer(many=True)

    def validate_answers(self, value):
        if not value:
            raise serializers.ValidationError("Debe incluir al menos una respuesta.")
        for answer in value:
            if answer["score"] < 1 or answer["score"] > 5:
                raise serializers.ValidationError("El puntaje debe estar entre 1 y 5.")
        return value


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    admin_id = serializers.IntegerField()

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError("La fecha de inicio no puede ser mayor a la de fin.")
        return attrs


class InternHoursSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    horas = serializers.IntegerField()
    horas_jul_oct = serializers.IntegerField()
    horas_acumuladas = serializers.IntegerField()
    horas_necesarias = serializers.IntegerField()
    horas_restantes_2212 = serializers.IntegerField()
    falta_sobra = serializers.IntegerField()
    faltaria_sobraria = serializers.IntegerField()
    total = serializers.IntegerField()
    cumplimiento_pct = serializers.IntegerField()
