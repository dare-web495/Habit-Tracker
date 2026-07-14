from rest_framework import serializers
from .models import Checkin, Habit, User, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkin
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    checkin_set = CheckinSerializer(many=True, read_only=True)
    
    class Meta:
        model = Habit
        fields = ['user', 'habit_name', 'frequency', 'created_date', 'category', 'checkin_set']
