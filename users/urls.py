from django.urls import path
from .views import GymUserSignUpView, \
GymProfileUpdateView, home,GymUserSignUpAPIView,ProfileView, GymLoginAPIView
app_name = 'users'
urlpatterns = [
    path('signup', GymUserSignUpView.as_view(),name="gym-user-signup"),
    path('profile-update', GymProfileUpdateView.as_view(),name="gym-user-profile"),
    path('dashbord', ProfileView.as_view(), name='profile'),
    path('api-login/', GymLoginAPIView.as_view(), name='api-login'),
    path('api-register/', GymUserSignUpAPIView.as_view(), name='api-signup')
]
