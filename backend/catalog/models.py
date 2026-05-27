from django.db import models
from users.models import User
class Product(models.Model):
    url = models.CharField(max_length=100)
    needed_price = models.IntegerField()
    current_price = models.IntegerField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.url

