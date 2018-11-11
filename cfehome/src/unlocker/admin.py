from django.contrib import admin

# Register your models here.
from .models import useractivity
from .models import facedata
from .models import OneTimeRequest
class UserActivityAdmin(admin.ModelAdmin):
	list_display = ['user', 'activity', 'timestamp']
	list_filter = ['timestamp']
	class Meta:
		model=useractivity

class RequestAdmin(admin.ModelAdmin):
	list_display = ['id','thumbnail','image','request_time']
	list_filter = ['request_time']
	class Meta:
		model=OneTimeRequest

admin.site.register(useractivity,UserActivityAdmin)
admin.site.register(facedata)
admin.site.register(OneTimeRequest,RequestAdmin)