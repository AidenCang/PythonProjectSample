from django.contrib import admin

# Register your models here.
from channelsApp.models import Room
from users.models import UserProfile

admin.site.register(
    Room,
    list_display=["id", "title", "staff_only"],
    list_display_links=["id", "title"],
)


admin.site.register(
    UserProfile,
    list_display=["username", "birthday", "gender","mobile","email"],
)
