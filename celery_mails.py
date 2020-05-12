from flask import Flask, render_template, redirect, url_for
from flask_celery import make_celery
from flask_sqlalchemy import SQLAlchemy
import pdfkit
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
#app.config['CELERY_BACKEND'] = 'db+mysql://root:@localhost/speedops_tasks'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/test'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.config['MAIL_SERVER'] = 'smtp.gmail.com'     #'mail.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] =False
app.config['MAIL_USE_TLS'] =True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'tarek.quao@gmail.com'
app.config['MAIL_PASSWORD'] = 'BoundedLove'
app.config['MAIL_DEFAULT_SENDER'] = ('DVLA', 'tarek.quao@gmail.com')
app.config['MAIL_MAX_MAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = None


#app.config.from_pyfile('config.cfg')    # sensitive config details


db = SQLAlchemy(app)
celery = make_celery(app)
mail = Mail(app)


class owners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    home_address = db.Column(db.String(60))
    license_plate = db.Column(db.String(100))
    contact_1 = db.Column(db.Integer)
    contact_2 = db.Column(db.String(100))

# MAILING A BUNCH OF offences look at how to use dictionaries like was done here https://youtu.be/48Eb8JuFuUI?t=1538

@app.route('/generate', methods=["POST", "GET"]) #http://127.0.0.1:5000/name/location
def send_report(name, location, amount_fined, license_number):
    send.delay(name, location, amount_fined, license_number)

    return 'PDF has been generated and sent!'
@celery.task(name='celery_mail_pdf.send')
def send(name, location, amount_fined, license_number):
    # let each final pdf be named with the string of the first name together withe license number
    
    path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    # Pass the options to format the pdf
    options = {
        'page-size': 'Letter', 'margin-top': '0.75in',
        'margin-right': '0.75in', 'margin-bottom': '0.75in',
        'margin-left': '0.75in', 'encoding': "UTF-8", 'no-outline': None
    }

    fname = name+'.pdf'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    rendered = render_template('report.html', name=name , location=location, amount_fined=amount_fined)
    pdf = pdfkit.from_string(rendered, fname, configuration=config, options=options)

    the_owner = owners.query.filter(owners.license_plate==license_number).first()

    msg = Message('Speeding Ticket Issue', sender='tarek.quao@gmail.com', recipients=['behek54387@bwtdmail.com']) #the_owner.contact_2
    msg.attach(fname, 'application/pdf', pdf)
    msg.body = 'Hello, Please find attached your speeding ticket details from (date) offense at ' + location
    +  ' \n Be sure to make payments in the next 7 days.'
    mail.send(msg)

    return redirect(url_for('dashboard'))
if __name__=="__main__":
    
    db.create_all()
    app.run(debug=True)