# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import datetime

import pytz
from django.conf import settings as ontask_settings
from django.contrib.sites.models import Site
from django.core import signing
from django.core.mail import send_mass_mail, send_mail
from django.template import Template, Context
from django.urls import reverse

import logs.ops
from action.evaluate import evaluate_action
from dataops import ops
from dataops import pandas_db
from email_action import settings
from workflow.models import Column


def send_messages(user,
                  action,
                  subject,
                  email_column,
                  from_email,
                  send_confirmation,
                  track_read,
                  add_column):
    """
    Performs the submission of the emails for the given action and with the
    given subject. The subject will be evaluated also with respect to the
    rows, attributes, and conditions.
    :param user: User object that executed the action
    :param action: Action from where to take the messages
    :param subject: Email subject
    :param email_column: Name of the column from which to extract emails
    :param from_email: Email of the sender
    :param send_confirmation: Boolean to send confirmation to sender
    :param track_read: Should read tracking be included?
    :param add_column: Should a new column be added?
    :return: Send the emails
    """

    # Evaluate the action string, evaluate the subject, and get the value of
    # the email colummn.
    result = evaluate_action(action,
                             extra_string=subject,
                             column_name=email_column)

    # Check the type of the result to see if it was successful
    if not isinstance(result, list):
        # Something went wrong. The result contains a message
        return result

    track_col_name = ''
    data_frame = None
    if add_column:
        data_frame = pandas_db.load_from_db(action.workflow.id)
        # Make sure the column name does not collide with an existing one
        i = 0  # Suffix to rename
        while True:
            i += 1
            track_col_name = 'EmailRead_{0}'.format(i)
            if track_col_name not in data_frame.columns:
                break

    # Everything seemed to work to create the messages.
    msgs = []
    for msg_body, msg_subject, msg_to in result:

        # If read tracking is on, add suffix for message (or empty)
        if track_read:
            # The track id must identify: action & user
            track_id = {
                'action': action.id,
                'sender': user.email,
                'to': msg_to,
                'column_to': email_column,
                'column_dst': track_col_name
            }

            track_str = \
                """<img src="https://{0}/{1}?v={2}" alt="" 
                    style="position:absolute; visibility:hidden"/>""".format(
                    Site.objects.get_current().domain,
                    reverse('trck'),
                    signing.dumps(track_id)
                )
        else:
            track_str = ''

        msgs.append((msg_subject, msg_body + track_str, from_email, [msg_to]))

    # Mass mail!
    if str(getattr(settings, 'EMAIL_HOST')):
        try:
            send_mass_mail(msgs, fail_silently=False)
        except Exception as e:
            # Something went wrong, notify above
            return e.message

    # Add the column if needed
    if add_column:
        # Create the new column and store
        column = Column(
            name=track_col_name,
            workflow=action.workflow,
            data_type='integer',
            is_key=False
        )
        column.save()

        # Increase the number of columns in the workflow
        action.workflow.ncols += 1
        action.workflow.save()

        # Initial value in the data frame and store the table
        data_frame[track_col_name] = 0
        ops.store_dataframe_in_db(data_frame, action.workflow.id)

    # Log the events (one per email)
    now = datetime.datetime.now(pytz.timezone(ontask_settings.TIME_ZONE))
    context = {
        'user': user.id,
        'action': action.id,
        'email_sent_datetime': str(now),
    }
    for msg in msgs:
        context['subject'] = msg[0]
        context['body'] = msg[1]
        context['from_email'] = msg[2]
        context['to_email'] = msg[3]
        logs.ops.put(user, 'action_email_sent', action.workflow, context)

    # Log the event
    logs.ops.put(
        user,
        'action_email_sent',
        action.workflow,
        {'user': user.id,
         'action': action.name,
         'num_messages': len(msgs),
         'email_sent_datetime': str(now),
         'filter_present': action.n_selected_rows != -1,
         'num_rows': action.workflow.nrows,
         'subject': subject,
         'from_email': user.email})

    # If no confirmation email is required, done
    if not send_confirmation:
        return None

    # Creating the context for the personal email
    context = {
        'user': user,
        'action': action,
        'num_messages': len(msgs),
        'email_sent_datetime': now,
        'filter_present': action.n_selected_rows != -1,
        'num_rows': action.workflow.nrows}

    # Create template and render with context
    template = Template(settings.NOTIFICATION_TEMPLATE)
    msg = template.render(Context(context))

    # Send email out
    try:
        send_mail(str(getattr(settings, 'NOTIFICATION_SUBJECT')),
                  msg,
                  str(getattr(settings, 'NOTIFICATION_SENDER')),
                  [user.email])
    except Exception as e:
        return 'An error occurred when sending your notification: ' + e.message

    # Log the event
    logs.ops.put(
        user,
        'action_email_notify', action.workflow,
        {'user': user.id,
         'action': action.id,
         'num_messages': len(msgs),
         'email_sent_datetime': str(now),
         'filter_present': action.n_selected_rows != -1,
         'num_rows': action.workflow.nrows,
         'subject': str(getattr(settings, 'NOTIFICATION_SUBJECT')),
         'body': msg,
         'from_email': str(getattr(settings, 'NOTIFICATION_SENDER')),
         'to_email': [user.email]})

    return None
