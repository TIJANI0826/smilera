from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

# Create your views here.
import random
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import request
#from lxml.html.clean import clean_html
from django.utils.html import escape, mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.db import transaction
from django.db.models import Count, Sum
from django.db.models.functions import Concat
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView,DetailView
from django.views import View
from django.views.generic.edit import FormView
from .decorators import gym_user_required
from .forms import GymUserForm, GymUserProfileForm
from .models import User, GymUser
# from formtools.wizard.views import SessionWizardView

from django.contrib.auth import authenticate

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser

from .models import User
from .serializers import(
    LoginSerializer,
    SignupSerializer,
    GymUserSignupSerializer,
    UpdateUserSerializer,
    UserDataSerializer
)


from django.views.generic import TemplateView

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class GymUserSignUpView(CreateView):
    model = User
    form_class = GymUserForm
    template_name = 'registration/signup_form.html'


    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Gym User'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:gym-user-profile')

class GymUserSignUpAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GymUserSignupSerializer

    def post(self, request):
        user_serializer = GymUserSignupSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.pass_code = random.randint(1000,9999)
            # asyncio.run(send_single_message(user, 'Verification code %s' %(user.pass_code,)))
            user.save()
            return Response(
                {'data': user_serializer.data},
                status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {'error': user_serializer.errors}
            )



@login_required
def home(request):
    context = {
        "user" : request.user.username
    }
    return render(request, 'home.html')

@method_decorator([login_required, gym_user_required], name='dispatch')
class GymProfileUpdateView(UpdateView):
    model = GymUser
    form_class = GymUserProfileForm
    template_name = 'registration/profile_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user.gymuser

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated with success!')
        return super().form_valid(form)

class ProfileView(DetailView):
    """
    View for profile page
    """
    model = GymUser
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        """
        Fetching user profile for viewing
        """
        obj = GymUser.objects.get(username=self.request.user.username)
        return obj

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class GymLoginAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):

        username = User.objects.filter(email=request.data['email']).first()
        if not username:
            username = User.objects.filter(email=request.data['email']).first()

            if not username:
                return Response(
                    {'error': 'your email or phone number is not exist in our database'},
                    status=status.HTTP_404_NOT_FOUND
                )

        user = authenticate(request, username=username.email, password=request.data['password'])
        if user:
            if user.is_verified:
                user_serialzer = LoginSerializer(data=request.data)
                if user_serialzer.is_valid():
                    user_token, _ = Token.objects.get_or_create(user=user)
                    serializer = UserDataSerializer(user)
                    return Response(
                        {
                            "token": user_token.key,
                            "user": serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': user_serialzer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': "user is not verified"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'make sure about your email and your password please'},
                status=status.HTTP_404_NOT_FOUND
            )




# from reviews.serializers import ReviewSerializer
# from products.serializers import ProductSerializer
# from dashboard.serializers import DashboardUpdateRateProductSerializer
# import random
# import asyncio
# from utils import send_single_message

# class LoginAPIView(GenericAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = LoginSerializer

#     def post(self, request):

#         username = User.objects.filter(phone_number=request.data['email']).first()
#         if not username:
#             username = User.objects.filter(email=request.data['email']).first()

#             if not username:
#                 return Response(
#                     {'error': 'your email or phone number is not exist in our database'},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#         user = authenticate(request, username=username.email, password=request.data['password'])
#         if user:
#             if user.is_verified:
#                 user_serialzer = LoginSerializer(data=request.data)
#                 if user_serialzer.is_valid():
#                     user_token, _ = Token.objects.get_or_create(user=user)
#                     serializer = UserDataSerializer(user)
#                     return Response(
#                         {
#                             "token": user_token.key,
#                             "user": serializer.data
#                         },
#                         status=status.HTTP_200_OK
#                     )
#                 else:
#                     return Response(
#                         {'error': user_serialzer.errors},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#             else:
#                 return Response(
#                     {'error': "user is not verified"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         else:
#             return Response(
#                 {'error': 'make sure about your email and your password please'},
#                 status=status.HTTP_404_NOT_FOUND
#             )


# class SignupAPIView(GenericAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = SignupSerializer

#     def post(self, request):
#         user_serializer = SignupSerializer(data=request.data)
#         if user_serializer.is_valid():
#             user = user_serializer.save()
#             user.pass_code = random.randint(1000,9999)
#             asyncio.run(send_single_message(user, 'Verification code %s' %(user.pass_code,)))
#             user.save()
#             return Response(
#                 {'data': user_serializer.data},
#                 status=status.HTTP_201_CREATED
#                 )
#         else:
#             return Response(
#                 {'error': user_serializer.errors}
#             )

# class Verification(APIView):
#     '''
#         verification user
#         params:
#             - code : pass code
#             - phone_number: user phone number
#     '''
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):

#         if not request.data.get('code') and not request.data.get('phone_number'):
#             return Response(
#                 {'error': 'please add your pass code and phone number'}
#             )
#         try:
#             pass_code = int(request.data.get('code'))
#             phone_number = str(request.data.get('phone_number'))
#         except:
#             return Response(
#                 {'error': 'please enter valid code'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             get_user = User.objects.get(pass_code=pass_code, phone_number=phone_number)
#             get_user.is_verified = True
#             get_user.pass_code = 0
#             get_user.save()
#             return Response(
#                 {'data': 'user verified'},
#                 status=status.HTTP_200_OK
#             )
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'you have entered wrong pass code'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
