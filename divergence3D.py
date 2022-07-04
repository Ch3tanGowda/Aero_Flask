import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pprint
import pandas as pd

xlen = 3
ylen = 3
zlen = 3

data = np.genfromtxt('Divergence3d.csv', delimiter = ',')
print (data)

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
            print(arr)
            print()


for k in range (1,xlen-1):
    for j in range (1,ylen-1):
        for i in range (1,zlen-1):
            print(arr[i][j+1][2])
            print(arr[i][j-1][2])
            print(arr[i][j+1][0])
            print(arr[i][j-1][0])
            divarr[i][j][k] = ((arr[i][j][k+1][5]-arr[i][j][k-1][5])/(arr[i][j][k+1][2]-arr[i][j][k-1][2])+(arr[i][j+1][k][4]-arr[i][j-1][k][4])/(arr[i][j+1][k][1]-arr[i][j-1][k][1])+(arr[i+1][j][k][3]-arr[i-1][j][k][3])/(arr[i+1][j][k][0]-arr[i-1][j][k][0]))

print (divarr)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(data[:,0],data[:,1],data[:,2],data[:,3],data[:,4],data[:,5],length= 0.3,arrow_length_ratio=0.5)
plt.show()



print(list(data[:,0]))



