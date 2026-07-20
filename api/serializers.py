from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Checkin, Habit, User, Category


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'validators': [validate_password]}}
        
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


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
