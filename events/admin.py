from django.contrib import admin
from events.models import Place, Event, Attendance

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ('expected_members', )

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('event__name', 'member', 'attendance', 'proxy_to', 'accepted',)
    list_filter = ('event__name',)

    def event__name(self, obj):
        return str(obj.event)

admin.site.register(Place)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Event, EventAdmin)
