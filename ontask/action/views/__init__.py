# -*- coding: utf-8 -*-

"""Module with all the views used related to actions."""

from ontask.action.views.action import (
    ActionCreateView, ActionUpdateView, action_index, delete_action,
    edit_action,
)
from ontask.action.views.clone import clone_action, clone_condition
from ontask.action.views.condition import (
    ConditionCreateView, FilterCreateView, delete_condition, delete_filter,
    edit_condition, edit_filter,
)
from ontask.action.views.edit_personalized import (
    action_out_save_content, edit_action_out, showurl,
)
from ontask.action.views.edit_survey import (
    edit_action_in, edit_description, select_column_action,
    select_condition_for_question, shuffle_questions, unselect_column_action,
)
from ontask.action.views.import_export import (
    action_import, export_ask, export_done, export_download,
)
from ontask.action.views.preview import (
    preview_next_all_false_response, preview_response,
)
from ontask.action.views.run import (
    run_action, run_action_item_filter, serve_action, serve_action_lti
)
from ontask.action.views.run_canvas_email import run_canvas_email_done
from ontask.action.views.run_email import run_email_done
from ontask.action.views.run_json import run_json_done
from ontask.action.views.run_survey import (
    run_survey_row, run_survey_ss, survey_thanks,
)
from ontask.action.views.run_zip import (
    action_zip_export, run_zip_done, zip_action,
)
from ontask.action.views.timeline import show_timeline
