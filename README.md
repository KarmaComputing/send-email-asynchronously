# Send all emails

1. You have a directory full of emails (text RFC 5322 or html email) and you want to send them all
2. Use this script to pipe each message to Postfix via `sendmail`.
3. Once send to `sendmail`, each email is deleted from the folder


- push-emails.sh - (app) pushes emails (text files) to server
- send-all-emails.sh (server) submits emails to postfix


# Usage: send-all-emails.sh <path-to-emails> (see incrontab to watch directory)

- Submits all emails found in <path-to-emails> to the
- Postfix  sendmail command which causes mails to get
- queued
- Each email is removed after piping to sendmail.
- Note: Email files must be text RFC emails (e.g. RFC 5322)
- Note: sendmail submits to Postfix's postdrop
- Note: Requires a running Postfix server

Need an email server?

See 
- http://www.postfix.org/
- https://github.com/chrisjsimpson/ansible-mailserver
- https://wildduck.email/


## Example RFC valid email

email1.txt
```
To: alice@example.com
Subject: Testing
From: bob@example.com

This is a test message
```

### Generate an RFC 5322 email
```
# Ref https://docs.python.org/3/library/email.examples.html
import smtplib
from email.message import EmailMessage

# Create a text/plain message
msg = EmailMessage()
msg.set_content("This is my email")

msg['Subject'] = f'Test my email'
msg['From'] = "bob@example.co.uk"
msg['To'] = "alice@example.co.uk"

with open("email.exmple", "w") as fp:
    fp.write(msg.as_string())
```

### Generate a html email
```
#Ref https://docs.python.org/3/library/email.examples.html
import smtplib

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

# Create the base text message.
msg = EmailMessage()
msg['Subject'] = "Ayons asperges pour le déjeuner"
msg['From'] = Address("Pepé Le Pew", "chris", "karmacomputing.co.uk")
msg['To'] = (Address("Penelope Pussycat", "chris", "karmacomputing.co.uk"))
msg.set_content("""\
Salut!
  
Cela ressemble à un excellent recipie[1] déjeuner.

[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

--Pepé
""")

# Add the html version.  This converts the message into a multipart/alternative
# container, with the original text message as the first part and the new html
# message as the second part.
asparagus_cid = make_msgid()
msg.add_alternative("""\
<html>
  <head></head>
  <body>
    <p>Salut!</p>
    <p>Cela ressemble à un excellent
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
            recipie
        </a> déjeuner.
    </p>
  </body>
</html>
""".format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
# note that we needed to peel the <> off the msgid for use in the html.


# Make a local copy of what we are going to send.
with open('outgoing.msg', 'wb') as f:
    f.write(bytes(msg))
```

# Watch a directory for new files
```
apt install incron
```
Add user to allowed list
```
vi /etc/incron.allow
```

Run script when email(s) are added to the directory

```
incrontab -e
```
incrontab entry:

```
<path-to-email-files> IN_CLOSE_WRITE,loopable=true /bin/bash <path-to-send-all-emails.sh> <path-to-emails-folder>

# e.g:
/var/mail IN_CLOSE_WRITE,loopable=true /bin/bash /home/<username>/path-to-send-all-emails.sh /var/mail
```

## Errors

##### incrond[27693]: cannot exec process: No such file or directory
[Inside you incrontabs, you must leave *only* 1 space between the <path> <mask> <cmd>.](http://sudoall.com/incrond-cannot-exec-process-no-such-file-or-directory/)
