from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'habit', views.HabitViewSet, basename='habit')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'checkin', views.CheckinViewset, basename='checkin')

urlpatterns = [
    path('', include(router.urls))
]
