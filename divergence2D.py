import csv
import numpy as np
import os
import matplotlib.pyplot as plt


rowsmat = 3
columnsmat = 3
data = np.genfromtxt('Divergence2d.csv', delimiter = ',')

arr=[]
for i in range(columnsmat):
    col = []
    for j in range(rowsmat):
        col.append(0)
    arr.append(col)

print(arr)
print()
divarr=[]
for i in range(columnsmat):
    col = []
    for j in range(rowsmat):
        col.append(0)
    divarr.append(col)
print(divarr)
print()

k=0
for i in range (rowsmat):
    for j in range (columnsmat):
        arr[j][i]= data[k]
        k=k+1
print(arr)
print()



for j in range (1,rowsmat-1):
    for i in range (1,columnsmat-1):
        print(arr[i][j+1][2])
        print(arr[i][j-1][2])
        print(arr[i][j+1][0])
        print(arr[i][j-1][0])
        divarr[i][j] = ((arr[i][j+1][3]-arr[i][j-1][3])/(arr[i][j+1][1]-arr[i][j-1][1])+(arr[i+1][j][2]-arr[i-1][j][2])/(arr[i+1][j][0]-arr[i-1][j][0]))

print (divarr)
x = "Python"
y =  x + ".png"

plt.quiver(data[:,0],data[:,1],data[:,2],data[:,3])
plt.savefig(y)

