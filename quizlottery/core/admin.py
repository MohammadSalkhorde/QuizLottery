from django.contrib import admin
from .models import Comments, Timer, Org


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """
    Admin panel for managing user comments.
    پیام‌های سیستم فارسی هستند.
    """
    list_display = ("id", "user", "text", "is_active", "register_date")
    list_filter = ("is_active", "register_date")
    search_fields = ("user__mobile_number", "user__name", "text")
    list_editable = ("is_active",)
    ordering = ("-register_date",)
    date_hierarchy = "register_date"


@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    """
    Admin panel for managing timers.
    پیام‌های سیستم فارسی هستند.
    """
    list_display = ("id", "title", "start_time", "end_time", "is_active")
    list_filter = ("is_active", "start_time", "end_time")
    search_fields = ("title",)
    list_editable = ("is_active",)
    ordering = ("-start_time",)
    date_hierarchy = "start_time"


@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    """
    Admin panel for managing organizations.
    پیام‌های سیستم فارسی هستند.
    """
    list_display = (
        "id",
        "title",
        "phone",
        "link",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("title", "phone", "address")
    list_editable = ("is_active",)
    ordering = ("-id",)
