from django.contrib import admin
from events.models import Place, Event, Attendance

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ('expected_members', )

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'attendance', 'proxy_to', 'accepted',)
    

admin.site.register(Place)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Event, EventAdmin)
