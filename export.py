import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import shutil
class exports():
   
    def __init__(self, recieving_email, loc, save_location):
        self.recieving_email = recieving_email
        self.loc = loc
        self.save_location = save_location

        
    def send_email(self):
        body = '''
        '''
        
        sender = ''
        #developer password
        password = ''
        receiver = self.recieving_email

        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = 'Report Generated on ' + datetime.today().strftime('%Y-%m-%d')

        message.attach(MIMEText(body, 'plain'))

        pdfname = self.loc
        binary_pdf = open(pdfname, 'rb')

        #creating the payload object and encoding it in base64 so it can be sent
        payload = MIMEBase('application', 'octate-stream', Name=pdfname)
        payload.set_payload((binary_pdf).read())
        encoders.encode_base64(payload)
        
        #attach the payload to the emamil
        payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
        message.attach(payload)

        session = smtplib.SMTP('smtp.gmail.com', 587)
        #start the STMP session
        session.starttls()
        
        session.login(sender, password)

        text = message.as_string()
        session.sendmail(sender, receiver, text)
        session.quit()

    def save_to_computer(self):
        try:
            #move the file to the desired location
            shutil.move(self.loc, self.save_location)
        except:
            pass
        return  