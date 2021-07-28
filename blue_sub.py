from flask import Blueprint,render_template

var = Blueprint("bl_var",__name__,template_folder="templates")

@var.route('/home')
@var.route('/')
def home():
    return "<h3> sub file </h3>"