#AerE 461/462
#Plots of opt history
#Chris Psenica  
#For big daddi z

# =============================================================================
# Imports
# =============================================================================
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Matrices Of CL & CD For -> CL Optimization (17 Total Iterations Shown , 4 Majors)
# =============================================================================

#---------- Matrices ----------
CL_all = [-1.774303744852545606e-03,
      -1.774038393762111809e-03,
      -1.475036239327209842e-03,
      -1.474996185891086498e-03,
      -1.634246652145066037e-03,
      -1.557439302985130780e-03,
      -1.516897863965027682e-03,
      -1.479334230154449870e-03,
      -1.475122588345811891e-03,
      -1.774461175330088736e-03,
      -1.186175107875442336e-03,
      -1.186175144923140579e-03,
      -1.186175107463327549e-03,
      -1.475036774507998416e-03,
      -1.208101040447218111e-03,
      -1.232367972022530012e-03,
      -1.232367913090115508e-03]

CD_all = [1.393837033954525850e-02,
      1.393851098547571610e-02,
      1.399955905017691293e-02,
      1.399955084465887012e-02,
      1.396306545905190433e-02,
      1.397972484992493492e-02,
      1.398925872316425512e-02,
      1.399850418708581401e-02,
      1.399953628104100289e-02,
      1.393901095202920715e-02,
      1.403209550988293586e-02,
      1.403209560002949274e-02,
      1.403209550986872500e-02,
      1.399955850290979242e-02,
      1.401173854821280429e-02,
      1.400070706236533624e-02,
      1.400070695601840498e-02]

CL_major = [-1.774303744852545606e-03,
            -1.474996185891086498e-03,
            -1.186175107463327549e-03,
            -1.208101040447218111e-03,
            -1.232367913090115508e-03]

CD_major = [1.393837033954525850e-02,
            1.399955084465887012e-02,
            1.403209550986872500e-02,
            1.401173854821280429e-02,
            1.400070695601840498e-02]

Iterations_all = list(range(1,18))    # 17 iterations 
Iterations_major = list(range(1,6))   # 5 iterations

#---------- Plots ----------
plt.rcParams.update({'font.size' : 16})
plt.plot(Iterations_all , CD_all)    # CD plot for all iterations
plt.title("CD Total Iteration History" , fontsize=16)
plt.xlabel('Iterations' , fontsize=16)
plt.ylabel('Value Of CD' , fontsize=16)
plt.grid()
plt.show()

plt.rcParams.update({'font.size' : 16})
plt.plot(Iterations_all , CL_all)    # CL plot for all iterations
plt.title("CL Total Iteration History" , fontsize=16)
plt.xlabel('Iterations' , fontsize=16)
plt.ylabel('Value Of CL' , fontsize=16)
plt.grid()
plt.show()

plt.rcParams.update({'font.size' : 16})
plt.plot(Iterations_major , CD_major)    # CD plot for major iterations only
plt.title("CD Major Iteration History" , fontsize=16)
plt.xlabel('Iterations' , fontsize=16)
plt.ylabel('Value Of CD' , fontsize=16)
plt.grid()
plt.show()

plt.rcParams.update({'font.size' : 16})
plt.plot(Iterations_major , CL_major)    # CL plot for major iterations only
plt.title("CL Major Iteration History" , fontsize=16)
plt.xlabel('Iterations' , fontsize=16)
plt.ylabel('Value Of CL' , fontsize=16)
plt.grid()
plt.show()




























































































































