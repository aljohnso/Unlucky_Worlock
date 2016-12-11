from flask import Flask, render_template, request, flash
from Forms.POAForms import MakeTripFormPOA

app = Flask(__name__)
app.secret_key = 'development key'


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
    app.run(debug=True)