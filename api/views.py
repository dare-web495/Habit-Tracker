from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category, Checkin, Habit, User
from .serializers import (
    CategorySerializer,
    CheckinSerializer,
    HabitSerializer,
    RegisterUserSerializer,
)

# Create my Permission class(es) here
class CustomPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        return obj.user == request.user

# Create your views here.
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    authentication_classes = [JWTAuthentication]
    # One class for ensuring only logged-in users access this feature 
    # another one for checking that the user owns this specific object.
    permission_classes = [IsAuthenticated, CustomPermission]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CheckinViewset(viewsets.ModelViewSet):
    queryset = Checkin.objects.all()
    serializer_class = CheckinSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

    def get_queryset(self):
        return Checkin.objects.filter(habit__user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
