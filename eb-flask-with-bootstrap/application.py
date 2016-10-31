from flask import Flask, render_template
FileName = "mySite.html"#change to your file name
def mySite():
    return render_template(FileName)
application = Flask(__name__)
application.add_url_rule('/', 'index', mySite)
# runs the app.
def boots():
    return render_template('ContainerTemplateTest.html')

def BootStrap():
    return render_template('BootstrapTutorial.html')
application.add_url_rule('/bootstrap', 'boots', BootStrap)


if __name__ == "__main__":
    application.run()