from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import useractivity,facedata

# Create your views here.
def home(request):
	# unlocker = unlocker.objects
	return render(request,'unlocker/home.html')

@login_required
def panel(request):
	# unlocker = unlocker.objects
	if request.method == 'POST':
		new_act = useractivity.objects.create(user=request.user,activity='checkin')

	userdata = get_object_or_404(facedata,owner=request.user)
	userdetails = get_object_or_404(User,username=request.user)
	checkins = useractivity.objects.all().filter(user=request.user).order_by("-timestamp")
	return render(request,'unlocker/panel.html',{'list':checkins, 'userdata':userdata, 'userdetails':userdetails})


# def activity_view(request):
# 	if request.method == 'POST':
# 		new_act = useractivity.objects.create(user=request.user,activity='checkin')
# 	return render(request,'unlocker/panel.html',{})

# class UsersActivityView(View):
#     @method_decorator(staff_member_required)
#     def dispatch(self, *args, **kwargs):
#         return super(UsersActivityView, self).dispatch(*args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         query = request.GET.get("q")
#         users = User.objects.all()
#         checked_in_list = []
#         checked_out_list = []
#         no_activity_today_users = []
#         all_activity = UserActivity.objects.all()
#         for u in users:
#             act = all_activity.filter(user=u).today().recent()
#             # act = u.useractivity_set.all().today()
#             if act.exists():
#                 current_user_activity_obj = act.first()
#                 if current_user_activity_obj.activity == 'checkin':
#                     checked_in_list.append(current_user_activity_obj.id)
#                 else:
#                     checked_out_list.append(current_user_activity_obj.id)
#             else:
#                 no_activity_today_users.append(u)
        
#         #all_activity = UserActivity.objects.all().today().recent()
#         checked_in_users = all_activity.filter(id__in=checked_in_list)
#         checked_out_users = all_activity.filter(id__in=checked_out_list)
#         all_activity = all_activity.today().recent()

#         if query:
#             checked_in_users = checked_in_users.filter(user__username__iexact=query)
#             checked_out_users = checked_out_users.filter(user__username__iexact=query)
#             all_activity = all_activity.filter(
#                     Q(user__username__iexact=query) |
#                     Q(user__first_name__iexact=query)
#                     )
#         context = {
#             "checked_in_users": checked_in_users,
#             "checked_out_users": checked_out_users,
#             "inactive_users": no_activity_today_users,
#             "all_activity": all_activity,
#             "query": query,
#         }
#         return render(request, "timeclock/users-activity-view.html", context)
