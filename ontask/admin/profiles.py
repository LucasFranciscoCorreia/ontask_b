# -*- coding: utf-8 -*-

"""Admin classes for Profiles"""

from authtools.admin import NamedUserAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse

from ontask.models import Profile

User = get_user_model()
admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class NewUserAdmin(NamedUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('is_active', 'email', 'name', 'permalink',
                    'is_superuser', 'is_staff',)

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        url = reverse("profiles:show",
                      kwargs={"slug": obj.profile.slug})
        # Unicode hex b6 is the Pilcrow sign
        return '<a href="{}">{}</a>'.format(url, '\xb6')
    permalink.allow_tags = True
