import csv
import numpy as np
import matplotlib.pyplot as plt


rowsmat = 4
columnsmat = 6
data = np.genfromtxt('curl2d.csv', delimiter = ',')

arr=[]
for i in range(columnsmat):
    col = []
    for j in range(rowsmat):
        col.append(0)
    arr.append(col)

print(arr)
print()
curlarr=[]
for i in range(columnsmat):
    col = []
    for j in range(rowsmat):
        col.append(0)
    curlarr.append(col)
print(curlarr)
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
        print(i,j)
        curlarr[i][j] = ((arr[i+1][j][3]-arr[i-1][j][3])/(arr[i+1][j][0]-arr[i-1][j][0])-(arr[i][j+1][2]-arr[i][j-1][2])/(arr[i][j+1][1]-arr[i][j-1][1]))

print (curlarr)
print (data)


plt.quiver(data[:,0],data[:,1],data[:,2],data[:,3])
plt.show()


data1=[]
for i in range(columnsmat*rowsmat):
    col = []
    for j in range(3):
        col.append(0)
    data1.append(col)

for i in range(columnsmat*rowsmat):
    data1[i][0] = data[i][0]
    data1[i][1] = data[i][1]
print(data1)


for i in range (rowsmat):
    for j in range (columnsmat):
        data1[(columnsmat*i)+j][2] = curlarr[j][i]

print(data1)

fields = ['X-Coordinate', 'Y-Coordinate', 'Vorticity']
filename = "university_records.csv"
    
# writing to csv file 
with open(filename, 'w') as csvfile: 
 
    csvwriter = csv.writer(csvfile) 
        

    csvwriter.writerow(fields) 
        

    csvwriter.writerows(data1)