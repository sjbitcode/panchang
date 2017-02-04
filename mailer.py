import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from jinja2 import Environment, FileSystemLoader


class Mailer:
    def __init__(
        self, sender_email, sender_password,
        receivers, subject, body
    ):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receivers = receivers
        self.subject = subject
        self.body = body
        self.server = 'smtp.gmail.com'
        self.templatedir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'templates'
        )
        self.imgdir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'img'
        )
        self.env = Environment(loader=FileSystemLoader(self.templatedir))

    def email_text(self):
        return 'Subject: {}\n\n{}'.format(self.subject, self.body)

    def send_email(self):
        try:
            # Set up server and login.
            server_ssl = smtplib.SMTP_SSL(self.server)
            server_ssl.ehlo()
            server_ssl.login(self.sender_email, self.sender_password)

            # Send email!
            email_text = self.email_text()
            server_ssl.sendmail(self.sender_email, self.receivers, email_text)
            server_ssl.quit()
            print('Email sent!')
        except smtplib.SMTPException:
            print('Something went wrong!')

    def send_html_email(self):
        # Create message container - t
        # he correct MIME type is multipart/alternative.
        attachment1 = 'logo.gif'
        attachment2 = 'diya.gif'

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "helooooo"
        msg['From'] = self.sender_email
        msg['To'] = ','.join(self.receivers)

        html = '''\
<html>
    <head></head>
    <body>
        <img src='cid:{}'>
        <table align="center" style="width:100%;">
            <tr>
                <th style="text-align:center;">Suntime times</th>
            </tr>
            <tr>
                <td>Sunrise</td>
                <td>07:06:23 AM</td>
            </tr>
            <tr>
                <td>Sunset</td>
                <td>05:54:12 PM</td>
            </tr>

            <tr></tr>
            <tr></tr>
            <tr></tr>

            <tr>
                <th style="text-align:center;">Auspicious times</th>
            </tr>
            <tr>
                <td>Abhijit Muhurta</td>
                <td>11:49:40 AM - 12:30:03 PM</td>
            </tr>
            <tr>
                <td>Amritkalam</td>
                <td>08:22:41 AM - 09:38:25 AM</td>
            </tr>

            <tr></tr>
            <tr></tr>
            <tr></tr>

            <tr>
                <th style="text-align:center;">Inauspicious times</th>
            </tr>
            <tr>
                <td>Durmuhurtham</td>
                <td>11:49:40 AM - 12:30:03 PM</td>
            </tr>
            <tr>
                <td>Yamagandam</td>
                <td>11:09:02 PM - 12:41:22 AM (tomorrow)</td>
            </tr>
            <tr>
                <td>Rahukalam</td>
                <td>11:49:40 AM - 12:30:03 PM</td>
            </tr>
            <tr>
                <td>Varjyam</td>
                <td>11:49:40 AM - 12:30:03 PM</td>
            </tr>
            <tr>
                <td>Gulikai</td>
                <td>11:49:40 AM - 12:30:03 PM</td>
            </tr>
        </table>
    </body>
</html>
'''.format(attachment1)

        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        fp = open(os.path.join(self.imgdir, attachment2), 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-ID', '<{}>'.format(attachment1))
        msg.attach(img)

        try:
            # Set up server and login.
            server_ssl = smtplib.SMTP_SSL(self.server)
            server_ssl.ehlo()
            server_ssl.login(self.sender_email, self.sender_password)

            # Send email!
            server_ssl.sendmail(self.sender_email, self.receivers, msg.as_string())
            server_ssl.quit()
            print('Email sent!')
        except smtplib.SMTPException:
            print('Something went wrong!')

    def jinja_email(self, data):
        # urls = ['http://example.com/1', 'http://example.com/2', 'http://example.com/3']
        data['img1'] = 'img/diya.gif'
        data['img2'] = 'img/logo.gif'
        # data = {
        #     'img1': 'img/diya.gif',
        #     'img2': 'img/logo.gif',
        #     'urls': urls
        # }
        text = self.env.get_template('email-body2.html')
        email_body = text.render(data)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = data['subject']
        msg['From'] = self.sender_email
        msg['To'] = ','.join(self.receivers)
        msg.attach(MIMEText(email_body, 'html', 'utf-8'))

        # Attach images to msg
        fp = open(data['img1'], 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-ID', '<{}>'.format(data['img1']))
        msg.attach(img)

        fp = open(data['img2'], 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-ID', '<{}>'.format(data['img2']))
        msg.attach(img)

        try:
            # Set up server and login.
            server_ssl = smtplib.SMTP_SSL(self.server)
            server_ssl.ehlo()
            server_ssl.login(self.sender_email, self.sender_password)

            # Send email!
            server_ssl.sendmail(self.sender_email, self.receivers, msg.as_string())
            server_ssl.quit()
            print('Email sent!')
        except smtplib.SMTPException:
            print('Something went wrong!')
