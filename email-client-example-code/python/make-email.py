# Ref https://docs.python.org/3/library/email.examples.html

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
import time

# Create the base text message.
msg = EmailMessage()
msg["Subject"] = "Ayons asperges pour le déjeuner"
msg["From"] = Address("Pepé Le Pew", "chris", "karmacomputing.co.uk")
msg["To"] = Address("Penelope Pussycat", "chris", "karmacomputing.co.uk")
msg.set_content(
    """\
Salut!
Cela ressemble à un excellent recipie[1] déjeuner.

[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

--Pepé
"""
)

# Add the html version.  This converts the message into a multipart/alternative
# container, with the original text message as the first part and the new html
# message as the second part.
asparagus_cid = make_msgid()
msg.add_alternative(
    """\
<html>
  <head></head>
  <body>
    <p>Salut!</p>
    <p>Cela ressemble à un excellent
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718"> # noqa
            recipie
        </a> déjeuner.
    </p>
  </body>
</html>
""",
    subtype="html",
)
# note that we needed to peel the <> off the msgid for use in the html.


# Make a local copy of what we are going to send.

timestamp = time.time_ns()

with open(f"./emails/email-{timestamp}.msg", "wb") as f:
    f.write(bytes(msg))
