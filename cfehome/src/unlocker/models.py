from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class unlock(models.Model):
	input_date = models.DateTimeField()
	image = models.ImageField(upload_to='images/')
	owner = models.ForeignKey(User,on_delete=models.CASCADE)

	def input_date_pretty(self):
		return self.input_date.strftime('%b %e, %Y')

	def __str__(self):
		return self.title