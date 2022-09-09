import jwt

from datetime import datetime, timedelta

from asyncio import AbstractServer
from operator import mod
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, AbstractUser,  BaseUserManager, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
# Create your models here.


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.birth_day = datetime.now()
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    # All these field declarations are copied as-is
    # from `AbstractUser`
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )

    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    contact = models.CharField(max_length=15, blank=False, null=False)
    # country_code = models.CharField(max_length=14, default='+91')
    birth_day = models.DateTimeField(default=datetime.now)
    user_type = models.CharField(choices=(('M', 'Mother'), ('C', 'Child'), 
                                          ('A', 'Admin'), ('D', 'Doctor')), max_length=1, default='A')
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = None

    USERNAME_FIELD = 'email'


    objects = UserManager()

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Appointment(models.Model):
    appointment_of = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                       related_name='patient_appointment')
    appointment_date = models.DateTimeField()
    doctor_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                    related_name='doctor_appointment')
    description = models.TextField()

    def __str__(self):
        return "{} app. with {}".format(self.appointment_of.first_name,
                                        self.appointment_of.last_name)


vaccine_names = [
    ('BCG', 'BCG'),
    ('HIB', 'HIB'),
    ('Hep-B', 'Hep-B'),
    ('MMR', 'MMR'),
    ('DPT', 'DPT'),
    ('Polio', 'Polio'),
]


class Vaccine(models.Model):
    vaccine_name = models.CharField(choices=vaccine_names, max_length=512)
    total_doses = models.IntegerField(default=1)
    age_given = models.CharField(max_length=100)  ## example 3,6,7
    description = models.TextField()

    def __str__(self):
        return self.vaccine_name


class VaccineStatus(models.Model):
    vaccine_name = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    dosage_count = models.IntegerField(default=1)
    status = models.CharField(max_length=15, 
                              choices=(('Pending', 'Pending'), ('Completed', 'Completed')), default='Pending')
    due_date = models.DateTimeField()
    applied_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.vaccine_name.vaccine_name

