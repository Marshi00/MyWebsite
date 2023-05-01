import re
from flask import Flask, jsonify, request, session
from datetime import datetime, timedelta
from flask_wtf.csrf import CSRFProtect
from flask import render_template
from flask_mail import Mail, Message
import smtplib
import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=1)

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

csrf = CSRFProtect(app)

mail = Mail(app)

# set this to false in production!!
debug = False


@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/projects")
def projects():
    return render_template('resume.html')


@app.route('/email', methods=["POST"])
def sendEmail():
    if "email" in request.form and "name" in request.form and "message" in request.form:

        email = request.form['email']
        message = request.form['message']
        name = request.form['name']

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            error = True
        elif len(name) < 3:
            msg = 'Name is Required and has to be at least 3 characters!'
            error = True
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Name must contain only letters and numbers!'
            error = True
        elif not re.match(r'[A-Za-z0-9]+', message):
            msg = 'Message must contain only letters and numbers!'
            error = True
        elif len(message) < 10:
            msg = 'Message must bet at least 10 characters!'
            error = True
        else:
            try:
                if session.get('limit_sent_email'):
                    session['limit_sent_email'] = session['limit_sent_email'] + 1
                else:
                    session['limit_sent_email'] = 1

                if (session.get('limit_sent_email') > 3):
                    msg = 'You cant send more than 3 Emails per day!'
                else:

                    # sender = 'no_reply@mydomain.com'
                    # receivers = ['person@otherdomain.com']

                    # message = """From: No Reply <no_reply@mydomain.com>
                    #     To: Person <person@otherdomain.com>
                    #     Subject: Test Email

                    #     This is a test e-mail message.
                    # """
                    # smtp_obj = smtplib.SMTP('localhost')
                    # smtp_obj.sendmail(sender, receivers, message)

                    msg = 'Email sent successfully!'
                    message = message + "\n" + email
                    msgEmail = Message(
                        name,
                        sender=email,
                        recipients=[app.config['MAIL_USERNAME']]
                    )
                    msgEmail.body = message
                    mail.send(msgEmail)

                error = False
            except:
                msg = 'Couldnt send Email!, something went wrong'
                error = True
    else:
        msg = 'Something went wrong!'
        error = True

    return jsonify(
        error=error,
        msg=msg
    )

