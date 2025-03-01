=========================
SMTP Email Notifier Utils
=========================

A simple module for sending SMTP-based notification emails.

Usage
=====

.. code-block:: python

    from smtp_email_notifier_utils.email_notifier import send_notification

    # Example usage
    recipient = "someone@example.com"
    subject = "Important Notification"
    message = "Hello, this is your notification message."

    success = send_notification(recipient, subject, message)
    if success:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification")

Exported scripts
================

* send-notification-email

.. code-block:: bash

    send-notification-email --recipient someone@example.com --subject="Important Notification" --message="Hello, this is your notification message."
