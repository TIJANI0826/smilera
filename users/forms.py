from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
#from lxml.html.clean import clean_html
from django.utils.html import escape, mark_safe

from .models import User,GymUser
GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female')
)

# class UserSignUpForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'phone_number','location',)


class GymUserForm(UserCreationForm):
    # gender = forms.ChoiceField(
    #     queryset=GENDER_TYPES,
    #     widget=forms.RadioSelect,
    #     required=True
    # )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2',  )

        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_gym_user = True
        user.save()
        gym_user = GymUser.objects.create(user=user,username=user.username)
        return user

class GymUserProfileForm(forms.ModelForm):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # username = models.CharField(max_length=10,unique=False, null=True, blank=True)
    # img = models.ImageField(null=True, blank=True, upload_to='media/')
    # email = models.EmailField(unique=True)
    # phone_number = models.CharField(max_length=50, null=True)
    # show_name = models.CharField(max_length=30, null=True, blank=True)
    # gender = models.CharField(max_length=2, choices=GENDER_TYPES, null=True, blank=True)
    # location = models.CharField(max_length=100, null=True, blank=True)
    # is_company = models.BooleanField(default=False)
    # company_name = models.CharField(max_length=50, null=True, blank=True)
    # company_address = models.CharField(max_length=50, null=True, blank=True)
    # is_blocked = models.BooleanField(default=False)
    # is_gold = models.BooleanField(default=False)
    # # favorite_products = models.ManyToManyField(Product)
    # # following = models.ManyToManyField('User', related_name='followers')
    # pass_code = models.IntegerField(default=0)
    # is_verified = models.BooleanField(default=False)
    # global_visa = models.CharField(max_length=50, null=True, blank=True)
    # local_visa = models.CharField(max_length=50, null=True, blank=True)
    # bank_name = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        model = GymUser
        fields = ('img', 'phone_number', 'show_name', 'gender',  )
    
    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user. = True
    #     user.save()
    #     gym_user = GymUser.objects.create(user=user)
    #     return user
