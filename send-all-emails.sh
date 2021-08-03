#!/bin/bash
  
set -euxo pipefail

# Usage: send-all-emails.sh <path-to-emails>

# Submits all emails found in <path-to-emails> to the
# Postfix  sendmail command which causes mails to get
# queued
# Each email is removed after piping to sendmail.
# Note: sendmail submits to Postfix's postdrop
# Note: Email files must be text RFC emails (e.g. RFC 5322)
# Note: Requires a running Postfix server

PATH_TO_EMAILS=$1

EMAILS="$PATH_TO_EMAILS/*"

for email in $EMAILS
do
    cat "$email" | sendmail -t
    rm $email
done
