from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from appsettings import SENDGRID_API_KEY, SENDGRID_EMAIL_FROM



class EmailSender():

    def __init__(self, to_email, subject, emailBody ):
        self.to_email = to_email
        self.subject = subject
        self.emailBody = emailBody

    def send(self):
        message = Mail(
            from_email= SENDGRID_EMAIL_FROM,
            to_emails= self.to_email,
            subject=self.subject,
            html_content=self.emailBody)
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)