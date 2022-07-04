from flask import Flask, app,render_template, request, flash, redirect
from sympy.core.sympify import sympify
from sympy.vector import CoordSys3D, divergence, curl
from flask_wtf import Form
from wtforms import StringField 
import codes.List as calc
import sympy
import math 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/', methods = ['POST', 'GET'])

def home():
    return render_template ('index.html')

@app.route('/reynolds.html', methods = ['POST', 'GET'])
def reynoldsnumber():
    reynoldsnumbervalue = ''
    if request.method == 'POST' and 'density' in request.form and 'velocity' in request.form and 'linear' in request.form and 'viscosity' in request.form:
        den = float (request.form.get('density'))
        vel = float (request.form.get('velocity'))
        lin = float (request.form.get('linear'))
        visc = float (request.form.get('viscosity'))
        reynoldsnumbervalue = calc.reynoldsnumber(vel,den,lin,visc)    
    return render_template ('reynolds.html', reynoldsnumbervalue = reynoldsnumbervalue)       




@app.errorhandler(404)
def page_not_found(e):
    return  render_template ('404.html')

##@app.errorhandler(Exception)
##def handle_exception(e):
##    return render_template("500.html", e=e), 500



if __name__ == "__main__":
    app.run(debug=True)