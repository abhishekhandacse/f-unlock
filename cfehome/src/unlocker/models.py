from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from io import BytesIO
import os.path
from django.core.files.base import ContentFile
THUMB_SIZE = (400,400)
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
		
class OneTimeRequest(models.Model):
	image = models.ImageField(upload_to='')
	request_time = models.DateTimeField(auto_now_add=True)
	thumbnail = models.ImageField(upload_to='thumbs/',editable=False, blank=True)
	access = models.BooleanField(default=False)
	def save(self, *args, **kwargs):
		if not self.make_thumbnail():
			raise Exception("Could not create thumbnail! Check the file type")
		super(OneTimeRequest,self).save(*args,**kwargs)
	def make_thumbnail(self):
		photo = Image.open(self.image)
		photo.thumbnail(THUMB_SIZE,Image.ANTIALIAS)
		thumb_name, thumb_extension = os.path.splitext(self.image.name)
		thumb_extension = thumb_extension.lower()
		thumb_filename = thumb_name + '_thumb' + thumb_extension
		if thumb_extension in ['.jpg', '.jpeg']:
			FTYPE = 'JPEG'
		elif thumb_extension == '.gif':
			FTYPE = 'GIF'
		elif thumb_extension == '.png':
			FTYPE = 'PNG'
		else:
			return False

		temp_thumb = BytesIO()
		photo.save(temp_thumb,FTYPE)
		temp_thumb.seek(0)

		self.thumbnail.save(thumb_filename,ContentFile(temp_thumb.read()),save=False)
		temp_thumb.close()
		return True