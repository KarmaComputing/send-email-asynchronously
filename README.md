# Send all emails

1. You have a directory full of emails (text RFC 5322) and you want to send them all
2. Use this script to pipe each message to Postfix via `sendmail`.
3. Once send to `sendmail`, each email is deleted from the folder


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
