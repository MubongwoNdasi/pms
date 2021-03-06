from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from allauth.account.models import EmailAddress
from django.urls import reverse

# from drug.models import Drug, Category
# from core.permissions.permissions import ROLE_LIST, role as user_role


# Create your models here.
from pms import settings


class City(models.Model):
    name = models.CharField(
        max_length=50)

    created_on = models.DateTimeField(_('added on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Pharmacy(models.Model):
    name = models.CharField(
        max_length=100, help_text="Enter the name of your pharmacy")
    location = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone = PhoneNumberField(_('phone number'), blank=True, help_text=_(
        'Number must be in format: +237654686473'))

    created_on = models.DateTimeField(_('added on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    class Meta:
        verbose_name_plural = 'Pharmacies'

    def get_absolute_url(self):
        return reverse('drug:list')

    def __str__(self):
        return self.name


class UserQueryset(models.query.QuerySet):

    def search_pharmacist(self, query):
        instances = self.filter()
        lookups = Q(email__icontains=query) | Q(first_name__icontains=query) | Q(
            last_name__icontains=query)
        return self.filter(lookups).distinct()


class UserManager(models.Manager):
    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    def search_pharmacist(self, query):
        return self.get_queryset().all().search_pharmacist(query)


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)

    # username = None
    email = models.EmailField(
        unique=True, verbose_name='Email', help_text='Enter email')
    address = models.CharField(max_length=100, help_text='Enter your area of residence', verbose_name='Address',
                               blank=True, null=True)
    phone = PhoneNumberField(_('phone number'), blank=True, help_text=_(
        'Number must be in international format.'), null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    @property
    def email_addresses(self):
        return EmailAddress.objects.filter(user__pk=self.pk)

    @property
    def is_verified(self):
        return EmailAddress.objects.filter(verified=True).exists()


class PharmacyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    works_at = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    created_on = models.DateTimeField(_('added on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    # class Meta:
    #     unique_together = (('user', 'works_at'),)

    # def __str__(self):
    #     return f'{self.user.email} | {self.works_at.name} in {self.city.name}'

    def __str__(self):
        return self.user.email


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name='profile')
    image = models.ImageField(upload_to='profile/',
                              default='profile/default_profile.jpg')

    created_on = models.DateTimeField(_('added on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __str__(self):
        return self.user.email
