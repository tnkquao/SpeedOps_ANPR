from flask import Flask, render_template, url_for, request, redirect

from main2 import *
from forms import *
from models import *

#app = Flask(__name__)
app.secret_key='hello'   # secret key used for encrypt and decrypt server data

@app.route('/searching', methods=['GET', 'POST'])
def pager():
    search = OffenceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('searcher.html', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Name':
            #user = db.session.query(speeders).filter(
            #    speeders.name.contains(search_string))
            #user = speeders.query.filter_by(name=search_string)

            qry = db_session.query(speeders).filter(
                speeders.name.contains(search_string))
            results = qry.all() 

        elif search.data['select'] == 'License Plate':
            qry = db_session.query(speeders).filter(
                speeders.license_plate.contains(search_string))
            results = qry.all()
            user = admin.query.filter_by(username=search_string)

        elif search.data['select'] == 'Location':
            qry = db_session.query(speeders).filter(
                speeders.location.contains(search_string))
            results = qry.all()
        else:
            qry = db_session.query(speeders)
            results = qry.all()
    else:
        qry = db_session.query(speeders)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/searching')

    else:
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
        #return render_template('results.html', results=results)


# displays all culprits who have outstanding fines to pay
@app.route('/paid')
def all_paid():
    qry = db_session.query(speeders).filter(speeders.fine_paid==True)
    results = qry.all
    table = Results(results)
    table.border = True
    return render_template('results.html', table=table)


# displays all culprits who have outstanding fines to pay
"""(for the write up) this makes it easy for the admin at any office to cross check with the system, for which 
offendants have oustanding =fines to be paid before the fine gets confirmed/canceled, and to allow for
any further services the person may need to be supplied. for example, license renewal, road worthy, to name a few"""
@app.route('/unpaid')
def not_paid():
    qry = db_session.query(speeders).filter(speeders.fine_paid==False)
    results = qry.all
    table = Results(results)
    table.border = True
    return render_template('results.html', table=table)


# use/modify block of code to change payment status. besure to have printed statement "Paid" for each 'paid' record

"""
def save_changes(offence, form, new=False):
    
    #Save the changes to the database
    
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    owner = owners()
    owner.name = form.artist.data
    offence.owner = owner
    offence.title = form.title.data
    offence.release_date = form.release_date.data
    offence.publisher = form.publisher.data
    offence.media_type = form.media_type.data
    if new:
        # Add the new album to the database
        db_session.add(album)
    # commit the data to the database
    db_session.commit()
"""

"""
@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(speeders).filter(
                speeders.id==id)
    offence = qry.first()
    if offence:
        form = OffenceForm(formdata=request.form, obj=offence)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(offence, form)
            flash('Album updated successfully!')
            return redirect('/')
        return render_template('edit_album.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
#</int:id>
"""
"""
# instead of 'delete' make this for pdf generation
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # Delete the item in the database that matches the specified
    # id in the URL
    
    qry = db_session.query(speeders).filter(
        speeders.id==id)
    offence = qry.first()
    if offence:
        form = OffenceForm(formdata=request.form, obj=offence)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            # over here add the lines of code for passing details to html and generating pdf for ticket offence
            db_session.delete(offence)
            db_session.commit()
            flash('Album deleted successfully!')
            return redirect('/')
        return render_template('delete_album.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)
int:id
"""

if __name__=="__main__":
    db.create_all()
app.run(debug=True)