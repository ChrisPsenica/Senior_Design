# Senior Desing AOA Script
# Chris Psenica
# This script is to determine the flow field needed to fly at a specified AOA as well as adjust the direction for CL and CD

#---------- Imports ----------
import numpy as np

#---------- Parameters ----------
aoa0 = 5.0   # Desired AOA to fly at in degrees
U0 = 15.433  # Cruise velocity in m/s

#---------- AOA Function ----------
aoa = aoa0 * (np.pi / 180.0)
U = [0.0 , float(U0 * np.sin(aoa)) , float(-U0 * np.cos(aoa))]

#---------- CD Function ----------
magCD = 1.0
CD = [0.0 , float(U0 * np.sin(aoa)) / U0 , float(-U0 * np.cos(aoa)) / U0]

#---------- CL Function ----------
magCL = 1.0
CL = [0.0 , float(U0 * np.cos(aoa)) / U0 , float(U0 * np.sin(aoa)) / U0]

#---------- Print Results ----------
print()
print("The flow field for the desired AOA is: ")
print(U)
print()
print("The unit vector for the desired CD direction is: ")
print(CD)
print()
print("The unit vector for the desired CL direction is: ")
print(CL)
print()










































