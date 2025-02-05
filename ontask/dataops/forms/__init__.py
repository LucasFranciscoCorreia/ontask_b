# -*- coding: utf-8 -*-

"""Package with forms to perform uploads, plugig execution."""

from ontask.dataops.forms.dataframeupload import load_df_from_sqlconnection
from ontask.dataops.forms.plugin import PluginInfoForm
from ontask.dataops.forms.row import RowForm
from ontask.dataops.forms.select import SelectColumnUploadForm, SelectKeysForm
from ontask.dataops.forms.upload import (
    FIELD_PREFIX, SQLConnectionForm, SQLRequestPassword, UploadCSVFileForm,
    UploadExcelFileForm, UploadGoogleSheetForm, UploadS3FileForm,
)
