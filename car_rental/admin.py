from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Car)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Reservation)
admin.site.register(Worker)
admin.site.register(Notification)
admin.site.register(UserActionLog)



