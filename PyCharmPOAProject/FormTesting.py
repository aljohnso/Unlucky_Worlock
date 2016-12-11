from flask import Flask, render_template, request, flash
from Forms.MakeTripForm import MakeTripForm

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def contact():
    print("in contact")
    form = MakeTripForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('FormTest.html', form=form)
        else:
            return "Form Submited Yay!"
    elif request.method == 'GET':
        print(form)
        return render_template('FormTest.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)