from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=True, is_parent=False, is_school=False, is_vendor=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) # change user password
        user_obj.parent = is_parent
        user_obj.school = is_school
        user_obj.vendor = is_vendor
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_parentuser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_parent=True
        )
        return user

    def create_schooluser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_school=True
        )
        return user

    def create_vendoruser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_vendor=True
        )
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_staff=True,
                is_admin=True,
        )
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    active      = models.BooleanField(default=True) # can login 
    parent       = models.BooleanField(default=False) # parent user
    school       = models.BooleanField(default=False) # school admin user
    vendor       = models.BooleanField(default=False) # vendor user  
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser 
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email' #username

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_parent(self):
        return self.parent

    @property
    def is_school(self):
        return self.school
        
    @property
    def is_vendor(self):
        return self.vendor

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin