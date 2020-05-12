from flask import Flask, render_template, make_response, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length
import pdfkit

"""
config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
pdfkit.from_file('templates/report.html', 'out-test.pdf', configuration=config)
"""

app = Flask(__name__)
app.secret_key='hello'   # secret key used for encrypt and decrypt server data


Bootstrap(app)

class reportForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=5, max=15)])
    location = StringField('Location', validators=[InputRequired(), Length(min=2, max=30)])
    amount_fined = IntegerField('Amount Fined', validators=[InputRequired(), Length(min=1, max=5)])


@app.route('/', methods=["POST", "GET"]) #http://127.0.0.1:5000/name/location
#def pdf_template(name, location, amount_fined):
def pdf_template():
    # let each final pdf be named with the string of the first name together withe license number
    
    path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    # Pass the options to format the pdf
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }

    form = reportForm(request.form)

    if form.validate_on_submit:
        #details = reportForm(name=form.name.data, location=form.location.data, amount_fined=form.amount_fined.data)
        #ticketname = reportForm(name=form.name.data)
        #print (ticketname)
        #fname = 'pdfs/'+ticketname+'.pdf'
        fname = 'pdfs/fine_slip2.pdf'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        rendered = render_template('report.html')  # name=name , location=location, amount_fined=amount_fined)
        css = ['static/style.css']
        pdf = pdfkit.from_string(rendered, fname, options=options, toc=None, cover=None, css=css, configuration=config)

        
        return render_template('report_temp.html', form=form)

    return render_template('report_temp.html', form=form)
    

    #return redirect(url_for('dashboard'))
    #return render_template('report.html')
    #return "done"
'''
@app.route('/', methods=["POST", "GET"])
def passer():
    form = reportForm()

    if form.validate_on_submit:
        pdf_template(form)#form.name.data, form.location.data, form.amount.data)

        return render_template('report_temp.html', form=form)

    return render_template('report_temp.html', form=form)
'''

@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    form = reportForm()

    return render_template('loginv2.html', form = form)


if __name__=="__main__":
    app.run(debug=True)