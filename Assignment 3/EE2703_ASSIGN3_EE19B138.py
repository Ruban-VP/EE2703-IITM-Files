"""
************** Python program to solve for the least square solution and plot the data ************

In this code, a file containing the noisy data is read, the datasets are processed and a model is fitted to each dataset
based on the least square error minimisation. Finally, various graphs are plotted to visualise the data and the fitted model. 

Done by: V. Ruban Vishnu Pandian 
Date of completion: 03/03/2021

Command line usage: ipython3 EE2703_ASSIGN3_EE19B138.py <Dataset filename>
Note: Ensure that the dataset file is in the PWD (Present working directory)

This program assumes the first column is the independent variable values (usually time) and the following columns
are different datasets with different noises.
"""

from __future__ import print_function
from sys import argv, exit     
from pylab import *
import scipy
import scipy.special as sp
import numpy as np                  #Importing the libraries needed for the code

labels = []
A_vals = linspace(0,2,21); A_vals.shape = (1, 21)
B_vals = linspace(-0.2,0,21); B_vals.shape = (1, 21)
MSE = np.zeros((21,21))
arrow = "$\\rightarrow$"           #Some useful variables are declared beforehand

def g(t,A,B): 
    out = (A*sp.jn(2,t))+(B*t)     #This function implements the fitting model function we are using for the given dataset.
    return out                     #It takes a vector and outputs a vector with its elements as functional values of 
                                   #the elements of the input vector

def mse(arr1, arr2):
    dimens1, dimens2 = arr1.shape             #This function takes two vectors (with equal length) as inputs, calculates
    diff = arr1-arr2                          #the mean squared error and returns it
    error = np.dot(diff.T,diff)/dimens1
    return error

if len(argv)!=2:
    print("\nNumber of arguments not sufficient. Usage: %s\n" % argv);
    exit()                        #If the number of arguments is not 2 (which we don't want), then this error message is printed

#This try-except block present below opens the file, loads the contents as a numpy float array. If that wasn't possible due to
#the listed reasons, an error message is printed and also the possible reasons of failure are printed as well.
try:
    data = np.loadtxt(argv[1])
except:
    print("\nSome of the following errors are there:\n")
    print("1. File name not valid\n2. Data doesn't have same number of columns for all rows\n3. Data has some non-floating point contents\n")
    print("Correct these errors and pass a valid datafile\n")
    exit()


N,k = data.shape                        #The dimensions of the dataset are stored

time = data[:,[0]]                      #Time vector (t) is obtained
true_val = g(time,1.05,-0.105);         #True value vector is generated

x = [i for i in range(1,k)]             #The noisy dataset is stored seperately
allcols = data[:,x]

scl = np.std(allcols-true_val, axis = 0)
scl.shape = (1,len(x))                  #Standard deviations of different datasets are calculated and stored in a row array

M = c_[sp.jn(2,time),time]

[X, Y] = meshgrid(A_vals, B_vals)       #Meshgrid is formed to plot a contour plot
for i in range(21):
    for j in range(21):                                                 #The mean squared error values corresponding to different 
        MSE[i,j] = mse(data[:,[1]],g(time,A_vals[0][i],B_vals[0][j]))   #combinations of A, B are stored in a 21x21 matrix 
                                                                           

lstsols = np.zeros((len(x),2))                      
for k in x:                                                         #For Loop to obtain the least square solutions
    temp,_,_,_ = scipy.linalg.lstsq(M, data[:,[k]],cond=None)       #The least square solutions of different datasets are obtained 
    temp.shape = (1,2)
    lstsols[k-1] = temp
    st = '\u03C3{0}'.format(chr(0x2080 +  k))                       #The labels for the first plot are generated
    labels.append(st+" = %.3f" % scl[0][k-1])

labels.append("True value")
lstsols = abs(lstsols - np.array([1.05, -0.105]))

p = np.array([[2],[3]])                            #Temporary vector 'p' used to check whether M.p = g(t;A,B) (A=2,B=3)
v1 = np.dot(M,p)                                   #Vector 1 which is M.p
v2 = g(time,2,3)                                   #Vector 2 which is g(t;A,B)
if np.all((v1-v2)==0)==True:                       #If-else condition used to check validity of the matrix M
	print("\nQ6: M matrix is formed and its validity verified successfully\n")
else:
	print("\nQ6: Invalid M matrix has been formed\n")

#First figure, which contains the plots of all the noisy datasets is generated (Also contains the true values plot)
figure(0)
plot(time,allcols)
plot(time,true_val,'k')
legend(labels)
xlabel('t'+arrow,size=20)
ylabel('f(t) + noise'+arrow,size=20)
title('Q4: Data to be fitted to theory',size=20)
grid(True)                                            

#Second figure, which contains the errorbars of the noisy data with sigma=0.1 is generated (Also contains the true values plot) 
figure(1)
plot(time,true_val,'k')
errorbar(time[::5],data[::5,1],scl[0][0],fmt='ro')
legend(["f(t)","Errorbar"])
xlabel('t'+arrow,size=20)
title('Q5: Data points for 'r'$\sigma=0.10$ along with exact function',size=15)
grid(True)

#Third figure, which contains the contours of the mean sqaured errors for different combinations of A, B is generated
figure(2)
contvals = linspace(0.025, 0.100, 4)
conplot = contour(X, Y, MSE, 20)
clabel(conplot, contvals)
xlabel('A'+arrow,size=10)
ylabel('B'+arrow,size=10)
title('Q8: Contour plot of 'r'$\epsilon_{ij}$',size=15)
plot(1.05,-0.105,'ro')
annotate("Exact solution",(1.05,-0.105))

#Fourth figure, which contains the linear plot of errors in estimate of A, B with respect to the noise is generated 
figure(3)
plot(scl.T,lstsols[:,[0]],'ro--')
plot(scl.T,lstsols[:,[1]],'go--')
legend(['Aerr','Berr'])
xlabel('Noise standard deviation'+arrow,size=20)
ylabel('MS error'+arrow,size=20)
title('Q10: Variation of error with noise',size=20)
grid(True)

#Fifth figure, which contains the logarithmic plot of errors in estimate of A, B with respect to the noise is generated 
figure(4)
errA = lstsols[:,0]
errB = lstsols[:,1]
loglog(scl.T,errA,'ro')
loglog(scl.T,errB,'go')
errorbar(scl.T,errA,errA,fmt='ro')
errorbar(scl.T,errB,errB,fmt='go')
legend(["Aerr","Berr"])
xlabel(''r'$\sigma_n$'+arrow,size=18)
ylabel('MS Error'+arrow,size=20)
title('Q11: Variation of error with noise',size=20)
grid(True)

show()  #Show command to show all the generated figures
#End of the code
