from django.contrib import admin
from derby.models import Place, Player, Training, TrainingPart, TrainingPartType

# Register your models here.
admin.site.register(Place)
admin.site.register(Player)
admin.site.register(TrainingPartType)
admin.site.register(TrainingPart)

class TrainingPartInline(admin.TabularInline):
    model = TrainingPart
    extra = 1

class TrainingAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None, {'fields': ['name', 'slug', 'text']}),
#        ('Members', {'fields': ['can_vote', 'group_can_vote']}),
#        ('Dates', {'fields': ['pub_date', 'end_date']}),
#    ]
#    filter_horizontal = ('can_vote', 'group_can_vote')
    inlines = [TrainingPartInline]
#    list_display = ('name', 'pub_date', 'end_date', 'get_vote_status',)
#    list_filter = ['pub_date']

admin.site.register(Training, TrainingAdmin)
