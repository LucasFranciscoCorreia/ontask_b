# -*- coding: utf-8 -*-

"""Admin definitions for action."""

from django.contrib import admin

from ontask.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    """Define Action Admin."""

    list_display = (
        'id',
        'workflow',
        'name',
        'description_text',
        'created',
        'modified',
        'text_content',
        'serve_enabled',
    )
