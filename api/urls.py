from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
)
from . import views

router = DefaultRouter()

router.register(r'habit', views.HabitViewSet, basename='habit')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'checkin', views.CheckinViewset, basename='checkin')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterUserView.as_view(), name='register')
]
