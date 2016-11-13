from flask import Flask, render_template, request
from CaesarEncipher import encipher


application = Flask(__name__)# runs the app.

def mySite():
    return render_template("mySite.html")
application.add_url_rule('/', 'index', mySite)

def BootStrap():
    return render_template('BootstrapTutorial.html')#will render HTML file 
application.add_url_rule('/bootstrap', 'boots', BootStrap)

def registration():
    encodedMessage = ''#intial message 
    if request.method == 'POST':#when we get a post request do this
        encodedMessage = encipher(request.form['message'], int(request.form['key']))#encode the message with the encipher code
    return render_template('Forms.html',encodedMessage=encodedMessage)#send back up WHATEVER value we have for encodedMessage
application.add_url_rule('/form', 'forms', registration, methods=['GET','POST'])#server interactions

#http://stackoverflow.com/questions/19794695/flask-python-buttons
#http://stackoverflow.com/questions/33743658/flask-how-to-update-html-table-with-data-from-sqlite-on-homepage-after-data-are
List_of_Trips = {}
def POAMain():
    Trip = {}
    Person = {}
    return render_template('POACreateTrip.html')
application.add_url_rule('/POA', 'POA', POAMain, methods=['GET','POST'])    






def game():
    newpos = ["200","210",'220','230','240']
    posindex = 0
    if request.method == 'POST':
        pos = newpos[posindex]
        posindex += 1
        print(pos)
        return render_template('gameCanvas.html', testchange= newpos)
    else:
        return render_template('gameCanvas.html')
application.add_url_rule('/connect4', 'connect4',game, methods=['GET','POST'])



if __name__ == "__main__":
    application.debug = True#very helpful however take this out when you are publishing cause it makes your back end visible to the haxers 
    application.run()#make it do its thing