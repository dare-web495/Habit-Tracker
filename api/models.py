from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=50)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name='habit')
    
    def __str__(self):
        return f"{self.user.username}'s habit is {self.habit_name} (created at {self.created_date})"
    


class Checkin(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['habit', 'date'],
                name='prevent_double_checkin'
            )
        ]
    
    def __str__(self):
        return f"{self.habit.user.username} checked in at {self.date}"
    