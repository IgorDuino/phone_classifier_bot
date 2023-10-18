from django.contrib import admin
from classifier.models import ClassificationRequest


@admin.register(ClassificationRequest)
class ClassificationRequestAdmin(admin.ModelAdmin):
    list_display = ("phone", "country", "telegram_age", "whatsapp_age", "average_age")
    list_filter = ("country",)
    search_fields = ("phone",)
    readonly_fields = ("telegram_age", "whatsapp_age", "average_age")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone",
                    "country",
                    "telegram_age",
                    "whatsapp_age",
                    "average_age",
                    "telegram_avatar_url",
                    "whatsapp_avatar_url",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        return False
