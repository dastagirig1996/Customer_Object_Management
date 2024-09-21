from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, unique=True)


class Refresh_Token(models.Model):
    name = models.CharField(max_length=500)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

# class BaseAbstarctModel(models.Model):
#      name = models.CharField(max_length=250, unique=True)
#      class Meta:
#          abstract = True

# class Role(BaseAbstarctModel):
#     pass

# class Api(BaseAbstarctModel):

#     role = models.ForeignKey(Role, on_delete=models.PROTECT, default=1)
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
    
     

# class Permissions(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.PROTECT) # admin, farmer, customer
#     api = models.ForeignKey(Api, on_delete=models.PROTECT) # 
#     has_get = models.BooleanField(default=False)
#     has_post = models.BooleanField(default=False)
#     has_put = models.BooleanField(default=False)
#     has_delete = models.BooleanField(default=False)