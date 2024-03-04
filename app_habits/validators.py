from rest_framework import serializers


class TimeToCompleteValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if time_to_complete := value.get(self.field):
            if time_to_complete > 120:
                raise serializers.ValidationError(f"Время выполнения должно быть не больше 120 секунд.")


class RelatedHabitOnlyNiceValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if habit_id := value.get(self.field):
            if not habit_id.is_nice:
                raise serializers.ValidationError(f'В поле "{self.field}" должна быть указана приятная привычка')


class FillingNotOutTwoFieldsValidator:

    def __init__(self, first_field, second_field, message=None):
        self.message = message
        self.first_field = first_field
        self.second_field = second_field

    def __call__(self, value):
        if value.get(self.first_field) and value.get(self.second_field):
            if not self.message:
                self.message = f'Недопустимо одновременно указывать "{self.first_field}" и "{self.second_field}"'
            raise serializers.ValidationError(self.message)


class FieldsIsNoneValidator:

    def __init__(self, *args, message=None):
        self.message = message
        self.fields = args

    def __call__(self, value):
        for field in self.fields:
            if value.get(field):
                if not self.message:
                    self.message = f'Запрещено заполнять поле "{field}""'
                raise serializers.ValidationError(self.message)
