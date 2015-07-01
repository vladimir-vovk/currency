from django.contrib import admin
from .models import Currency, Rate


class RateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'value', 'obsolete')

admin.site.register(Currency)
admin.site.register(Rate, RateAdmin)


