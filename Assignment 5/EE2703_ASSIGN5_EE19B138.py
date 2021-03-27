"""
************** Python program to visualise and analyse a given resistor configuration ************

In this code, a copper plate is visualised using the plotting commands. Also the potential, current density and temperature 
profiles are found using the Laplace equation and the error is analysed as a function of iteration number.

Done by: V. Ruban Vishnu Pandian 
Date of completion: 27/03/2021

Command line usage: ipython3 EE2703_ASSIGN5_EE19B138.py <Nx> <Ny> <rad> <Niter> 

The last four arguments are optional, but if they are entered, all should be entered, i.e., if non-default values are passed
only to certain variables, then pass the default values to other variables as well. Passing only non-default values to 
certain variables will create ambiguity.

Also, this code works on the assumption that stepsize is same in both the axes. So, in order to visualise a square plate, pass
equal values for Nx, Ny. And for rectangular plate, pass Nx, Ny such that their ratio is the same as the dimensions ratio.
This is explained in detail in the report.

                                             (Nx/Ny) = (X length)/(Y length)
"""

from __future__ import print_function
from sys import argv, exit     
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d      #Importing the libraries needed for the code

Nx=25; Ny=25; rad=8; Niter=1500; arrow = "$\\rightarrow$"; arrow_left = "$\\leftarrow$"   #Defining some useful variables

if len(argv)!=1 and len(argv)!=5:
    print("\nInvalid number of command line arguments.")
    print("Note that if non-default values are to be passed only to certain variables, pass default values to other variables.")
    print("\nCommand usage: %s\n" % argv)
    exit()                       #If the no. of arguments passed isn't 1 or 5, this error will be printed 
elif len(argv)==5:
    try:
        Nx = int(argv[1]); Ny = int(argv[2]); rad = float(argv[3]); Niter = int(argv[4]); 
    except:
        print("\nNon-default values passed are not valid. Pass valid arguments.\n")
        exit()                  #If the non-default arguments passed aren't integers (or float for radius), this error is printed

    if Nx<25 or Ny<25 or rad<8 or Niter<1500:
        print("\nThe non-default values passed are less than default values. Pass values which are more than or equal",end='')
        print("to the default values.\n"); exit()    #If the non-default values are less than default values, this error is printed
    elif Nx<=(2*rad) or Ny<=(2*rad):
        print("\nThe diameter of the wire is more than the plate dimension(s). Please provide appropriate dimensions.\n")
        exit()              #If the diameter of the central wire exceeds the plate dimensions, this error is printed

phi = np.zeros((Ny,Nx))
T = np.zeros((Ny,Nx))+300.0
error = np.zeros((Niter,1))      #The potential, temperature and error arrays are initialised

x = np.array([i for i in range(Nx)])
y = np.array([i for i in range(Ny)])
X, Y = np.meshgrid(x,y)
X_mid = (Nx-1)/2; Y_mid = (Ny-1)/2      #Meshgrid is generated. Middle 'x' and 'y' values are also calculated

X_temp = X-X_mid; Y_temp = Y-Y_mid
dists = np.multiply(X_temp,X_temp)+np.multiply(Y_temp,Y_temp); ii = np.where(dists<=(rad*rad))
phi[ii]=1.0                             #The region where the wire is soldered is found

#Figure to plot the initial potential contour
plt.figure(0)
plt.contourf(X, Y, phi, levels=75, cmap=plt.cm.get_cmap("plasma"))
plt.colorbar(label="\u03A6 values",orientation="vertical")
plt.plot(ii[1],ii[0],'ro')
plt.title("Initial potential plot (in V)")
plt.legend(["\u03A6 = 1 volt"])
plt.xlabel("x"+arrow)
plt.ylabel("y"+arrow)                  

#This For loop present below carries out the averaging process for potential and temperature 
for k in range(Niter):
	
    oldphi = phi.copy()
    phi[1:Ny-1,1:Nx-1] = 0.25*(phi[0:Ny-2,1:Nx-1]+phi[2:Ny,1:Nx-1]+phi[1:Ny-1,0:Nx-2]+phi[1:Ny-1,2:Nx])
    phi[0,:Nx]=0.0; phi[:Ny,0]=phi[:Ny,1]; phi[:Ny,Nx-1]=phi[:Ny,Nx-2]; phi[Ny-1,:Nx]=phi[Ny-2,:Nx]
    phi[ii] = 1.0                                   #Potential array is averaged and updated
    error[k]=np.max((np.abs(phi-oldphi)))           #Error array is updated

    Jx = 0.5*(phi[1:Ny-1,0:Nx-2]-phi[1:Ny-1,2:Nx]); Jy = 0.5*(phi[0:Ny-2,1:Nx-1]-phi[2:Ny,1:Nx-1])
    heats = np.multiply(Jx,Jx)+np.multiply(Jy,Jy)   #Currents(Jx, Jy) and heats arrays are updated 

    T[1:Ny-1,1:Nx-1] = 0.25*(T[0:Ny-2,1:Nx-1]+T[2:Ny,1:Nx-1]+T[1:Ny-1,0:Nx-2]+T[1:Ny-1,2:Nx]+heats)
    T[0,:Nx]=300.0; T[:Ny,0]=T[:Ny,1]; T[:Ny,Nx-1]=T[:Ny,Nx-2]; T[Ny-1,:Nx]=T[Ny-2,:Nx]
    T[ii] = 300.0                                   #Temperature array is averaged and updated
 
itervals = np.array([i for i in range(0,Niter)]); itervals.shape = (Niter,1)
A = np.c_[np.ones((Niter,1)),itervals]              #The matrix and the "log of errors" vector is generated. They serve as 
b = np.log(error)                                   #the training data for the lstsq() function

fit1 = np.linalg.lstsq(A,b,rcond=None)[0]
fit2 = np.linalg.lstsq(A[501:Niter],b[501:Niter],rcond=None)[0]   #Both the fits are generated 

fit1_vals = np.dot(A,fit1)
fit2_vals = np.dot(A[501:Niter],fit2)      #Error vector using both the fits are generated

#Figure to plot the final potential contour
plt.figure(1)
plt.contourf(X, Y, phi, levels=75, cmap=plt.cm.get_cmap("plasma"))
plt.colorbar(label="\u03A6 values",orientation="vertical")
plt.plot(ii[1],ii[0],'ro')
plt.title("Final potential plot (in V)")
plt.legend(["\u03A6 = 1 volt"])
plt.xlabel("x"+arrow)
plt.ylabel("y"+arrow)

#Figure to plot the 3D surface potential plot
fig2 = plt.figure(2)
ax = fig2.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, phi, rstride=1, cstride=1, cmap=plt.cm.get_cmap("plasma"))
plt.colorbar(surf,shrink=0.5,label="\u03A6 values")
ax.set_title("3D potential plot (in V)")
ax.set_xlabel("x"+arrow) 
ax.set_ylabel(arrow_left+"y")
ax.set_zlabel(arrow_left+"\u03A6")

#Figure to plot the Semilogy plot of Error vs Iteration number
plt.figure(3)
plt.plot(itervals[::50],error[::50],'ro',label="Every 50th iteration")
plt.semilogy(itervals,error,label="Exact error plot")
plt.semilogy(itervals,np.exp(fit1_vals),color="forestgreen",label="Fit using all iterations")
plt.semilogy(itervals[501:Niter],np.exp(fit2_vals),color="yellow",label="Fit excluding first 500 iterations")
current_handles, current_labels = plt.gca().get_legend_handles_labels()
current_handles.append(current_handles[0]); current_labels.append(current_labels[0])
del current_handles[0]; del current_labels[0]
plt.legend(current_handles,current_labels)
plt.xlabel("Iteration number"+arrow)
plt.ylabel("Absolute max. error"+arrow)
plt.title("Semilogy error plot")
plt.grid(True)

#Figure to plot the Loglog plot of Error vs Iteration number
plt.figure(4)
plt.loglog(itervals,error)
plt.plot(itervals[::50],error[::50],'ro')
plt.legend(["Exact error","Every 50th iteration"])
plt.xlabel("Iteration number"+arrow)
plt.ylabel("Absolute max. error"+arrow)
plt.title("Loglog error plot")
plt.grid(True)

Jx_temp = np.zeros((Ny,Nx)); Jy_temp = np.zeros((Ny,Nx))  #The currents arrays, which are 'Ny-2' by 'Nx-2' are padded with zero 
Jx_temp[1:Ny-1,1:Nx-1]=Jx; Jy_temp[1:Ny-1,1:Nx-1]=Jy      #currents so that they can be plotted on a 'Ny' by 'Nx' grid 

#Figure to plot the vector plot of the current densities
plt.figure(5)
plt.quiver(X, Y, Jx_temp, Jy_temp,scale=5,label='Current vector')
plt.plot(ii[1],ii[0],'ro',label="\u03A6 = 1 volt")
plt.legend(plt.gca().get_legend_handles_labels()[0],plt.gca().get_legend_handles_labels()[1],loc="upper right")
plt.title("Vector plot of current flow")
plt.xlabel("x"+arrow)
plt.ylabel("y"+arrow)

#Figure to plot the temperature profile contour
plt.figure(6)
plt.contourf(X, Y, T, levels=75, cmap=plt.cm.get_cmap("inferno"))
plt.colorbar(label="T values",orientation="vertical")
plt.plot(ii[1],ii[0],'ro')
plt.title("Temperature plot (in K)")
plt.legend(["\u03A6 = 1 volt"])
plt.xlabel("x"+arrow)
plt.ylabel("y"+arrow)

plt.show()  #Command to show all the figures
#End of the code