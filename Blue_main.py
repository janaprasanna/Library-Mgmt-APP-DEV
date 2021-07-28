from flask import Flask,render_template,redirect
from blue_sub import var
app = Flask(__name__)

app.register_blueprint(var, url_prefix="/admin")

'''route('/') is present on both the files, but the preferences goes to the sub file and not the main file.
Depending on the url prefix(in this case its blank "" ) the route perfoms.
eg url prefix='/admin' indicates that after this prefix only if any route matches with blueprint, it returns that value.'''
@app.route('/')
def home():
    return "<h3>Main file</h3>"



if __name__ == "__main__":
    app.run(debug=True)

    '''running the application from blue_main file but the content is in blue_sub file.'''