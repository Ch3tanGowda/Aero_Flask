import math #Importing the math library
import sympy
import sympy.vector as symvec
from sympy.vector import CoordSys3D, divergence, curl
import csv
import numpy as np
import matplotlib.pyplot as plt
import pprint
import pandas as pd
import os
import string
import random
import base64

def differentiate(y,x):
    diff = sympy.diff(y,x)
    return (diff)
    
def dynamicpressure(densityinf,velocityinf): 
    dynamicpressure= ((0.5)*(densityinf)*(velocityinf**2)) 
    return (dynamicpressure)

def dragcoefficient(dragforce,dynamicpressure,surfacearea):
    dragcoefficient=(dragforce/(dynamicpressure*surfacearea))  
    return (dragcoefficient)

def liftcoefficient(liftforce,dynamicpressure,surfacearea):
    liftcoefficient=(liftforce/(dynamicpressure*surfacearea))  
    return (liftcoefficient)
    
def normalforcecoefficient(normalforce,dynamicpressure,surfacearea):
    normalforcecoefficient=(normalforce/(dynamicpressure*surfacearea))  
    return (normalforcecoefficient)

def axialforcecoefficient(axialforce,dynamicpressure,surfacearea):
    axialforcecoefficient=(axialforce/(dynamicpressure*surfacearea))  
    return (axialforcecoefficient)

def momentcoefficient(moment,dynamicpressure,surfacearea):
    momentcoefficient=(moment/(dynamicpressure*surfacearea))  
    return (momentcoefficient)

def reynoldsnumber(velocity,density,linear,viscosity):
    rn =  ((density*velocity*linear)/(viscosity))
    return(rn)

def liftnormalaxial(normal_force,axial_force,angle_of_attack): 
    lift=((normal_force*(math.cos(math.radians(angle_of_attack))))-(axial_force*(math.sin(math.radians(angle_of_attack))))) 
    return(lift)

def dragnormalaxial(normal_force,axial_force,angle_of_attack):
    drag=((normal_force*(math.sin(math.radians(angle_of_attack))))+(axial_force*(math.cos(math.radians(angle_of_attack))))) 
    return(drag)

def normalusingdistribution(pressure_upper,pressure_lower,tau_upper,tau_lower,theta_upper,theta_lower,leading_edge,trailing_edge,x):
    normal_1 = sympy.Function('normal_1')
    normal_2 = sympy.Function('normal_2')
    normal_1 = (-1*(pressure_upper * sympy.cos((theta_upper*math.pi/180)) + tau_upper * sympy.sin((theta_upper*math.pi/180)))) 
    normal_2 = ((pressure_lower * sympy.cos((theta_upper*math.pi/180)) - (tau_lower * sympy.sin((theta_lower*math.pi/180)))))
    normal = sympy.integrate(normal_1,(x,leading_edge,trailing_edge)) + sympy.integrate(normal_2,(x,leading_edge,trailing_edge))
    return (normal)

def axialusingdistribution(pressure_upper,pressure_lower,tau_upper,tau_lower,theta_upper,theta_lower,leading_edge,trailing_edge,x):
    axial_1 = sympy.Function('axial_1')
    axial_2 = sympy.Function('axial_2')
    axial_1 = ((-1 * pressure_upper * sympy.sin(theta_upper*math.pi/180)) + (tau_upper * sympy.cos(theta_upper*math.pi/180)))
    axial_2 = ((pressure_lower * sympy.sin(theta_lower*math.pi/180)) + (tau_lower * sympy.cos(theta_lower*math.pi/180)))
    axial = sympy.integrate(axial_1,(x,leading_edge,trailing_edge)) + sympy.integrate(axial_2,(x,leading_edge,trailing_edge))
    return (axial)

def coeff_lift_calc(coeff_normal_force,coeff_axial_force,angle_of_attack): #Defining the Function which would calculate coefficient of lift
    coeff_lift = ((coeff_normal_force*(math.cos(math.radians(angle_of_attack))))-(coeff_axial_force*(math.sin(math.radians(angle_of_attack))))) #Calculating the value of coefficient of lift
    return(coeff_lift)

def coeff_drag_calc(coeff_normal_force,coeff_axial_force,angle_of_attack): #Defining the Function which would calculate coefficient of drag
    coeff_drag = ((coeff_normal_force*(math.sin(math.radians(angle_of_attack))))+(coeff_axial_force*(math.cos(math.radians(angle_of_attack))))) #Calculating the value of coefficient of drag
    return(coeff_drag)
    
def centre_pressure_calc(moment_le,normal_force): #Defining the Function which would calculate the positon of the x-cordinate of center of pressure
    center_pressure = (moment_le/normal_force)
    return(center_pressure)

def stall_velocity_calc(coeff_lift_max,weight,area,density_inf): #Defining the Function which would calculate the Stall velocity
    stall_velocity = math.sqrt((2*weight)/(density_inf*area*coeff_lift_max)) #Calculating the Stall velocity
    return(stall_velocity)

def coeff_drag_calc(velocity_inf,thrust,area,density_inf): #Defining the Function which would calculate Coefficient of drag during steady flight.
    coeff_drag = math.sqrt((2*thrust)/(density_inf*area*(velocity_inf**2))) #Calculating the Coefficient of drag
    return(coeff_drag)

def pressure_at_depth_calc(pressure_atmospheric,density,depth,gravity): #Defining the Function which would calculate pressure at some depth from the surface
    pressure_at_depth = pressure_atmospheric + (density*gravity*depth) #Calculating the velocity
    return(pressure_at_depth)

def shearstressviscosity(viscosity_coeff,velocity_profile,y):
    while True:
        try:
            shear_stress = sympy.Function('shear_stress')
            shear_stress = viscosity_coeff*(sympy.diff(velocity_profile,y))
            return (shear_stress)
            break
        except ValueError:
            return ('Enter valid Input')

def velocity_from_euler(density,gravity,pressure1,pressure2,velocity1,height1,height2):
    velocity2 = math.sqrt((2*((gravity*(height1-height2))+((pressure1-pressure2)/density)))-(velocity1**2))
    return(velocity2)

def pressure_from_euler(density,gravity,pressure1,velocity1,velocity2,height1,height2):
    pressure2 = (pressure1+(density*gravity*(height1-height2))+(0.5*(velocity1**2 - velocity2**2)))
    return(pressure2)

def velocity_from_continuity(velocity1,area1,density1,area2,density2):
    velocity2 = (velocity1*density1*area1)/(density2*area2)
    return(velocity2)

def velocity_from_pressure_continuity(density,area1,pressure1,area2,pressure2):
    velocity2 = math.sqrt((2*(pressure1-pressure2))/(density*(1-((area2/area1)**2))))
    return(velocity2)

def cp_from_velocity(velocity,velocityinf):
    cp = (1-((velocity/velocityinf)**2))
    return(cp)

def divergence(symbol1):
    div = divergence(symbol1)
    return(div)

def divergence3d (file,xlen,ylen,zlen):
    data = np.genfromtxt(file, delimiter = ',')

    arr=[]
    for i in range(zlen):
        col = []
        for j in range(ylen):
            row = []
            for k in range(xlen):
                row.append(0)
            col.append(row)
        arr.append(col)

    divarr =  np.zeros((zlen,ylen,xlen))

    p=0
    for i in range (xlen):
        for j in range (ylen):
            for k in range (zlen):
                arr[k][j][i]= data[p]
                p=p+1



    for k in range (1,xlen-1):
        for j in range (1,ylen-1):
            for i in range (1,zlen-1):
                divarr[i][j][k] = ((arr[i][j][k+1][5]-arr[i][j][k-1][5])/(arr[i][j][k+1][2]-arr[i][j][k-1][2])+(arr[i][j+1][k][4]-arr[i][j-1][k][4])/(arr[i][j+1][k][1]-arr[i][j-1][k][1])+(arr[i+1][j][k][3]-arr[i-1][j][k][3])/(arr[i+1][j][k][0]-arr[i-1][j][k][0]))



    data0 = (list(data[:,0]))
    data1 = (list(data[:,1]))
    data2 = (list(data[:,2]))
    data3 = (list(data[:,3]))
    data4 = (list(data[:,4]))
    data5 = (list(data[:,5]))
 
    return (data0,data1,data2,data3,data4,data5,divarr)

def divergence2d (rowsmat,columnsmat,file):
    data = np.genfromtxt(file, delimiter = ',')

    arr=[]
    for i in range(columnsmat):
        col = []
        for j in range(rowsmat):
            col.append(0)
        arr.append(col)

    divarr=[]
    for i in range(columnsmat):
        col = []
        for j in range(rowsmat):
            col.append(0)
        divarr.append(col)


    k=0
    for i in range (rowsmat):
        for j in range (columnsmat):
            arr[j][i]= data[k]
            k=k+1


    for j in range (1,rowsmat-1):
        for i in range (1,columnsmat-1):
            divarr[i][j] = ((arr[i][j+1][3]-arr[i][j-1][3])/(arr[i][j+1][1]-arr[i][j-1][1])+(arr[i+1][j][2]-arr[i-1][j][2])/(arr[i+1][j][0]-arr[i-1][j][0]))

    x = ''.join(random.choices(string.ascii_uppercase, k = 5))
    y =  x + ".png"

    plt.quiver(data[:,0],data[:,1],data[:,2],data[:,3])
    plt.savefig(y)
    


    with open(y, "rb") as img_file:
        img = str(base64.b64encode(img_file.read()))
        img = img[2:]
        img = img[:-1]

    #os.remove(y)
    return (data,divarr,img)

def curl2d (rowsmat,columnsmat,file):
    data = np.genfromtxt(file, delimiter = ',')

    arr=[]
    for i in range(columnsmat):
        col = []
        for j in range(rowsmat):
            col.append(0)
        arr.append(col)


    curlarr=[]
    for i in range(columnsmat):
        col = []
        for j in range(rowsmat):
            col.append(0)
        curlarr.append(col)


    k=0
    for i in range (rowsmat):
        for j in range (columnsmat):
            arr[j][i]= data[k]
            k=k+1
    

    for j in range (1,rowsmat-1):
        for i in range (1,columnsmat-1):
            curlarr[i][j] = ((arr[i+1][j][3]-arr[i-1][j][3])/(arr[i+1][j][0]-arr[i-1][j][0])-(arr[i][j+1][2]-arr[i][j-1][2])/(arr[i][j+1][1]-arr[i][j-1][1]))

    x1 = ''.join(random.choices(string.ascii_uppercase, k = 5))
    y1 =  x1 + ".png"

    plt.quiver(data[:,0],data[:,1],data[:,2],data[:,3])
    plt.savefig(y1)
    

    with open(y1, "rb") as img_file:
        img1 = str(base64.b64encode(img_file.read()))
        img1 = img1[2:]
        img1 = img1[:-1]

 
   
    os.remove(y1)
    
    data0 = (list(data[:,0]))
    data1 = (list(data[:,1]))
    data2 = (list(data[:,2]))
    data3 = (list(data[:,3]))

    return (data,curlarr,img1)

def curl3d (file,xlen,ylen,zlen):
    data = np.genfromtxt(file, delimiter = ',')
    arr=[]
    for i in range(zlen):
        col = []
        for j in range(ylen):
            row = []
            for k in range(xlen):
                row.append(0)
            col.append(row)
        arr.append(col)

    curlarr=[]
    for i in range(zlen):
        col = []
        for j in range(ylen):
            row = []
            for k in range(xlen):
                row.append(0)
            col.append(row)
        curlarr.append(col)

    p=0
    for i in range (xlen):
        for j in range (ylen):
            for k in range (zlen):
                arr[k][j][i]= data[p]
                p=p+1
                print(arr)
                print()


    for k in range (1,xlen-1):
        for j in range (1,ylen-1):
            for i in range (1,zlen-1):
                curlarr[i][j][k] = ([(arr[i][j+1][k][5]-arr[i][j-1][k][5])/(arr[i][j+1][k][1]-arr[i][j-1][k][1])-(arr[i][j][k+1][4]-arr[i][j][k-1][4])/(arr[i][j][k+1][2]-arr[i][j][k-1][2])],[(arr[i][j][k+1][3]-arr[i][j][k-1][3])/(arr[i][j][k+1][2]-arr[i][j][k-1][2])-(arr[i+1][j][k][5]-arr[i-1][j][k][5])/(arr[i+1][j][k][0]-arr[i-1][j][k][0])],[(arr[i+1][j][k][4]-arr[i-1][j][k][4])/(arr[i+1][j][k][0]-arr[i-1][j][k][0])-(arr[i][j+1][k][3]-arr[i][j-1][k][3])/(arr[i][j+1][k][1]-arr[i][j-1][k][1])])



        data0 = (list(data[:,0]))
        data1 = (list(data[:,1]))
        data2 = (list(data[:,2]))
        data3 = (list(data[:,3]))
        data4 = (list(data[:,4]))
        data5 = (list(data[:,5]))
    
    return (data0,data1,data2,data3,data4,data5,curlarr)

