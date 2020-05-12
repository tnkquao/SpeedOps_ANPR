from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import pdfkit

app = Flask(__name__)
app.secret_key='hello'   # secret key used for encrypt and decrypt server data

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/speedops'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['TESTING'] =False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] =True
app.config['MAIL_USE_TLS'] =False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'tarek.quao@gmail.com'
app.config['MAIL_PASSWORD'] = 'BoundlessLove'
app.config['MAIL_DEFAULT_SENDER'] = 'tarek.quao@gmail.com'
app.config['MAIL_MAX_MAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False


db = SQLAlchemy(app)
mail = Mail(app)


class owners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    home_address = db.Column(db.String(60))
    license_plate = db.Column(db.String(100))
    contact_1 = db.Column(db.Integer)
    contact_2 = db.Column(db.String(100))


#@app.route('/<name>/<location>/<amount_fined>/<license_number>')
@app.route('/send')
def index():#name, location, amount_fined, license_number):
    """
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
    """

    msg = Message('Speeding Ticket Issue', recipients=['revid30916@ismailgul.net']) #the_owner.contact_2
    #msg.attach(fname, 'application/pdf', pdf)
    msg.body = 'Hello, Please find attached your speeding ticket details from (date) offense at ' #+ location+  ' \n Be sure to make payments in the next 7 days.'
    mail.send(msg)
    return 'message sent'       #redirect(url_for('index'))

    """
    msg = Message('Hello', sender='tarek.quao@gmail.com', recipients='revid30916@ismailgul.net')
    mail.send(msg)
    return 'Message sent!'
    """
if __name__=="__main__":
    db.create_all()
    app.run(debug=True)