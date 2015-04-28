from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import threading


class MailSender(threading.Thread):

    MAIL_SUBJ_BASE = settings.APP_NAME + " - "

    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user
        self.callback = None
        self.msg = None

    def compose(self, title, template_url, context_json):
        context_json['user_name'] = self.user.name
        d = Context(context_json)
        text_content = get_template(template_url + '.txt').render(d)
        html_content = get_template(template_url + '.html').render(d)
        self.msg = EmailMultiAlternatives(self.MAIL_SUBJ_BASE + title,
                                     text_content,
                                     "info@app.com",
                                     [self.user.email])
        self.msg.attach_alternative(html_content, "text/html")

    def send(self):
        self.msg.send()

    def send_async(self, callback=None):
        self.callback = callback
        self.start()

    def run(self):
        self.send()
        if self.callback:
            self.callback()

