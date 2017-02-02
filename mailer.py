import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "helooooo"
        msg['From'] = self.sender_email
        msg['To'] = ','.join(self.receivers)

        html = '''\
        <html>
            <head></head>
            <body>
                <table style="border: blue 1px solid;">
                    <tr><td class="cell">Cell 1.1</td><td class="cell">Cell 1.2</td></tr>
                    <tr><td class="cell">Cell 2.1</td><td class="cell"></td></tr>
                </table>
            </body>
        </html>
        '''
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        # import pdb; pdb.set_trace();
        try:
            # Set up server and login.
            server_ssl = smtplib.SMTP(self.server)
            server_ssl.starttls()
            server_ssl.login(self.sender_email, self.sender_password)

            # Send email!
            server_ssl.sendmail(self.sender_email, self.receivers, msg.as_string())
            server_ssl.quit()
            print('Email sent!')
        except smtplib.SMTPException:
            print('Something went wrong!')
