from django.contrib import admin
from django import forms

from kites import models


class Upper(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data["name"].upper()
    

class UpperUnder(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data["name"].upper().replace(' ', '_')


class KiteAdmin(admin.ModelAdmin):
    form = UpperUnder
    list_display = ['id', 'brand', 'name', 'time_update', 'is_published', 'expert']
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'expert')
    fields = ['brand', 'name', 'text', 'is_published', 'expert', 'photo1']


class BrandAdmin(admin.ModelAdmin):
    form = Upper
    list_display = ['id', 'name', 'slug']
    fields = ['name']
    # prepopulated_fields = {'slug': ('name', )}


# class ExpertAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name', )}


admin.site.register(models.Kite, KiteAdmin)
admin.site.register(models.Brand, BrandAdmin)
# admin.site.register(models.Expert, ExpertAdmin)
