from django.contrib import admin
from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'url', 'named_url', 'order')
    list_filter = ('menu',)
    search_fields = ('title', 'url', 'named_url')
    list_editable = ('order',)
    raw_id_fields = ('parent',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Фильтруем родительские элементы по текущему меню"""
        if db_field.name == "parent":
            if request.GET.get('menu__id__exact'):
                kwargs["queryset"] = MenuItem.objects.filter(
                    menu_id=request.GET.get('menu__id__exact')
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)