from rest_framework import serializers
from .models import Checkin, Habit, User, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        