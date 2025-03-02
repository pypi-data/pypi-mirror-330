from django.contrib import admin
from .models import VSServer, VSMod


class VSModsInline(admin.TabularInline):
    model = VSMod

class VSServerAdmin(admin.ModelAdmin):
    readonly_fields = ['last_heartbeat',]
    inlines = [VSModsInline]


admin.site.register(VSServer, VSServerAdmin)
admin.site.register(VSMod)
