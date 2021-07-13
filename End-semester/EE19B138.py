"""
************** Python program to analyse the radiation from a loop antenna ************

In this code, the magnetic field due to a current carrying circular loop is found along the z-axis, analysed and a model 
is fitted for the field with respect to the z values. 

Done by: V. Ruban Vishnu Pandian 
Date of completion: 25/05/2021

Command line usage: python3 EE19B138.py <flag> <k_flag> <Nx> <Ny> <Nz> <N_angle>

Note: If certain parameters are provided non-default values, provide default values for other parameters. Passing
insufficient parameters will cause ambiguity and hence, the code won't work. Also, don't pass very high values for 
Nx, Ny, Nz and N_angle because it'll slow down the code.
"""

from sys import argv, exit
import pylab as p
import scipy.linalg as sp     #Importing the required libraries

flag = 0; k_flag = 0
a = 10; k = 1/a
Nx = 3; Ny = 3; Nz = 1000; N_angle = 100 #The parameters are initialised with default values
arrow = "$\\rightarrow$"      #Useful variable in plotting

if len(argv)!=1 and len(argv)!=7:
    print("\nInvalid number of command line arguments.")
    print("Note that if non-default values are to be passed only to certain variables, pass default values to other variables.")
    print("\nCommand usage: %s\n" % argv)
    exit()                    
    #If the number of command line arguments is neither 1 nor 7 (which we don't want), then this error is printed

elif len(argv)==7:
    try:
        flag = int(argv[1]); k_flag = int(argv[2]); Nx = int(argv[3])
        Ny = int(argv[4]); Nz = int(argv[5]); N_angle = int(argv[6])     #Non-default values are stored
    except:
        print("\nNon-default values passed are not valid. Pass valid arguments.\n")
        exit()                            #If the non-default values are not valid, this error is printed

    if Nx<3 or Ny<3 or Nz<2 or N_angle<20:
        print("\nThe non-default values passed are too low. Pass bigger values.\n")
        exit()
    elif Nx%2==0 or Ny%2==0 or N_angle%2!=0:
        print("\nSome of the following conditions must have been violated:\n")
        print("1. Nx (Number of divisions in x-axis) must be an odd number.")
        print("2. Ny (Number of divisions in y-axis) must be an odd number.")
        print("3. N_angle (Number of divisions for the interval [0,2pi]) must be an even number.\n")
        print("Please make the required corrections to the non-default values passed so that these conditions are obeyed.\n")
        exit()
    #If the non-default values are either too low or doesn't satisfy certian conditions, the if-else block present
    #above will be executed

if k_flag!=0:
    k = 0         #If k_flag is non-zero (Non-default case), k is equated to zero (Static current case)

xval = p.linspace(-1,1,Nx); del_x = xval[1]-xval[0]
yval = p.linspace(-1,1,Ny); del_y = yval[1]-yval[0]
zval = p.linspace(1,1000,Nz); del_z = zval[1]-zval[0] #The x,y,z interval arrays are created and stepsizes are computed 

angle_vals = p.linspace(0,2*p.pi,N_angle+1)
del_angle = angle_vals[1]-angle_vals[0]               #The angle interval array is created and stepsize is computed           

x_vals = a*p.cos(angle_vals)
y_vals = a*p.sin(angle_vals)                          
#The two arrays present above refer to the radial vectors array (rl) 

phi_cap_x_vals = -p.sin(angle_vals)
phi_cap_y_vals = p.cos(angle_vals)
#The two arrays present above refer to the tangential unit vectors array (phi_cap) 

dl_x_vals = a*del_angle*phi_cap_x_vals 
dl_y_vals = a*del_angle*phi_cap_y_vals 
#The two arrays present above refer to the infinitesimal current element vectors array (dl_l) 

current_x_vals = p.cos(angle_vals)*phi_cap_x_vals
current_y_vals = p.cos(angle_vals)*phi_cap_y_vals
#The two arrays present above refer to the normalised current vectors array (I). The I array is just used for plotting 

p.figure(1)
p.quiver(x_vals,y_vals,current_x_vals,current_y_vals,color='b',scale=40)
p.grid(True)
p.xlabel("x (in cm)"+arrow)
p.ylabel("y (in cm)"+arrow)
p.title("Normalised current distribution plot")
p.legend(['Current vector'])         #Plotting commands for the current distribution

p.figure(2)
p.plot(x_vals,y_vals,'k--')
p.quiver(x_vals*0,y_vals*0,x_vals,y_vals,angles='xy',color='b',scale=1,scale_units='xy')
p.grid(True)
p.xlabel("x (in cm)"+arrow)
p.ylabel("y (in cm)"+arrow)
p.title("Radial vector plot")
p.legend(['Circular wire','Radial vector'])  #Plotting commands for the radial vectors

p.figure(3)
p.quiver(x_vals,y_vals,phi_cap_x_vals,phi_cap_y_vals,color='b',scale=40)
p.grid(True)
p.xlabel("x (in cm)"+arrow)
p.ylabel("y (in cm)"+arrow)
p.title("Tangential vector plot")
p.legend(['Tangential vector'],loc="upper right") #Plotting commands for the tangential unit vectors

yy, zz, xx = p.meshgrid(yval,zval,xval)   #The 3D arrays which store the y,z,x coordinates are created respectively
Ax = p.zeros((Nz,Ny,Nx))
Ay = p.zeros((Nz,Ny,Nx))                  #3D arrays to store the vector potential terms are initialised with zeros

#Function calc(l): This function takes in the index 'l' as input, calculates the distances of points r_ijk from r_l using
#vector operations, generates the Ax_l and Ay_l terms and returns them 
def calc(l):
    ang = angle_vals[l]
    xl = x_vals[l]; yl = y_vals[l]
    Rl = p.sqrt(((xx-xl)**2)+((yy-yl)**2)+(zz**2))        #Distances are calculated for a particular 'l'

    Ax_l = p.cos(ang)*p.exp(-1j*k*Rl)*dl_x_vals[l]/Rl 
    Ay_l = p.cos(ang)*p.exp(-1j*k*Rl)*dl_y_vals[l]/Rl     #Ax_l, Ay_l terms are calculated for all 'ijk'

    return Ax_l, Ay_l                                     #Returning of Ax_l and Ay_l

#The variable 'flag' is a control variable which allows the user to decide whether to include phi=2pi in the 
#vector potential computation or not
if flag==0:
    Niter = N_angle         #If flag=0 (Default case), then 2pi won't be included and we will get Bz = 0
else:
    Niter = N_angle+1       #If flag!=0 (Non-default case), then 2pi will be included 

"""
For loop to calculate A_ijk: We use a for loop to calculate A_ijk because we can't vectorize the summation over 'l'.
To do that we need to store the 3D R_ijk arrays for different values of 'l' in a list and then must implement element-wise
multiplication in list which is not feasible.
"""
for l in range(Niter):
    Ax_l, Ay_l = calc(l)            #The Ax_l, Ay_l values are obtained by calling the calc function
    Ax = Ax+Ax_l; Ay = Ay+Ay_l      #The returned vector potential terms are added to the Ax, Ay 3D arrays

zero_ind_x = int(Nx/2); zero_ind_y = int(Ny/2)
#The zero indices in x,y axes (Indices where x=0, y=0) are found in order to compute Bz

Bz1 = (Ay[:,zero_ind_y,zero_ind_x+1]-Ay[:,zero_ind_y,zero_ind_x-1])/(2*del_x) #Partial derivative of Ay with respect to x is computed 
Bz2 = (Ax[:,zero_ind_y-1,zero_ind_x]-Ax[:,zero_ind_y+1,zero_ind_x])/(2*del_y) #Negative partial derivative of Ax with respect to y is computed
Bz = Bz1+Bz2; Bz = Bz*100   #Bz is computed by adding the partial derivative terms we got
                            #Also, Bz is multiplied wiht 100 so that its units would now be in Tesla (T)

M = p.c_[zval**0,p.log(zval)]      
N = p.log(abs(Bz))
x = sp.lstsq(M,N)[0]  #The matrices present in the model fit matrix equation are computed and the parameters are computed
                      #using the least squares function
c = p.exp(x[0])       
b = x[1]              #The parameters are extracted and stored in variables 'c' and 'b'

Bz_fit = c*(zval**b)  #The Bz values using the fitting parameters are obtained

p.figure(4)
p.loglog(zval,abs(Bz))
p.loglog(zval,Bz_fit)
p.grid(True)
p.xlabel("z (in cm)"+arrow)
p.ylabel(r"|B$_z$(z)| (in T)"+arrow)
p.title(r"Logarithmic plot of z vs |B$_z$(z)|")
p.legend([r'Actual |B$_z$(z)| plot',r'Plot of |B$_z$(z)| obtained using fit'],loc="upper right")
#Plotting commands for plotting the actual Bz values and Bz values obtained using fit on a logarithmic scale

p.show() #Show command to invoke Matplotlib and show all these plots on the monitor

if flag==0:
    print("\nThe Bz plot we get is because of computer precision error. Theoretically, Bz is zero.")
    print("Hence, the variation it has with z is random and the plot is not useful.")
    print("Estimated value of c: %e" % c)
    print("Estimated value of b: %.3f\n" % b)
    #If flag=0, i.e, 2pi is not included, then the Bz plot we get is purely due to computer error. The user is informed
    #about the same 

else:
    print("\nWhen flag is not equal to 1, the contribution for A from angle 2pi is also considered.")
    print("This leads to a proper variation of Bz vs z since now we have a non-zero Bz component that properly varies with z.\n")
    print("Estimated value of c: %.3f" % c)
    print("Estimated value of b: %.3f\n" % b)
    #If flag!=0, i.e, 2pi is included, then the Bz plot we get is proper and it is because of the element at phi=0.
    #The user is informed about the same 

#End of the code