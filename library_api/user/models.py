from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model

from library.models import Library




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    libraries = models.ManyToManyField(Library, through='UserLibraryRelation', related_name='users')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    REQUIRED_FIELDS = []

    def is_library_admin(self, library):
        try:
            relation = self.library_relations.get(library=library)
            return relation.is_admin
        except UserLibraryRelation.DoesNotExist:
            return False

    def __str__(self):
        return self.email


User = get_user_model()


class UserLibraryRelation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='library_relations')
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='user_relations')
    is_admin = models.BooleanField(default=False)
    max_num_books = models.IntegerField(default=5)

    class Meta:
        unique_together = ('user', 'library')

    def __str__(self):
        return f"{self.user.email} - {self.library.name}"