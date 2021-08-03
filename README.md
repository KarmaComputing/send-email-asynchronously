# Send all emails

With many text emails in a directoy, send them
all one by one to postfix, then remove them (fire and forget).

# Usage: send-all-emails.sh <path-to-emails>

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
