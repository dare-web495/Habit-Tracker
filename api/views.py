from django.shortcuts import render
from rest_framework import viewsets
from .models import Habit, Category, User, Checkin
from .serializers import UserSerializer, CheckinSerializer, HabitSerializer, CategorySerializer

# Create your views here.
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
