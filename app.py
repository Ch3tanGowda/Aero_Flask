from flask import Flask, app,render_template, request, flash, redirect
from sympy.core.sympify import sympify
from sympy.vector import CoordSys3D, divergence, curl
from flask_wtf import Form
from wtforms import StringField 
import codes.List as calc
import sympy
import math 
import os
import random
import string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas
import csv



app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config["CSV_UPLOADS"] = 'uploads/csv'
app.config["ALLOWED_CSV_EXTENSIONS"] = ["CSV"]
app.config["MAX_CSV_SIZE"] = 100*1024*1024

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
    return render_template ('reynolds.html', reynoldsnumbervalue = reynoldsnumbervalue, title = 'Reynolds Number')       

@app.route('/dynamicpressure.html', methods = ['POST', 'GET'])
def dynamicpressure():
    dynamicpressurevalue = ''
    if request.method == 'POST' and 'density' in request.form and 'velocity' in request.form:
        den = float (request.form.get('density'))
        vel = float (request.form.get('velocity'))
        dynamicpressurevalue = calc.dynamicpressure(den,vel)  
    return render_template ('dynamicpressure.html', dynamicpressurevalue = dynamicpressurevalue, title ='Dynamic Pressure')

@app.route('/dragcoefficient.html', methods = ['POST', 'GET'])
def dragcoefficient():
    dragcoefficientvalue = ''
    if request.method == 'POST' and 'dragforce' in request.form and 'dynamicpressure' in request.form and 'surfacearea' in request.form :
        dragforce = float (request.form.get('dragforce'))
        dynamicpressure = float (request.form.get('dynamicpressure'))
        surfacearea = float (request.form.get('surfacearea'))
        dragcoefficientvalue = calc.dragcoefficient(dragforce,dynamicpressure,surfacearea)    
    return render_template ('dragcoefficient.html', dragcoefficientvalue = dragcoefficientvalue, title = 'Drag Coefficient')  

@app.route('/liftcoefficient.html', methods = ['POST', 'GET'])
def liftcoefficient():
    liftcoefficientvalue = ''
    if request.method == 'POST' and 'liftforce' in request.form and 'dynamicpressure' in request.form and 'surfacearea' in request.form :
        liftforce = float (request.form.get('liftforce'))
        dynamicpressure = float (request.form.get('dynamicpressure'))
        surfacearea = float (request.form.get('surfacearea'))
        liftcoefficientvalue = calc.liftcoefficient(liftforce,dynamicpressure,surfacearea)    
    return render_template ('liftcoefficient.html', liftcoefficientvalue = liftcoefficientvalue, title = 'Lift Coefficient')  

@app.route('/normalforcecoefficient.html', methods = ['POST', 'GET'])
def normalforcecoefficient():
    normalforcecoefficientvalue = ''
    if request.method == 'POST' and 'normalforce' in request.form and 'dynamicpressure' in request.form and 'surfacearea' in request.form :
        normalforce = float (request.form.get('normalforce'))
        dynamicpressure = float (request.form.get('dynamicpressure'))
        surfacearea = float (request.form.get('surfacearea'))
        normalforcecoefficientvalue = calc.normalforcecoefficient(normalforce,dynamicpressure,surfacearea)    
    return render_template ('normalforcecoefficient.html', normalforcecoefficientvalue = normalforcecoefficientvalue, title = 'Normal Force Coefficient')  

@app.route('/axialforcecoefficient.html', methods = ['POST', 'GET'])
def axialforcecoefficient():
    axialforcecoefficientvalue = ''
    if request.method == 'POST' and 'axialforce' in request.form and 'dynamicpressure' in request.form and 'surfacearea' in request.form :
        axialforce = float (request.form.get('axialforce'))
        dynamicpressure = float (request.form.get('dynamicpressure'))
        surfacearea = float (request.form.get('surfacearea'))
        axialforcecoefficientvalue = calc.axialforcecoefficient(axialforce,dynamicpressure,surfacearea)    
    return render_template ('axialforcecoefficient.html', axialforcecoefficientvalue = axialforcecoefficientvalue, title = 'Axial Force Coefficient')  

@app.route('/momentcoefficient.html', methods = ['POST', 'GET'])
def momentforcecoefficient():
    momentcoefficientvalue = ''
    if request.method == 'POST' and 'moment' in request.form and 'dynamicpressure' in request.form and 'surfacearea' in request.form :
        moment = float (request.form.get('moment'))
        dynamicpressure = float (request.form.get('dynamicpressure'))
        surfacearea = float (request.form.get('surfacearea'))
        momentcoefficientvalue = calc.momentcoefficient(moment,dynamicpressure,surfacearea)    
    return render_template ('momentcoefficient.html', momentcoefficientvalue = momentcoefficientvalue, title = 'Moment Coefficient')  

@app.route('/liftdragfromnormalaxial.html', methods = ['POST', 'GET'])
def liftdragfromnormalaxial():
    lift = ''
    drag = ''
    if request.method == 'POST' and 'normalforce' in request.form and 'axialforce' in request.form and 'angleofattack' in request.form :
        normalforce = float (request.form.get('normalforce'))
        axialforce = float (request.form.get('axialforce'))
        angleofattack = float (request.form.get('angleofattack'))
        lift = calc.liftnormalaxial(normalforce,axialforce,angleofattack)  
        drag = calc.dragnormalaxial(normalforce,axialforce,angleofattack)
    return render_template ('liftdragfromnormalaxial.html', lift = lift, drag = drag, title = 'Lift and Drag force from Normal and Axial forces')


@app.route('/nad.html', methods = ['POST', 'GET'])
def normalaxialdistribution():
    x = sympy.Symbol('x')
    normal = sympy.Function('normal')
    axial = sympy.Function('axial')
    if request.method == 'POST' and 'pressure_upper' in request.form and 'pressure_lower' in request.form and 'tau_upper' in request.form and 'tau_lower' in request.form and 'y_upper' in request.form and 'y_lower' in request.form and 'leading_edge' in request.form and 'trailing_edge' in request.form :
        pressure_upper = (request.form.get('pressure_upper'))
        pressure_upper = sympy.parse_expr(pressure_upper)
        pressure_lower = (request.form.get('pressure_lower'))
        pressure_lower = sympy.parse_expr(pressure_lower)
        tau_upper = (request.form.get('tau_upper'))
        tau_upper = sympy.parse_expr(tau_upper)
        tau_lower = (request.form.get('tau_lower'))
        tau_lower = sympy.parse_expr(tau_lower)
        y_upper = (request.form.get('y_upper'))
        y_upper = sympy.parse_expr(y_upper)
        theta_upper = calc.differentiate(y_upper,x)
        y_lower = (request.form.get('y_lower'))
        y_lower = sympy.parse_expr(y_lower)
        theta_lower = calc.differentiate(y_lower,x)
        leading_edge = float(request.form.get('leading_edge'))
        trailing_edge = float(request.form.get('trailing_edge'))
        
        normal = calc.normalusingdistribution(pressure_upper,pressure_lower,tau_upper,tau_lower,theta_upper,theta_lower,leading_edge,trailing_edge,x)
        axial = calc.axialusingdistribution(pressure_upper,pressure_lower,tau_upper,tau_lower,theta_upper,theta_lower,leading_edge,trailing_edge,x)
    return render_template ('nad.html', normal = normal, axial = axial, title = '')

@app.route('/liftdragfromnormalaxialcoeff.html', methods = ['POST', 'GET'])
def axialforcecoefficientcoeff():
    liftcoeff = ''
    dragcoeff = ''
    if request.method == 'POST' and 'normalcoeff' in request.form and 'axialcoeff' in request.form and 'angle_of_attack' in request.form :
        normalcoeff = float (request.form.get('normalcoeff'))
        axialcoeff = float (request.form.get('axialcoeff'))
        angle_of_attack = float (request.form.get('angle_of_attack'))
        liftcoeff = calc.coeff_lift_calc(normalcoeff,axialcoeff,angle_of_attack)    
        dragcoeff = calc.coeff_drag_calc(normalcoeff,axialcoeff,angle_of_attack)  
    return render_template ('liftdragfromnormalaxialcoeff.html', liftcoeff = liftcoeff , dragcoeff = dragcoeff, title = 'Lift and Drag from Normal and Axial force Coefficients')  

@app.route('/centerpressurefromle.html', methods = ['POST', 'GET'])
def centereofpressurecalc():
    cop = ''
    if request.method == 'POST' and 'moment_le' in request.form and 'normalforce' in request.form:
        moment_le = float (request.form.get('moment_le'))
        normalforce = float (request.form.get('normalforce'))
        cop = calc.centre_pressure_calc(moment_le,normalforce)  
    return render_template ('centerpressurefromle.html', cop = cop, title = 'Location of Center of Presuure') 

@app.route('/stallvelocity.html', methods = ['POST', 'GET'])
def stallvelocitycalc():
    stall_velocity = ''
    if request.method == 'POST' and 'coeff_lift_max' in request.form and 'weight' in request.form and 'area' in request.form and 'density_inf' in request.form:
        coeff_lift_max = float (request.form.get('coeff_lift_max'))
        weight = float (request.form.get('weight'))
        area = float (request.form.get('area'))
        density_inf = float (request.form.get('density_inf'))
        stall_velocity = calc.stall_velocity_calc(coeff_lift_max,weight,area,density_inf)    
    return render_template ('stallvelocity.html', stall_velocity = stall_velocity, title = 'Stalling Velocity')    

@app.route('/dragduringsteadyflight.html', methods = ['POST', 'GET'])
def dragduringsteadyflight():
    coeff_drag= ''
    if request.method == 'POST' and 'velocity_inf' in request.form and 'thrust' in request.form and 'area' in request.form and 'density_inf' in request.form:
        velocity_inf = float (request.form.get('velocity_inf'))
        thrust = float (request.form.get('thrust'))
        area = float (request.form.get('area'))
        density_inf = float (request.form.get('density_inf'))
        coeff_drag = calc.coeff_drag_calc(velocity_inf,thrust,area,density_inf) 
    return render_template ('dragduringsteadyflight.html', coeff_drag = coeff_drag, title = 'Drag during Steady Flight')  
    
@app.route('/pressureunderliquid.html', methods = ['POST', 'GET'])
def pressureunderliquid():
    shearstress= ''
    if request.method == 'POST' and 'pressure_atmospheric' in request.form and 'density' in request.form and 'depth' in request.form and 'acceleration_gravity' in request.form:
        pressure_atmospheric = float (request.form.get('pressure_atmospheric'))
        density = float (request.form.get('density'))
        depth = float (request.form.get('depth'))
        acceleration_gravity = float (request.form.get('acceleration_gravity'))
        shearstress = calc.pressure_at_depth_calc(pressure_atmospheric,density,depth,acceleration_gravity) 
    return render_template ('pressureunderliquid.html', shearstress = shearstress, title = 'Pressure under Liquid')  

@app.route('/shearstressvisc.html', methods = ['POST', 'GET'])
def shearstressvisc():  
    while True:
        try:    
            y = sympy.Symbol('y')
            shearstresscalc = sympy.Function ('shearstresscalc')
            shearstress = ('')
            if request.method == 'POST' and 'viscosity_coeff' in request.form and 'velocity_profile' in request.form and 'y_calculated' in request.form:
                viscosity_coeff = float (request.form.get('viscosity_coeff'))
                velocity_profile = (request.form.get('velocity_profile'))
                velocity_profile = sympy.parse_expr(velocity_profile)
                y_calculated = float (request.form.get('y_calculated'))
                shearstresscalc = calc.shearstressviscosity(viscosity_coeff,velocity_profile,y)
                shearstress = shearstresscalc.subs(y,y_calculated)
            return render_template ('shearstressvisc.html', shearstress = shearstress, title = '')
        except (SyntaxError):
            return  render_template ('shearstressvisc.html', shearstress = "[ERROR: ENTER PROPER INPUT]", title = 'Shear Stress')
        break

@app.route('/velocityeuler.html', methods = ['POST', 'GET'])
def VelocityEuler():
    velocity2= ''
    if request.method == 'POST' and 'density' in request.form and 'gravity' in request.form and 'pressure1' in request.form and 'pressure2' in request.form and 'velocity1' in request.form and 'height1' in request.form and 'height2' in request.form:
        density = float (request.form.get('density'))
        gravity = float (request.form.get('gravity'))
        pressure1 = float (request.form.get('pressure1'))
        pressure2 = float (request.form.get('pressure2'))
        velocity1 = float (request.form.get('velocity1'))
        height1 = float (request.form.get('height1'))
        height2 = float (request.form.get('height2'))
        velocity2 = calc.velocity_from_euler(density,gravity,pressure1,pressure2,velocity1,height1,height2) 
    return render_template ('velocityeuler.html', velocity2 = velocity2, title = 'Velocity at a point (Bernoulli Principle)')

@app.route('/pressureeuler.html', methods = ['POST', 'GET'])
def PressureEuler():
    pressure2= ''
    if request.method == 'POST' and 'density' in request.form and 'gravity' in request.form and 'pressure1' in request.form and 'velocity1' in request.form and 'velocity2' in request.form and 'height1' in request.form and 'height2' in request.form:
        density = float (request.form.get('density'))
        gravity = float (request.form.get('gravity'))
        pressure1 = float (request.form.get('pressure1'))
        velocity1 = float (request.form.get('velocity1'))
        velocity2 = float (request.form.get('velocity2'))
        height1 = float (request.form.get('height1'))
        height2 = float (request.form.get('height2'))
        pressure2 = calc.velocity_from_euler(density,gravity,pressure1,velocity1,velocity2,height1,height2) 
    return render_template ('pressureeuler.html', pressure2 = pressure2, title = 'Pressure at a point (Bernoulli Principle)')

@app.route('/velocityfromcontinuity.html', methods = ['POST', 'GET'])
def velocityfromcontinuity():
    velocity2= ''
    if request.method == 'POST' and 'velocity1' in request.form and 'area1' in request.form and 'density1' in request.form  and 'area2' in request.form and 'density2' in request.form:
        velocity1 = float (request.form.get('velocity1'))
        area1 = float (request.form.get('area1'))
        density1 = float (request.form.get('density1'))
        area2 = float (request.form.get('area2'))
        density2 = float (request.form.get('density2'))
        velocity2 = calc.velocity_from_continuity(velocity1,area1,density1,area2,density2) 
    return render_template ('velocityfromcontinuity.html', velocity2 = velocity2, title = 'Velocity at a point from Continuity')  

@app.route('/velocityfrompressurecontinuity.html', methods = ['POST', 'GET'])
def velocityfrompressurecontinuity():
    velocity2= ''
    if request.method == 'POST' and 'density' in request.form and 'area1' in request.form and 'pressure1' in request.form and 'area2' in request.form and 'pressure2' in request.form:
        density = float (request.form.get('density'))
        area1 = float (request.form.get('area1'))
        pressure1 = float (request.form.get('pressure1'))
        area2 = float (request.form.get('area2'))
        pressure2 = float (request.form.get('pressure2'))
        velocity2 = calc.velocity_from_pressure_continuity(density,area1,pressure1,area2,pressure2) 
    return render_template ('velocityfrompressurecontinuity.html', velocity2 = velocity2, title = 'Velocity at a point from Continuity (Pressure Method)')  

@app.route('/cpfromvelocity.html', methods = ['POST', 'GET'])
def cpfromvelocity():
    cp = ''
    if request.method == 'POST' and 'velocity' in request.form and 'velocityinf' in request.form:
        vel = float (request.form.get('velocity'))
        velinf = float (request.form.get('velocityinf'))
        cp = calc.cp_from_velocity(vel,velinf)  
    return render_template ('cpfromvelocity.html', cp = cp, title = 'Center of Pressure from Velocity') 

@app.route('/divergencetest.html', methods = ['POST', 'GET'])
def divergencetest():
    divergence= ''
    if request.method == 'POST' and 'velocityfield' in request.form :
        velocityfield = (request.form.get('velocityfield'))
        velocityfield = sympy.parse_expr(velocityfield)
        divergence = calc.divergence(velocityfield) 
    return render_template ('divergencetest.html', divergence = divergence, title = 'Divergence Test')  

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_CSV_EXTENSIONS

@app.route('/div3d.html', methods = ['POST', 'GET'])
def div3d():
    data1 = ''
    data2 = ''
    data3 = ''
    data4 = ''
    data5 = ''
    data6 = ''
    div = ''
    if request.method == 'POST' and 'xlen' in request.form and 'ylen' in request.form and 'zlen' in request.form and 'file' in request.files:
        file = request.files["file"]
        xlen = int(request.form.get('xlen'))
        ylen = int(request.form.get('ylen'))
        zlen = int(request.form.get('zlen'))
        data1, data2, data3, data4, data5, data6, divarr = calc.divergence3d(file,xlen,ylen,zlen)
        div = 0
        for k in range (1,xlen-1):
            for j in range (1,ylen-1):
                for i in range (1,zlen-1):
                    div = div + divarr[i][j][k]
    return render_template ('div3d.html', data1 = data1, data2 = data2, data3 = data3, data4 = data4, data5 = data5, data6 = data6, div = div, title = 'Divergence in a 3D flow')

@app.route('/div2d.html', methods = ['POST', 'GET'])
def div2d():
    divarr = ''
    data = ''
    img = ''
    if request.method == 'POST' and 'xlen' in request.form and 'ylen' in request.form and 'file' in request.files:
        file = request.files["file"]
        xlen = int(request.form.get('xlen'))
        ylen = int(request.form.get('ylen'))
        data,divarr,img = calc.divergence2d(xlen,ylen,file)
        div = 0
        for k in range (1,xlen-1):
            for j in range (1,ylen-1):
                    div = div + divarr[j][k]
    

    return render_template ('div2d.html',img = img, title = 'Divergence in a 2D flow',div = div)

@app.route('/curl2d.html', methods = ['POST', 'GET'])
def curl2d():
    data = ''
    img = ''
    curl = ''
    if request.method == 'POST' and 'xlen' in request.form and 'ylen' in request.form and 'file' in request.files:
        file = request.files["file"]
        xlen = int(request.form.get('xlen'))
        ylen = int(request.form.get('ylen'))
        data,curlarr,img = calc.curl2d(xlen,ylen,file)
        curl = 0

        for j in range (1,xlen-1):
            for i in range (1,ylen-1):
                curl = curl + curlarr[i][j]
    
    return render_template ('curl2d.html',img = img, title = 'Curl in a 2D flow',curl = curl)

@app.route('/curl3d.html', methods = ['POST', 'GET'])
def curl3d():
    data1 = ''
    data2 = ''
    data3 = ''
    data4 = ''
    data5 = ''
    data6 = ''
    div = ''
    if request.method == 'POST' and 'xlen' in request.form and 'ylen' in request.form and 'zlen' in request.form and 'file' in request.files:
        file = request.files["file"]
        xlen = int(request.form.get('xlen'))
        ylen = int(request.form.get('ylen'))
        zlen = int(request.form.get('zlen'))
        data1, data2, data3, data4, data5, data6, curlarr = calc.curl3d(file,xlen,ylen,zlen)
        div = 0
        for k in range (1,xlen-1):
            for j in range (1,ylen-1):
                for i in range (1,zlen-1):
                    curl = curl + curl[i][j][k]
    return render_template ('curl3d.html', data1 = data1, data2 = data2, data3 = data3, data4 = data4, data5 = data5, data6 = data6, div = div, title = 'Curl in a 3D flow')

@app.errorhandler(404)
def page_not_found(e):
    return  render_template ('404.html')

##@app.errorhandler(Exception)
##def handle_exception(e):
##    return render_template("500.html", e=e), 500


if __name__ == "__main__":
    app.run(debug=True)
    