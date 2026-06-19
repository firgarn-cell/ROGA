from django.contrib import admin
from .models import CustomUser, Application, Review

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transport_type', 'start_date', 'status', 'created_at')
    list_filter = ('status', 'transport_type')
    search_fields = ('user__username', 'user__fio') 
    list_editable = ('status',) 
    list_per_page = 10 

admin.site.register(CustomUser)
admin.site.register(Review)