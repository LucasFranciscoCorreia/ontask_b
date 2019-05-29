# -*- coding: utf-8 -*-

"""Test the views for the scheduler pages."""

import os

from django.conf import settings
from django.urls import reverse

from dataops.pandas import get_table_row_by_index
from table.views.table_display import (
    display, display_ss,
    display_view,
    display_view_ss,
    row_delete,
)
import test


class TableTestViewTableDisplay(test.OnTaskTestCase):
    """Test stat views."""

    fixtures = ['simple_table']
    filename = os.path.join(
        settings.BASE_DIR(),
        'table',
        'fixtures',
        'simple_table.sql',
    )

    user_email = 'instructor01@bogus.com'
    user_pwd = 'boguspwd'

    workflow_name = 'wflow1'

    def test_display(self):
        """Test the use of forms in to schedule actions."""
        # Remove is_key from column 'age'
        col = self.workflow.columns.get(name='age')
        col.is_key = False
        col.save()

        # Store the number of rows
        nrows = self.workflow.nrows

        # Get the visualization for the whole table
        resp = self.get_response('table:display', display)
        self.assertEqual(resp.status_code, 200)

        # Get the JSON subset of the table display
        resp = self.get_response(
            'table:display_ss',
            display_ss,
            method='POST',
            req_params={
                'draw': '1',
                'start': '0',
                'length': '10',
                'order[0][column]': '1',
                'order[0][dir]': 'asc',
                'search[value]': ''},
            is_ajax=True)
        self.assertEqual(resp.status_code, 200)

        # GEt the display of the view
        view = self.workflow.views.get(name='simple view')
        resp = self.get_response(
            'table:display_view',
            display_view,
            {'pk': view.id})
        self.assertEqual(resp.status_code, 200)

        # Get the JSON subset of the view display
        resp = self.get_response(
            'table:display_view_ss',
            display_view_ss,
            {'pk': view.id},
            method='POST',
            req_params={
                'draw': '1',
                'start': '0',
                'length': '10',
                'order[0][column]': '1',
                'order[0][dir]': 'asc',
                'search[value]': ''},
            is_ajax=True)
        self.assertEqual(resp.status_code, 200)

        # Delete one row of the table
        r_val = get_table_row_by_index(self.workflow, None, 1)
        resp = self.get_response(
            'table:row_delete',
            row_delete,
            req_params={'key': 'email', 'val': r_val['email']},
            is_ajax=True)
        self.assertEqual(resp.status_code, 200)

        req = self.factory.get(
            reverse('table:row_delete'),
            {'key': 'email', 'value': r_val['email']})

        # The POST request uses the params in the GET URL
        get_url = req.get_full_path()
        req = self.factory.post(
            get_url,
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        req = self.add_middleware(req)
        resp = row_delete(req)
        self.assertEqual(resp.status_code, 200)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.nrows, nrows - 1)

        # Incorrect post
        resp = self.get_response(
            'table:row_delete',
            row_delete,
            method='POST',
            req_params={'key': 'email', 'val': r_val['email']},
            is_ajax=True)
        self.assertEqual(resp.status_code, 200)
