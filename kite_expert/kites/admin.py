from django.contrib import admin

from kites import models
from kites import forms


class KiteAdmin(admin.ModelAdmin):
    form = forms.KiteForm
    list_display = ['id', 'brand', 'name', 'slug', 'time_update', 'is_published', 'expert']
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'expert')
    fields = ['brand', 'name', 'text', 'is_published', 'expert', 'photo1', 'photo2', 'photo3', 'photo4']


class BrandAdmin(admin.ModelAdmin):
    form = forms.BrandForm
    list_display = ['id', 'name', 'slug']
    fields = ['name']
    # prepopulated_fields = {'slug': ('name', )}


admin.site.register(models.Kite, KiteAdmin)
admin.site.register(models.Brand, BrandAdmin)
# admin.site.register(models.Expert, ExpertAdmin)
