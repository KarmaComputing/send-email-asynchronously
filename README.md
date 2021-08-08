# Send all emails

1. You have a directory full of emails (text RFC 5322 or html email) and you want to send them all
2. Use this script to pipe each message to Postfix via `sendmail`.
3. Once send to `sendmail`, each email is deleted from the folder


- push-emails.sh - (app) pushes emails (text files) to server
- send-all-emails.sh (server) submits emails to postfix

# Why is this useful?

Allows you to easily send email asynchronously or send email in background.
Especially web applications will block and wait until the email is sent before loading the page, 
which is slow. Why is it slow? Because your application is sending the email in the same process,
you may get away with using `threads` , however depending on your web server these threads may die
with the request and is not reliable for this reason.

### Why does sending an email block my application from loading anyway?

tldr 1: Because your code has to connect to another server, which takes ages, wait, and then carry on
tldr 2: Because sending email during script execution is usually synchronous by default 
rather than asynchronous, you need to do long-running tasks asynchronously

e.g. What happens when your application sends an email:

The main [thread](https://en.wikipedia.org/wiki/Thread_(computing)) of your application:

- Opens a TCP connection to the email server (which could be in another country)
- Logs into the email server (SMTP auth)
- Submits the email to the email server over the TCP connection (SMTP submission)
- Waits for the SMTP submission to complete
- Finally continues loading your app.

How to make that faster?

Stop sending the email during the script synchronously. The code in this
repo is *one* way to achieve this.

> "We can solve any problem by introducing an extra level of indirection." - [David Wheeler (1927 – 13 December 2004)](https://en.wikipedia.org/wiki/David_Wheeler_(computer_scientist))

It works like this:

1. In your application, instead of sending your email(s) right away, simply write them to a single folder on your server (is *very* fastand easy to write to a file) see [examples](https://github.com/chrisjsimpson/send-all-emails/tree/main/email-client-example-code). This is important as your application is no longer blocking whilst sending an email. So when *do* emails get sent? - They're copyied to the email server in the background, [`inotify`](https://en.wikipedia.org/wiki/Inotify) notices a new email is in the directory, and the email file is pushed into [postfix](https://en.wikipedia.org/wiki/Postfix_(software)) for sending. 
2. In the background, watch for files as they get created in the folder with emails you created using [(we use inotify to achieve this)](https://en.wikipedia.org/wiki/Inotify)
3. Run a command to `copy` these email to your email server using [incrontab](https://linux.die.net/man/5/incrontab)
Then, in the background, copy (e.g. using `scp`) the emails to your email server.
4. Simerly, the email server is watching the directory for email files to be written to, and when new email files are placed into the email folder, the `send-all-emails` script processes and sends the emails (e.g. using postfix)

Sending email asynchronously is a common question/problem when coding web applications
and (maybe?) isn't well understood:

- [socketlabs](https://www.socketlabs.com/blog/web-api-send-email-async/)
- [django (python)](https://code.djangoproject.com/ticket/28189)
- [flask (python)](https://stackoverflow.com/questions/32197564/how-to-send-emails-in-background-in-python-webapplication-with-flask-framework), [flask 'What happens with this code for me is that sometimes I receive an email and sometimes don't'](https://stackoverflow.com/questions/11047307/run-flask-mail-asynchronously/18407455), [flask mega tutorial-](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-email-support)
- [laravel (php)- cron/queue](https://laravel.com/docs/8.x/queues#running-the-queue-worker)

Often Celery/Redis/task-queues are [written about](https://www.peterspython.com/en/blog/celery-redis-and-the-in-famous-email-task-example) as a solution for this, but there are other ways since setting up and configuring these systems is outside of
typical day to day experience, hence there are many SaaS services to outsource this complexity, but understanding how things
work is useful/fun - and profitable skills to learn. 


# Usage: send-all-emails.sh <path-to-emails> (see incrontab to watch directory)

- Submits all emails found in <path-to-emails> to the
- Postfix  sendmail command which causes mails to get
- queued
- Each email is removed after piping to sendmail.
- Note: Email files must be text RFC emails (e.g. RFC 5322)
- Note: sendmail submits to Postfix's postdrop
- Note: Requires a running Postfix server

#### Need an email server?

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

## Emails are just plain text

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

# (Email Server) Watch directory for new files
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

# (App server) Watch directory for email files & push them to email server asynchronously
```
apt install incron
apt-get install keychain
```

Setup keychain (to allow incrontab) to scp to email server

```
# Add to end of ~/.bashrc
/usr/bin/keychain "$HOME/.ssh/id_rsa"
source "$HOME/.keychain/${HOSTNAME}-sh"
```

Add user to allowed list (e.g. alice/bob)
```
vi /etc/incron.allow
```

Run script when email(s) are added to the directory

```
incrontab -e
```
incrontab entry:

```
<path-to-email-files> IN_CLOSE_WRITE,loopable=true /bin/bash <push-emails.sh> <path-to-emails-folder>

# e.g:
/var/mail IN_CLOSE_WRITE,loopable=true /bin/bash /home/<username>/path-to-send-all-emails.sh /var/mail
```

## Errors

##### incrond[27693]: cannot exec process: No such file or directory
[Inside you incrontabs, you must leave *only* 1 space between the <path> <mask> <cmd>.](http://sudoall.com/incrond-cannot-exec-process-no-such-file-or-directory/)
