import os
from imbox import Imbox
from sender import Mail, Message
import pendulum


imap = os.environ['GMAIL_IMAP']
user = os.environ['GMAIL_USER']
pwrd = os.environ['GMAIL_PASS']

if __name__ == "__main__":
    with Imbox(imap, username=user, password=pwrd,
               ssl=True, ssl_context=None,
               starttls=False) as imbox:
        drafts = imbox.messages(folder="[Gmail]/Drafts")
        todays_mail = []
        for uid, msg in drafts:
            if 'schedmail' in msg.subject.lower():
                date = msg.subject.lower().split(':')[1]
                today = pendulum.now().date().isoformat()
                subject_date = pendulum.parse(date).date().isoformat()
                if subject_date == today:
                    todays_mail.append(msg)

    mail = Mail('smtp.gmail.com', port=587, username=user,
                password=pwrd, use_tls=True)

    for i in todays_mail:
        msg = Message(i.subject.split(':')[-1])
        msg.fromaddr = (i.sent_from[0]['name'], i.sent_from[0]['email'])
        msg.to = [j['email'] for j in i.sent_to]
        msg.cc = [j['email'] for j in i.cc]
        msg.bcc = [j['email'] for j in i.bcc]
        msg.body = i.body['plain'][0]
        msg.html = i.body['html'][0]
        msg.charset = 'utf-8'

        mail.send(msg)
