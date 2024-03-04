from rest_framework import serializers

from app_habits.models import Habit
from app_habits.validators import (TimeToCompleteValidator, FillingNotOutTwoFieldsValidator,
                                   RelatedHabitOnlyNiceValidator)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class HabitNiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        exclude = ('start_time', 'periodic', 'related', 'reward')
        read_only_fields = ('owner', 'is_nice')
        validators = [
            TimeToCompleteValidator('time_to_complete'),
        ]


class HabitGoodCreateSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField()

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('owner', 'is_nice')
        validators = [
            FillingNotOutTwoFieldsValidator('related', 'reward'),
            TimeToCompleteValidator('time_to_complete'),
            RelatedHabitOnlyNiceValidator('related'),
        ]


class HabitGoodUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('owner', 'is_nice')
        validators = [
            FillingNotOutTwoFieldsValidator('related', 'reward'),
            TimeToCompleteValidator('time_to_complete'),
            RelatedHabitOnlyNiceValidator('related'),
        ]

    def update(self, instance, validated_data):

        if validated_data.get("related") and instance.reward:
            validated_data['reward'] = None
        elif validated_data.get("reward") and instance.related:
            validated_data['related'] = None
        instance = super().update(instance, validated_data)
        return instance


class HabitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('id', 'task', 'start_time', 'location', 'periodic', 'is_nice')


class HabitListAllSerializer(serializers.ModelSerializer):
    owner_email = serializers.SerializerMethodField()

    @staticmethod
    def get_owner_email(instance):
        owner_email = instance.owner.email
        return owner_email

    class Meta:
        model = Habit
        fields = ('id', 'task', 'start_time', 'location', 'periodic', 'is_nice', 'owner_email', )
