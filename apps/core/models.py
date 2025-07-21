from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):

    user_role = models.CharField(max_length=10, default='customer', choices=(

                ('admin', 'admin'),
                ('customer', 'customer'),

            )
    )

    def __str__(self):
        return self.username
