from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from app_habits.models import Habit
from app_habits.paginators import HabitPaginator
from app_habits.serializers import HabitNiceCreateSerializer, HabitGoodCreateSerializer, HabitListAllSerializer, \
    HabitListSerializer, HabitSerializer, HabitGoodUpdateSerializer
from app_habits.services import add_task, update_task, delete_task
from app_users.permissions import IsModerator, IsPublic, IsOwner


class HabitNiceCreateAPIView(CreateAPIView):
    """Habit Nice Create"""
    queryset = Habit.objects.all()
    serializer_class = HabitNiceCreateSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.is_nice = True
        new_habit.save()


class HabitGoodCreateAPIView(CreateAPIView):
    """Habit Good Create"""
    queryset = Habit.objects.all()
    serializer_class = HabitGoodCreateSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()
        add_task(new_habit)


class HabitListAPIView(ListAPIView):
    """Habit List"""
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = None
    filterset_fields = ('is_nice', )
    pagination_class = HabitPaginator

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Habit.objects.all()
        else:
            queryset = Habit.objects.filter(owner=self.request.user)

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            serializer_class = HabitListAllSerializer
            self.ordering_fields = ('id', 'task', 'start_time', 'location', 'periodic', 'is_nice', 'owner_email', )
        else:
            serializer_class = HabitListSerializer
            self.ordering_fields = ('id', 'task', 'start_time', 'location', 'periodic', 'is_nice', )

        return serializer_class


class HabitRetrieveAPIView(RetrieveAPIView):
    """Habit Retrive"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsPublic | IsOwner | IsModerator]


class HabitPublicListAPIView(ListAPIView):
    """Habit Public List"""
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitListAllSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('id', 'task', 'start_time', 'location', 'periodic', 'is_nice', 'owner_email', )
    filterset_fields = ('is_nice', )
    pagination_class = HabitPaginator


class HabitUpdateAPIView(UpdateAPIView):
    """Habit Update"""
    queryset = Habit.objects.all()
    lookup_field = 'pk'
    serializer_class = HabitGoodUpdateSerializer
    permission_classes = [IsOwner | IsModerator]

    def get_serializer_class(self):
        if self.get_object().is_nice:
            return HabitNiceCreateSerializer
        return HabitGoodUpdateSerializer

    def perform_update(self, serializer):
        obj = serializer.save()
        update_task(obj)


class HabitDestroyAPIView(DestroyAPIView):
    """Habit Delete"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]

    def perform_destroy(self, instance):
        delete_task(instance)
        instance.delete()
