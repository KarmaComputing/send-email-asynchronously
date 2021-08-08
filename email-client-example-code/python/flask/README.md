# Flask app python asynchronous email example

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

Now head over to [http://127.0.0.1:5000/send-email](http://127.0.0.1:5000/send-email)
and this will *write* an email file. See the main repo README for how to set-up automatic
push and sending via the email server.
