from django.urls import path, include
from rest_framework.router import DefaultRouter
from . import views

router = DefaultRouter()

router.regiser(r'habit', views.HabitViewSet, basename='habit')
router.regiser(r'category', views.CategoryViewSet, basename='category')
router.regiser(r'checkin', views.CheckinViewset, basename='checkin')

urlpatterns = [
    path('', include(router.urls))
]
