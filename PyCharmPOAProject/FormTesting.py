from flask import Flask, render_template, request, flash, redirect, url_for
from Forms.POAForms import MakeTripFormPOA

from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.secret_key = 'development key'





@app.route('/', methods=['GET', 'POST'])
def add_Trip():
    db = get_db()
    form = MakeTripFormPOA()
    if request.method == 'POST':
        # print(form.data)  # returns a dictonary with keys that are the feilds in the table
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('POA_Add_Trip.html', form=form)
        else:
            AddTrip(form.data, db)
            flash('New entry was successfully posted')
            return redirect(url_for('show_entries'))
    elif request.method == 'GET':
        return render_template('POA_Add_Trip.html', form=form)


if __name__ == '__main__':
    Bootstrap(app)
    app.run()
    app.run(debug=True)