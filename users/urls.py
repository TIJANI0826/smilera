from django.urls import path,include
from .views import GymUserSignUpView, GymProfileUpdateView, home,GymUserSignUpAPIView,ProfileView
app_name = 'users'
urlpatterns = [
    path('signup', GymUserSignUpView.as_view(),name="gym-user-signup"),
    path('profile-update', GymProfileUpdateView.as_view(),name="gym-user-profile"),
    path('dashbord', ProfileView.as_view(), name='profile')
]
