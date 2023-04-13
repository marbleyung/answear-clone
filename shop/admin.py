from django.contrib import admin
from django.contrib.admin import StackedInline

from .models import *


class PictureInline(StackedInline):
    model = Item.pictures.through
    ordering = ("pk", )


class ItemAdmin(admin.ModelAdmin):
    model = Item
    exclude = ('item_type', )
    list_display = ("name", 'price', 'item_material', 'item_brand', "item_category", "item_type", 'item_gender')
    list_filter = ("name", 'price', 'item_material', 'item_brand', "item_category", "item_type", 'item_gender')
    search_fields = ("name", 'item_material', 'item_brand', "item_category", "item_type", 'item_gender')
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("name", ), }
    inlines = [PictureInline, ]
    readonly_fields = ('final_price', 'quantity')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "pictures":
            kwargs["queryset"] = ItemPicture.objects.order_by('-id')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class ItemGenderAdmin(admin.ModelAdmin):
    list_display = ("gender",)
    prepopulated_fields = {"slug": ("gender",)}  # new


class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ("type",)
    prepopulated_fields = {"slug": ("type",)}  # new


class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ("category",)
    prepopulated_fields = {"slug": ("category",)}  # new


class ItemSizeAdmin(admin.ModelAdmin):
    list_display = ("size",)
    prepopulated_fields = {"slug": ("size",)}  # new


class ItemStockAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "item":
            kwargs["queryset"] = Item.objects.order_by('-id')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ItemPicture, )
admin.site.register(ItemGender, ItemGenderAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(ItemSize, ItemSizeAdmin)
admin.site.register(ItemBrandSegment)
admin.site.register(ItemBrand)
admin.site.register(ItemMaterial)
admin.site.register(ItemColor)
admin.site.register(ItemSeason)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemStock, ItemStockAdmin)
admin.site.register(ItemInCart)
