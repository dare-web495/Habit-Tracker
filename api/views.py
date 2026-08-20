from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, viewsets 
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response

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
    
    @action(detail=True, methods=['get'], url_path='stats')
    def stats(self, request, pk=None):
        habit = self.get_object()
        
        checkin_date = list(
            Checkin.objects.filter(habit=habit)
            .values_list('date', flat=True)
            .order_by('date')
        )
        
        today = timezone.localdate()
        
        if habit.frequency == 'daily' or habit.frequency == 'Daily':
            stats = self._calculate_daily_stats(habit, checkin_date, today)
        else:
            stats = self._calculate_weekly_stats(habit, checkin_date, today)
            
        return Response(stats, status=status.HTTP_200_OK)
    
    def _calculate_daily_stats(self, habit, check_in_dates, today):
        yesterday = today - timedelta(days=1)
        current_streak = 0
        longest_streak = 0

        if check_in_dates:
            # current streak calculation
            last_check_in = check_in_dates[-1]
            if last_check_in == today or last_check_in == yesterday:
                current_streak = 1
                for i in range(len(check_in_dates) - 1, 0, -1):
                    if check_in_dates[i] - check_in_dates[i - 1] == timedelta(days=1):
                        current_streak += 1
                    else:
                        break

            # longest streak calculation
            temp_streak = 1
            longest_streak = 1
            for i in range(1, len(check_in_dates)):
                if check_in_dates[i] - check_in_dates[i - 1] == timedelta(days=1):
                    temp_streak += 1
                else:
                    longest_streak = max(longest_streak, temp_streak)
                    temp_streak = 1
            longest_streak = max(longest_streak, temp_streak)

        # coompletion rate calculation
        thaty_days = today - timedelta(days=30)
        actual = sum(1 for d in check_in_dates if d >= thaty_days)
        days_active = (today - habit.created_date.date()).days + 1
        expected = min(30, max(1, days_active))
        completion_rate = f"{round((actual / expected) * 100, 2)}%"
            
        return {
            'habit_name': habit.habit_name,
            'frequency': habit.frequency,
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'completion_rate_30_days': completion_rate
        }
        
    def _calculate_weekly_stats(self, habit, check_in_dates, today):
        current_streak = 0
        longest_streak = 0
        
        check_in_weeks = sorted(list(set(d.isocalendar()[:2] for d in check_in_dates)))
        current_year, current_wk, _ = today.isocalendar()
        this_week = (current_year, current_wk)
        
        # Determine "last week" tracking year transitions correctly via timedelta
        last_week_date = today - timedelta(weeks=1)
        ly, lw, _ = last_week_date.isocalendar()
        prev_week = (ly, lw)
        
        if check_in_weeks:
            # Current streak validation (alive if checked in this week or last week)
            last_checked_week = check_in_weeks[-1]
            if last_checked_week == this_week or last_checked_week == prev_week:
                current_streak = 1
                for i in range(len(check_in_weeks) - 1, 0, -1):
                    # If the difference between consecutive items is exactly 1 week
                    if self._is_consecutive_week(check_in_weeks[i-1], check_in_weeks[i]):
                        current_streak += 1
                    else:
                        break
            # Longest streak evaluation
            temp_streak = 1
            longest_streak = 1
            for i in range(1, len(check_in_weeks)):
                if self._is_consecutive_week(check_in_weeks[i-1], check_in_weeks[i]):
                    temp_streak += 1
                else:
                    longest_streak = max(longest_streak, temp_streak)
                    temp_streak = 1
            longest_streak = max(longest_streak, temp_streak)

        # Completion Rate (Last 4 Weeks / 28 Days)
        four_weeks_ago = today - timedelta(weeks=4)
        actual_weeks_checked = len([w for w in check_in_weeks if w >= four_weeks_ago.isocalendar()[:2]])
        
        # Calculate weeks elapsed since creation
        weeks_since_creation = ((today - habit.created_date.date()).days // 7) + 1
        expected_weeks = min(4, max(1, weeks_since_creation))
        completion_rate = f"{round((actual_weeks_checked / expected_weeks) * 100, 2)}%"

        return {
            'habit_name': habit.habit_name,
            'frequency': habit.frequency,
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'completion_rate_4_weeks': completion_rate
        }

    def _is_consecutive_week(self, week1, week2):
        """Helper to determine if week2 comes immediately after week1."""
        y1, w1 = week1
        y2, w2 = week2
        if y1 == y2 and w2 - w1 == 1:
            return True
        # Handle New Year transition (e.g., Year 2025 W52 to Year 2026 W1)
        if y2 - y1 == 1 and w2 == 1:
            # Verify if w1 was genuinely the last week of that year
            # ISO years have either 52 or 53 weeks
            import datetime
            last_day_of_year = datetime.date(y1, 12, 28) # Dec 28 always falls in the last ISO week
            return w1 == last_day_of_year.isocalendar()[1]
        return False

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
