from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Habit, Category, Checkin
from .serializers import CheckinSerializer, HabitSerializer, CategorySerializer


# Create your views here.
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(self.request.user)

class CheckinViewset(viewsets.ModelViewSet):
    queryset = Checkin.objects.all()
    serializer_class = CheckinSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Checkin.objects.filter(self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(self.request.user)
