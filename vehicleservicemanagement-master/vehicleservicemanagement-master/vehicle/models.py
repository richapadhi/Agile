from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class Mechanic(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/MechanicProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    skill = models.CharField(max_length=500,null=True)
    salary=models.PositiveIntegerField(null=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Request(models.Model):
    projectInformation = models.CharField(max_length=255, null=True)  # Assuming a character limit
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    workLocation = models.CharField(max_length=255, null=True)
    positionDomain = models.CharField(max_length=255, null=True)
    positionRole = models.CharField(max_length=255, null=True)
    EXPERIENCE_LEVEL_CHOICES = [
        ('Entry Level', 'Entry Level'),
        ('Mid Level', 'Mid Level'),
        ('Senior Level', 'Senior Level'),
    ]
    experienceLevel = models.CharField(
        max_length=50,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='Entry Level',
        null = True
    )
    technology = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.projectInformation

class Feedback(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=40)
    message=models.CharField(max_length=500)
