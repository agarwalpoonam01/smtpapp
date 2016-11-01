import smtplib
import email.utils
from email.mime.text import MIMEText

# Create the message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'agrawal@gmail.com'))
msg['From'] = email.utils.formataddr(('Author', 'poonam@gmail.com'))
msg['Subject'] = 'Simple test message'

server = smtplib.SMTP('127.0.0.1', 1025)
server.set_debuglevel(True) # show communication with the server
try:
    server.sendmail('poonam@gmail.com', ['poonam@gmail.com','agrawal@gmail.com'], msg.as_string())
finally:
    server.quit()
