from flask import Flask, render_template, request, flash
from Forms.POAForms import MakeTripFormPOA

app = Flask(__name__)
app.secret_key = 'development key'

from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app
@app.route('/', methods=['GET', 'POST'])
def contact():
    form = MakeTripFormPOA()
    if request.method == 'POST':
        print(form.data)#returns a dictonary with keys that are the feilds in the table
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('FormTest.html', form=form)
        else:
            return "Form Submited Yay!"
    elif request.method == 'GET':

        return render_template('FormTest.html', form=form)


if __name__ == '__main__':
    create_app()
    app.run(debug=True)