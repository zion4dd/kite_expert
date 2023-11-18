from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe

from kites import models
from kites import forms


@admin.register(models.Kite)
class KiteAdmin(admin.ModelAdmin):
    form = forms.KiteForm
    list_display = ('id', 'brand', 'name', 'slug', 'time_update', 'is_published', 'expert', 'photos')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'expert')
    fields = ('brand', 'name', 'text', 'is_published', 'expert', 'photo1', 'photo2', 'photo3', 'photo4')
    ordering = ( 'brand', 'name')
    list_per_page = 10
    readonly_fields = ('photos', )
    save_on_top = True
    # exclude

    @admin.display(description="photos")
    def photos(self, kite):
        ph = ''
        if kite.photo1:
            ph += f"<img src='{kite.photo1.url}' width=50>"
        if kite.photo2:
            ph += f"<img src='{kite.photo2.url}' width=50>"
        if kite.photo3:
            ph += f"<img src='{kite.photo3.url}' width=50>"
        if kite.photo4:
            ph += f"<img src='{kite.photo4.url}' width=50>"
        return mark_safe(ph) if ph else 'No photo'


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    form = forms.BrandForm
    list_display = ('id', 'name', 'slug')
    fields = ('name', )
    # prepopulated_fields = {'slug': ('name', )}


admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_display_links = ('id', 'username')
    # list_editable = ('is_active',)


# admin.site.register(models.Kite, KiteAdmin)
# admin.site.register(models.Brand, BrandAdmin)
# admin.site.register(models.Expert, ExpertAdmin)
# admin.site.register(User, CustomUserAdmin)