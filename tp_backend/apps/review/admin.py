from django.contrib import admin

from .models import Review

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "rating", "isApproved", "createdAt")
    search_fields = ("uuid_hex", "title", "student__email", "student__name")
    ordering = ("-createdAt",)
    
    fieldsets = (
        ("General info", {
            "fields": ("uuid_hex", "title", "student", "content", "rating", "isApproved"),
        }),
        ("Dates", {
            "fields": ("createdAt", "updatedAt"),
        }),
    )
    
     
    readonly_fields = ("uuid_hex", "student", "createdAt", "updatedAt")
    
    def uuid_hex(self, obj):
        return obj.uuid.hex
    uuid_hex.short_description = "UUID"


admin.site.register(Review, ReviewAdmin)