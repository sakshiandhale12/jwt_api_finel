from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    def create_user(self, email, Name, tc, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not Name:
            raise ValueError("Users must have a name")
        if not tc:
            raise ValueError("Users must have a tc")

        try:
            # Check if a user with the given tc already exists
            existing_user = self.model.objects.get(tc=tc)
            raise ValueError("A user with this tc already exists")
        except self.model.DoesNotExist:
            pass  # Continue creating the user if no existing user with the same tc is found

        user = self.model(
            email=self.normalize_email(email),
            Name=Name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, Name, tc, password=None):
        user = self.create_user(
            email,
            Name=Name,
            tc=tc,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )

    Name = models.CharField(max_length=200)
    tc = models.CharField(max_length=11, unique=True)  # Update the field type to CharField
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Name', 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

