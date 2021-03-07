"""
In the send_email() function, the application instance is passed as an argument to a
background thread that will then deliver the email without blocking the main application.

Using current_app directly in the send_async_email() function that runs as a background
thread would not have worked, because current_app is a context-aware variable that is tied to
the thread that is handling the client request. In a different thread, current_app would
not have a value assigned.

Passing current_app directly as an argument to the thread object would not have worked either,
because current_app is really a proxy object that is dynamically mapped to the application
instance. So passing the proxy object would be the same as using current_app directly in the thread.

### IMPORTANT:
What I needed to do is access the real application instance that is stored inside the proxy object,
and pass that as the app argument. The current_app._get_current_object() expression extracts the
actual application instance from inside the proxy object, so that is what I passed to the thread
as an argument.
"""
from threading import Thread
from flask_mail import Message
from flask import render_template, current_app
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # The current_app._get_current_object() expression extracts the actual application instance 
    # from inside the proxy object, so that is what I passed to the thread as an argument.
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.jinja',
                                         user=user, token=token))
