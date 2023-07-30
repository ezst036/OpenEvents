from django.contrib import admin
from . models import Event, StripeKeys

@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'price']
    prepopulated_fields = {'slug':('name',)}

@admin.register(StripeKeys)
class StripeKeysAdmin(admin.ModelAdmin):
    readonly_fields = ('apikeys',)
    list_display = ['apikeys', ]