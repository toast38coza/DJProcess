from django.contrib import admin
from .models import Process, Task

class TaskInline(admin.StackedInline):
    """AddressInline"""
    model = Task

class ProcessAdmin(admin.ModelAdmin):
    list_display = ('process_id', 'status')
    inlines = (TaskInline,)

admin.site.register(Process, ProcessAdmin)
admin.site.register(Task)


