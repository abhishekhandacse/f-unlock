from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class facedata(models.Model):
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	image = models.ImageField(upload_to='images/')
	time_posted = models.DateTimeField(auto_now_add=True)
	audio = models.FileField(upload_to='audios/',null=True)
	def __str__(self):
		return str(self.owner)


class useractivity(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	activity = models.CharField(max_length=120, default="Checkin")
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.activity)

	class Meta:
		verbose_name='User Activity'
		verbose_name_plural = "User Activities"
		