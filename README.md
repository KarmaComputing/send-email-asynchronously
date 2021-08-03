# Send all emails

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
