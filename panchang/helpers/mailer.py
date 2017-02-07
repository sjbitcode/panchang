import logging
import logging.config

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# logger = logging.getLogger('mailer-logger')

# Configure logger
# logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('panchang.tasks')


class Mailer:
    def __init__(self, sender_email, sender_password, smtp_server):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.templatedir = os.path.join(BASE_DIR, 'templates')
        self.imgdir = os.path.join(BASE_DIR, 'img')
        self.env = Environment(loader=FileSystemLoader(self.templatedir))

    def send_email(self, email_data, template):
        '''
        Establish smtp connection and login.
        Create email message with given data and template.
        Send email.
        '''
        smtp = self.smtp_connect()
        msg = self.create_email(email_data, template)

        try:
            smtp.sendmail(
                self.sender_email,
                email_data['receivers'],
                msg.as_string()
            )
            logger.info('Sent email!')
            # print('Email sent!!!')
            # log.info('Email sent from {} to {}'.format(
            #     self.sender_email,
            #     ', '.join(email_data['receivers'])
            # ))
        except smtplib.SMTPException as e:
            # log.exception('Error sending mail from {} to {}'.format(
            #     self.sender_email,
            #     ', '.join(email_data['receivers'])
            # ))
            # print('Could not send email: {}'.format(e))
            raise
        smtp.quit()

    def smtp_connect(self):
        '''
        Attempts to connect and login to an smtp server.
        Calls smtp_login to login.

        Returns smtp object if successful, else raises Exception.
        '''
        try:
            smtp_ssl = smtplib.SMTP_SSL(self.smtp_server)
            smtp_ssl.ehlo()
            smtp_ssl = self.smtp_login(smtp_ssl)
        except Exception as e:
            print('Could not connect to {}: {}'.format(self.smtp_server, e))
            raise
        return smtp_ssl

    def smtp_login(self, smtp):
        '''
        Attempts to login to an smtp server with
        an email and password.

        Returns smtp object if successful, else raises Exception.
        '''
        try:
            smtp.login(self.sender_email, self.sender_password)
        except smtplib.SMTPException as e:
            print('Could not login with {}/{} on {}: {}'.format(
                self.sender_email, self.sender_password, smtp, e))
            raise
        return smtp

    def render_template(self, data, template):
        '''
        Render given data context to given template.
        '''
        template = self.env.get_template(template)
        email_body = template.render(data)
        return email_body

    def attach_image(self, msg, img_path):
        '''
        Attaches image to MIMEMultipart email container.
        '''
        fp = open(img_path, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-ID', '<{}>'.format(img_path))
        msg.attach(img)
        return msg

    def create_email(self, email_data, template):
        '''
        Given email_data dictionary,
            ex. {
                'subject': 'Hi there',
                'receivers': ['bob@example.com', 'jim@example.com'],
                'images': ['world.png', 'smiley.png'],
                'data': {'msg': 'Hello world'}
            }

        and a template (ex. 'say-hello.html'),

        create the email message, render the template with
        data from email_data dictionary
        '''

        # inject absolute paths to all images in context data.
        for img in email_data['images']:
            img_name = img.split('.')[0]
            email_data['data'][img_name] = os.path.join(self.imgdir, img)

        # render template with context data.
        email_body = self.render_template(email_data['data'], template)

        # Create container email message.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = email_data['subject']
        msg['From'] = self.sender_email
        msg['To'] = ','.join(email_data['receivers'])

        # attach email body and images to msg.
        msg.attach(MIMEText(email_body, 'html', 'utf-8'))
        for img in email_data['images']:
            img_name = img.split('.')[0]
            msg = self.attach_image(msg, email_data['data'][img_name])

        return msg
