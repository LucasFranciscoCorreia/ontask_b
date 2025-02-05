# -*- coding: utf-8 -*-

"""Models for the plugin registry and the SQL connections."""

from builtins import object

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ontask.models.const import CHAR_FIELD_LONG_SIZE, CHAR_FIELD_MID_SIZE


class Plugin(models.Model):
    """Model to store the plugins in the system.

    @DynamicAttrs
    """

    # file in the server
    filename = models.CharField(
        max_length=CHAR_FIELD_LONG_SIZE,
        blank=False,
        unique=True,
    )

    # Last time the file was checked (to detect changes)
    modified = models.DateTimeField(auto_now=True, null=False)

    # Name provided by the plugin
    name = models.CharField(max_length=CHAR_FIELD_MID_SIZE, blank=False)

    # Description text
    description_text = models.CharField(
        max_length=CHAR_FIELD_LONG_SIZE,
        default='',
        blank=True,
    )

    # Boolean stating if the plugin is a model or a transformation
    is_model = models.BooleanField(
        default=None,
        verbose_name=_('Is a model'),
        null=True,
        blank=True,
    )

    # Boolean stating if the plugin is ready to run
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Ready to run'),
        null=False,
        blank=False,
    )

    # Boolean stating if the plugin is allowed to run
    is_enabled = models.BooleanField(
        default=False,
        verbose_name=_('Enabled'),
        null=False,
        blank=False,
    )

    # Last time the file was checked (to detect changes)
    executed = models.DateTimeField(
        _('Last verified'),
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        """Render name with field."""
        return self.name

    class Meta(object):
        """Define the criteria for ordering."""

        ordering = ['name']
