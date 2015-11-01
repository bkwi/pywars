from django.db import models
from django.conf import settings

import uuid

from django.contrib.auth.models import (
        BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from main.utils import _gen_id, send_email, logger

class AppUserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        """
        Creates and saves user
        """

        if not email:
            raise ValueError("User must have an email address")

        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email = self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser
        """
        user = self.create_user(email, name=name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):

    id = models.CharField(primary_key=True, default=_gen_id, max_length=16)

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        db_index=True
    )
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField(default=0)
    password_reset_token = models.CharField(default=None, max_length=32,
                                            null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = AppUserManager()

    def get_full_name(self):
        return "%s, name: %s" % (self.email, self.name)

    def get_short_name(self):
        return self.email

    def avatar_url(self):
        return "https://robohash.org/{}.png".format(self.name)

    def __unicode__(self):
        return 'User {} ({})'.format(self.id, self.email)

    def already_solved_challenge(self, challenge):
        for s in self.solutions.all():
            if s.challenge_id == challenge.id:
                return True
        return False

    def send_password_reset_email(self):
        self.password_reset_token = uuid.uuid4().hex
        self.save()
        logger.info('%s requested password reset link. Token: %s...',
                    self, self.password_reset_token[:10])
        reset_link = "{}/user/reset-password/{}/{}".format(
                     settings.APP_HOST, self.id, self.password_reset_token)
        send_email(email_address=self.email,
                   body="Click here to reset your password: %s" % reset_link,
                   subject="[PyWars] Password Reset Link")


