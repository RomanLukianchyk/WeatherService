from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_user_added = models.BooleanField(default=False)

    def __str__(self):
        return self.name
