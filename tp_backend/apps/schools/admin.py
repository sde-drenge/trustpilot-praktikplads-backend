from django.contrib import admin
from django.db.models import Prefetch
from django.contrib.auth import get_user_model

from .models import School
from user.constants import Roles 

User = get_user_model()

# Register your models here.

class StudentsInline(admin.TabularInline):
    model = User
    fk_name = "school"
    extra = 0
    fields = ("email", "name", "role")
    can_delete = False
    verbose_name = "Student"
    verbose_name_plural = "Students"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role=Roles.STUDENT)


class TeachersInline(admin.TabularInline):
    model = User
    fk_name = "school"
    extra = 0
    fields = ("email", "name", "role")
    can_delete = False
    verbose_name = "Teacher"
    verbose_name_plural = "Teachers"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role=Roles.TEACHER)

# class UserAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "domain", "student_count", "teacher_count", "createdAt")
    search_fields = ("uuid_hex", "name", "domain")
    ordering = ("-createdAt",)
    inlines = [StudentsInline, TeachersInline]
    
    fieldsets = (
        ("General info", {
            "fields": ("uuid_hex", "name", "domain", "isActive", "description"),
        }),
        ("Dates", {
            "fields": ("createdAt", "updatedAt"),
        }),
        ("Counts", {
            "fields": ("student_count", "teacher_count"),
        }),
    )
    
    def uuid_hex(self, obj):
        return obj.uuid.hex
    uuid_hex.short_description = "UUID"

    def student_count(self, obj):
        # uses the reverse relation "users" and filters
        return obj.users.filter(role=Roles.STUDENT).count()

    def teacher_count(self, obj):
        return obj.users.filter(role=Roles.TEACHER).count()

    # Optional: speed up counts when listing many schools
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related(
            Prefetch("users", queryset=User.objects.only("id", "role"))
        )

    


    readonly_fields = ("uuid_hex", "student_count", "teacher_count", "createdAt", "updatedAt")
    
    def uuid_hex(self, obj):
        return obj.uuid.hex

admin.site.register(School, SchoolAdmin)