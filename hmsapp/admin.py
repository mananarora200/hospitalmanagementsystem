from django.contrib import admin
from.models import UserProfile, UserHistory,Medic,Labs,Visits,Case
# Register your models here
admin.site.register(UserProfile)
admin.site.register(UserHistory)
admin.site.register(Medic)
admin.site.register(Labs)
admin.site.register(Case)
admin.site.register(Visits)