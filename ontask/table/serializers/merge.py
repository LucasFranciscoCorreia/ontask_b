# -*- coding: UTF-8 -*-#

"""Serilizers for frames and merge operations."""

import json

import pandas as pd
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from ontask.dataops.pandas import detect_datetime_columns
from ontask.table.serializers.pandas import DataFramePandasField


class DataFrameJSONField(serializers.Field):
    """Define the JSON field for serialization."""

    def to_representation(self, instance):
        """Transform DF to json with specific date format.

        Return the to_json result using Pandas. This function though is
        destructive with respect to NaN and NaT.
        """
        return json.loads(instance.to_json(date_format='iso'))

    def to_internal_value(self, data):
        """Create the data frame from the given data detecting date/time."""
        try:
            df = pd.DataFrame(data)
            # Detect date/time columns
            df = detect_datetime_columns(df)
        except Exception as exc:
            raise serializers.ValidationError(exc)

        return df


class DataFrameBasicMergeSerializer(serializers.Serializer):
    """Common functions for DF serializer."""

    how = serializers.CharField(
        required=True,
        initial='',
        help_text=_(
            'One of the following values: inner, outer, left or right'),
    )

    left_on = serializers.CharField(
        required=True,
        initial='',
        help_text=_(
            'ID of the column in destination data frame with unique key'))

    right_on = serializers.CharField(
        required=True,
        initial='',
        help_text=_('ID of column in source data frame with unique key'))


class DataFrameJSONMergeSerializer(DataFrameBasicMergeSerializer):
    """Merger serializer for data frame in JSON format."""

    src_df = DataFrameJSONField(
        help_text=_(
            'Field must be a JSON string encoding a pandas data frame'),
    )


class DataFramePandasMergeSerializer(DataFrameBasicMergeSerializer):
    """Merger serializer for data frame in pandas format."""

    src_df = DataFramePandasField(
        help_text=_(
            'This field must be the Base64 encoded '
            + 'result of pandas.to_pickle() function'),
    )
