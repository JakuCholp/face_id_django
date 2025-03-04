from django.contrib import admin

from .models import People, Visits

admin.site.register(People)





@admin.register(Visits)
class VisitsAdmin(admin.ModelAdmin):
    list_display = ('people', 'visiting_time', 'countOFvisits')  
    readonly_fields = ('visiting_time',) 
