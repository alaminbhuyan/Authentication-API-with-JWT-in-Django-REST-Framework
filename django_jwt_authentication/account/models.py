from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Custom user manager class
class MyUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, terms_and_condition, password=None, password2=None):
        """
        Creates and saves a User with the given username, first_name, last_name, email, terms_and_condition and password.

        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            terms_and_condition=terms_and_condition,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, terms_and_condition, password=None):
        """
        Creates and saves a superuser with the given username, first_name, last_name, email, terms_and_condition and password.

        """
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            terms_and_condition=terms_and_condition,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(verbose_name="username", max_length=200)
    first_name = models.CharField(verbose_name="firstname", max_length=200)
    last_name = models.CharField(verbose_name="lastname", max_length=200)
    terms_and_condition = models.BooleanField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    # It will be take when you will create a new superuser or user
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "terms_and_condition"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
