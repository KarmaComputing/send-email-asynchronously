from flask import Flask
from write_email import write_email

app = Flask(__name__)

EMAIL_PATH = "./emails"  # Normally you would put this in your .env file


@app.route("/send-email")
def queue_email():
    """Note: We don't send the email here
    because that would be slow, instead we're
    writing it to disk, then (see the main repo
    readme for how to set-up inotify to copy
    these email files to the mail server and send them"""
    write_email()
    return "That was fast! Check the emails directory to see email files ready for copying to server"
