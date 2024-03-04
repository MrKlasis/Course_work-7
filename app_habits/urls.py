from django.urls import path

from app_habits.apps import AppHabitsConfig
from app_habits.views import HabitNiceCreateAPIView, HabitGoodCreateAPIView, HabitListAPIView, HabitPublicListAPIView, \
    HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView

app_name = AppHabitsConfig.name

urlpatterns = [
    path('habit/create/nice/', HabitNiceCreateAPIView.as_view(), name="habit_nice_create"),
    path('habit/create/good/', HabitGoodCreateAPIView.as_view(), name="habit_good_create"),
    path('habit/list/', HabitListAPIView.as_view(), name="habit_list"),
    path('habit/public_list/', HabitPublicListAPIView.as_view(), name="habit_public_list"),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name="habit_retrieve"),
    path('habit/<int:pk>/update/', HabitUpdateAPIView.as_view(), name="habit_update"),
    path('habit/<int:pk>/destroy/', HabitDestroyAPIView.as_view(), name="habit_destroy")
]
