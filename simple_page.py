from types import MethodType
from flask import Flask, app,render_template, request
import codes.FA_01_Extra1 as calc

simple_page = Blueprint('simple_page',app, template_folder='templates')
@simple_page.route('/reynolds.html', methods = ['POST', 'GET'])
def calculate1():
    rn = ''
    if request.method == 'POST' and 'density' in request.form and 'velocity' in request.form and 'linear' in request.form and 'viscosity' in request.form:
        den = float (request.form.get('density'))
        vel = float (request.form.get('velocity'))
        lin = float (request.form.get('linear'))
        visc = float (request.form.get('viscosity'))
        rn = calc.reynoldsnumber(vel,den,lin,visc)
    return render_template ('reynolds.html', rn = rn)       

    