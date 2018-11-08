from django.contrib import admin

# Register your models here.
from .models import useractivity
from .models import facedata
class UserActivityAdmin(admin.ModelAdmin):
	list_display = ['user', 'activity', 'timestamp']
	list_filter = ['timestamp']
	class Meta:
		model=useractivity
			
		

admin.site.register(useractivity,UserActivityAdmin)
admin.site.register(facedata)