"""
************** Python program to simulate a tubelight environment ************

In this program, the environment inside a tubelight is simulated. The electron positions and velocities are found,
random collisions are simulated and the steady state intensity plot is obtained. Also, the electron phase space
plot is obtained.

Done by: V. Ruban Vishnu Pandian 
Date of completion: 11/04/2021

Command line usage: ipython3 EE2703_ASSIGN6_EE19B138.py <n> <M> <nk> <u0> <p> <Msig>

Note: If certain parameters are provided non-default values, provide default values for other parameters. Passing
insufficient parameters will cause ambiguity and hence, the code won't work.
"""

from __future__ import print_function
from sys import argv, exit     
import pylab as pl                      #Libraries needed for the code are imported

n=100
M=10
nk=500
u0=5
p=0.25
Msig = 2
arrow = "$\\rightarrow$"                #Useful parameters are initialised 

if len(argv)!=1 and len(argv)!=7:
    print("\nInvalid number of command line arguments.")
    print("Note that if non-default values are to be passed only to certain variables, pass default values to other variables.")
    print("\nCommand usage: %s\n" % argv)
    exit()                             #If number of arguments is neither 1 nor 7, this error is printed
elif len(argv)==7:
    try:
        n = int(argv[1]); M = int(argv[2]); nk = int(argv[3]); u0 = float(argv[4]); p = float(argv[5]); Msig = float(argv[6]);
    except:
        print("\nNon-default values passed are not valid. Pass valid arguments.\n")
        exit()                         #If non-default values passed aren't valid, this error is printed  

    if n<100 or M<10 or nk<500 or u0<5 or Msig<2 or p<0 or p>1:
        print("\nNon-default values of some parameters are less than their default values (or) Probability is less than 1.")
        print("Pass valid values.\n");
        exit()             #If non-default values are less than default values (or) if probability is more than 1,
                           #this error is printed

xx = pl.zeros((n*M))
u = pl.zeros((n*M))
dx = pl.zeros((n*M))
X = []
V = []
I = []
all_inds = list(range(n*M))      #Vectors and lists required for storing the information are initialised

for i in range(nk):              #For loop to iterate over the timesteps
    ii = pl.where(xx>0)[0]
    dx[ii] = u[ii]+0.5
    xx[ii] = xx[ii]+dx[ii]
    u[ii] = u[ii]+1               #Position and velocity updates are done for electrons inside the tube

    end = pl.where(xx[ii]>n)[0]
    xx[ii[end]] = 0; u[ii[end]] = 0; dx[ii[end]] = 0
    non_zero_x = pl.array(list(set(ii)-set(ii[end])),dtype=int)
    #Electrons with x>n are reset to zero intial conditions

    kk = pl.where(u[non_zero_x]>=u0)[0]
    ll = pl.where(pl.rand(len(kk))<=p)[0]
    kl = non_zero_x[kk[ll]]
    u[kl] = 0                             #Energetic electrons are found and their random collisions are simulated

    rho = pl.rand(len(kl))                #Position update is done for energetic electrons which 
    xx[kl] = xx[kl]-(dx[kl]*rho)          #had undergone successful collisions 
              
    
    m = int((pl.randn()*Msig)+M)
    space_inds = pl.array(list(set(all_inds)-set(non_zero_x)),dtype=int)
    slotnum = min(len(space_inds),m)
    xx[space_inds[:slotnum]] = 1; u[space_inds[:slotnum]] = 0; dx[space_inds[:slotnum]] = 0; 
    #Electrons to be injected are allocated empty slots inside the tube

    I.extend(xx[kl].tolist())
    X.extend(xx.tolist())
    V.extend(u.tolist())   #Lists which store the intensity, position and velocity data are updated


#Figure to plot intensity population plot
pl.figure(0)
histo1=pl.hist(I,bins=pl.arange(0,n+1,1),edgecolor='b',rwidth=1,color='w')
pl.xlabel("x"+arrow)
pl.ylabel("Intensity (No. of excited electrons)"+arrow)
pl.title("Intensity vs X")

#Figure to plot position population plot
pl.figure(1)
histo2=pl.hist(X,bins=pl.arange(0,n+1,1),edgecolor='b',rwidth=1,color='w')
pl.xlabel("x"+arrow)
pl.ylabel("No. of electrons"+arrow)
pl.title("No. of electrons vs X")

#Figure to plot velocity population plot
pl.figure(2)
histo3=pl.hist(V,bins=pl.arange(0,5*u0,1),edgecolor='b',rwidth=1,color='w')
pl.xlabel("v"+arrow)
pl.ylabel("No. of electrons"+arrow)
pl.title("No. of electrons vs V")

#Figure to plot electron phase space plot
pl.figure(3)
pl.plot(X,V,'rx')
pl.xlabel("x"+arrow)
pl.ylabel("v"+arrow)
pl.title("Electron phase space")
pl.show()                               #Show command to plot the generated figures

#Code to print the Bins' midpoints vs Intensities values on the terminal
bins1 = pl.linspace(0, n, n+1)
xpos = 0.5*(bins1[:-1]+bins1[1:])
intensities = histo1[0]
print("Xpos, Intensity:")
for i in range(len(xpos)):
    print(xpos[i], intensities[i])

#End of the code

