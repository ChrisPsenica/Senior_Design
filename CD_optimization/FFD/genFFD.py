#Chris Psenica
#Senior Design FFD Point Generation Script
#01/18/2024

#--------------- Imports ---------------
import numpy as np
import sys
import os

#--------------- Parameters ---------------
x , y , z = [] , [] , []   # Initiate matrices to store all x , y , and z coordinates
Offset = 0.003             # All FFD points will be this distance from the surface of the body

#--------------- FFD Points (Top) ---------------
x.append(0 + Offset)
y.append(0.05 + Offset)
z.append(0 + Offset)

s = 1
for i in range(8):
    x.append(0 + Offset)
    y.append(0.05 + Offset)
    z.append(z[0] - (0.09 * s))
    
    s = s + 1

s = 0
for i in range(len(x)):
    x.append(x[s] - (2 * Offset) - 0.08)
    y.append(y[s])
    z.append(z[s])

    s = s + 1

#--------------- FFD Points (Bottom) ---------------
x.append(0 + Offset)
y.append(-0.075 - Offset)
z.append(0 + Offset)

s = 1
for i in range(8):
    x.append(0 + Offset)
    y.append(-0.075 - Offset)
    z.append(z[0] - (0.09 * s))
    
    s = s + 1

s = 0
for i in range(9):
    x.append(x[s] - (2 * Offset) - 0.08)
    y.append(-0.075 - Offset)
    z.append(z[s])

    s = s + 1

#--------------- Write MAPDL Code For Keypoints (For Testing Purposes Only) ---------------
os.remove("MAPDL_BodyFFD.txt")
f = open("MAPDL_BodyFFD.txt" , 'a')
b = 1
f.write('/cle')
f.write('\n')
f.write('/prep7')
f.write('\n')

for i in range (len(x)):
    f.write('k,')
    f.write(str(b))
    f.write(',')
    f.write(str(x[i]))
    f.write(',')
    f.write(str(y[i]))
    f.write(',')
    f.write(str(z[i]))
    f.write('\n')
    b = b + 1

f.close()


#--------------- Write Points To .xyz File ---------------
os.remove("BodyFFD.xyz")
f = open("BodyFFD.xyz",'a')

f.write('           1')
f.write('\n')
f.write('           9           2           2')
f.write('\n')

for i in range (len(x)): 

    f.write(str(x[i]))
    f.write(' ')
  

f.write('\n')

for i in range (len(x)):

    f.write(str(y[i]))
    f.write(' ')

f.write('\n')

for i in range (len(x)):

    f.write(str(z[i]))
    f.write(' ')


f.close()
