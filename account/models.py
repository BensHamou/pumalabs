from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Horaire(models.Model):
    hour_start = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(23)])
    minutes_start = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    hour_end = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(23)])
    minutes_end = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])    
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    @property
    def passed_time(self):
        total_start = self.hour_start + self.minutes_start / 60 
        total_end = self.hour_end + self.minutes_end / 60 
        total = total_end - total_start
        if total < 0:
            total += + 24
        return round(total, 2)

    def __str__(self):
        name = str(self.hour_start) + 'H'
        if self.minutes_start > 0:
            name += str(self.minutes_start) + 'M' 
        name += '-' + str(self.hour_end) + 'H'
        if self.minutes_end > 0:
            name += str(self.minutes_end) + 'M'
        return name
    
class Usine(models.Model):
    designation = models.CharField(max_length=100)
    horaires = models.ManyToManyField(Horaire, blank=True)
    address = models.CharField(max_length=250, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.designation
    
class Setting(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=250)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name + ' : ' + self.value

class User(AbstractUser):

    ROLE_CHOICES = [
        ('Nouveau', 'Nouveau'),
        ('Technicien', 'Technicien'),
        ('Validateur', 'Validateur'),
        ('Observateur', 'Observateur'),
        ('Gestionnaire de production', 'Gestionnaire de production'),
        ('Admin', 'Admin'),
    ]

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    role = models.CharField(choices=ROLE_CHOICES, max_length=30)
    usines = models.ManyToManyField(Usine, blank=True)
    is_admin = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    fields = ('username', 'fullname', 'email', 'role', 'usines', 'is_admin', 'first_name', 'last_name')

    
    def __str__(self):
        return self.fullname

    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'