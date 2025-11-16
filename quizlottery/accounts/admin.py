from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    # --- Columns displayed in the list view ---
    list_display = (
        "id",
        "mobile_number",
        "full_name",
        "province",
        "city",
        "is_active",
        "is_admin",
        "register_date",
        "last_login",
        "show_profile_image",
    )

    # --- Clickable fields in list view ---
    list_display_links = ("id", "mobile_number")

    # --- Admin sidebar filters ---
    list_filter = (
        "is_active",
        "is_admin",
        "gender",
        "province",
        "city",
        "register_date",
    )

    # --- Search functionality in admin ---
    search_fields = (
        "mobile_number",
        "name",
        "family",
        "national_id",
        "email",
    )

    # --- Items per page ---
    list_per_page = 25

    # --- Readonly fields (non-editable in admin form) ---
    readonly_fields = (
        "last_login",
        "register_date",
        "show_profile_image_large",
    )

    # --- Structured layout for the user detail/edit page ---
    fieldsets = (
        ("اطلاعات کاربری", {
            "fields": (
                "mobile_number",
                ("name", "family"),
                "email",
                "gender",
                ("province", "city"),
                "national_id",
            )
        }),
        ("عکس‌ها", {
            "fields": (
                "image_name",
                "show_profile_image_large",
                "cover_image",
            )
        }),
        ("اطلاعات تکمیلی", {
            "fields": (
                "active_code",
            )
        }),
        ("وضعیت", {
            "fields": (
                "is_active",
                "is_admin",
                "is_superuser",
                "last_login",
                "register_date",
            )
        }),
    )

    # --- Admin actions that apply to multiple selected users ---
    actions = ["activate_users", "deactivate_users"]

    # ---------------------------
    #  Custom Methods
    # ---------------------------

    # Returns a nicely formatted full name
    def full_name(self, obj):
        return f"{obj.name} {obj.family}".strip()
    full_name.short_description = "نام کامل"

    # Displays a small circular thumbnail in the list view
    def show_profile_image(self, obj):
        if obj.image_name:
            return format_html(
                "<img src='{}' width='40' height='40' style='border-radius:50%; object-fit:cover;'>",
                obj.image_name.url
            )
        return "—"
    show_profile_image.short_description = "عکس"

    # Large image preview inside the user detail page
    def show_profile_image_large(self, obj):
        if obj.image_name:
            return format_html(
                "<img src='{}' width='200' style='border-radius:12px;'>",
                obj.image_name.url
            )
        return "—"
    show_profile_image_large.short_description = "پیش‌نمایش عکس پروفایل"

    # --- Admin Action: Activate selected users ---
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "کاربران با موفقیت فعال شدند.")
    activate_users.short_description = "فعال‌سازی کاربران انتخاب‌شده"

    # --- Admin Action: Deactivate selected users ---
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "کاربران با موفقیت غیرفعال شدند.")
    deactivate_users.short_description = "غیرفعال‌سازی کاربران انتخاب‌شده"
