from django.contrib import admin

from .models import Company

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "vat_number", "createdAt")
    search_fields = ("uuid_hex", "name", "vat_number")
    ordering = ("-createdAt",)
    
    fieldsets = (
        ("General info", {
            "fields": ("uuid_hex", "name", "description", "address", "website", "vat_number"),
        }),
        ("Dates", {
            "fields": ("createdAt", "updatedAt"),
        }),
    )


    readonly_fields = ("uuid_hex", "createdAt", "updatedAt")

    def uuid_hex(self, obj):
        return obj.uuid.hex
    uuid_hex.short_description = "UUID"

admin.site.register(Company, CompanyAdmin)