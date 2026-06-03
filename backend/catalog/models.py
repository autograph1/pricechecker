from django.db import models
from users.models import User
class Product(models.Model):
    url = models.URLField(max_length=1000)
    needed_price = models.IntegerField()
    current_price = models.IntegerField(null=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.url

