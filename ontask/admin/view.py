# -*- coding: utf-8 -*-

"""Admin classes for the views."""

from django.contrib import admin

from ontask.models import View


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    """Class to admin the views."""

    list_display = (
        'id',
        'workflow',
        'name',
        'description_text',
        'created',
        'modified',
        'formula')
