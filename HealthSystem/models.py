from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, password, **other_fields)

    def create_user(self, username, password, **other_fields):

        if not username:
            raise ValueError(_('You must provide a username'))

        user = self.model(username=username, password=password,**other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class UserStatus(models.TextChoices):
        DOCTOR = 'DR', _('Doctor')
        PATIENT = 'PR', _('Patient')

    userStatus = models.CharField(
        max_length=2,
        choices=UserStatus.choices,
        default=UserStatus.PATIENT,
    )

    username= models.CharField(max_length=200, unique=True)
    firstname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)
    token = models.TextField(blank=True)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Appointment(models.Model):

    class AppointmentStatus(models.TextChoices):
        ACCEPT = 'ACT', _('ACCEPT')
        REJECT = 'RJT', _('REJECT')

    Status = models.CharField(
        max_length=3,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.REJECT,
    )
    
    patientId = models.IntegerField()
    diagnosis = models.TextField(null=True, blank=True)
    doctorId = models.IntegerField()
    date = models.DateTimeField()

class Comment(models.Model):
    comment = models.TextField(null=True, blank=True)
    userId = models.IntegerField(null=True, blank=True)
    doctorId = models.IntegerField(null=True, blank=True)
    # user = models.CharField(max_length=200, blank=True, null=True)

class Vitals(models.Model):
    pass