from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from djangoql.admin import DjangoQLSearchMixin

from .models import User

# Register your models here.


# class UserAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
class UserAdmin(DjangoQLSearchMixin, BaseUserAdmin):
    search_fields = [
        "email",
        "uuid_hex",
        "name",
    ]
    list_display = (
        "email",
        "name",
        "createdAt",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "isActive",
                    "is_staff",
                    "is_superuser",
                    "uuid_hex",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Additional info"),
            {
                "fields": (
                    "verificationEmailSentAt",
                    "verificationCode",
                    "role",
                )
            },
        ),
    )

    ordering = ("-createdAt",)

    readonly_fields = [
        "password",
        "uuid_hex",
        "createdAt",
        "updatedAt",
        "deletedAt",
    ]

    def uuid_hex(self, obj):
        return obj.uuid.hex


admin.site.register(User, UserAdmin)