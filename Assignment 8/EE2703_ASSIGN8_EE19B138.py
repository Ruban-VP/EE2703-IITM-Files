"""
************** Python program to plot DFT of certain signals ****************

In this program, the in-built DFT library of python is used to compute and plot DFT of certain signals such as:
1. Sinusoids
2. Amplitude modulated signal
3. Frequency modulated signal
4. Gaussian signal

Done by: V. Ruban Vishnu Pandian 
Date of completion: 07/05/2021

Command line usage: ipython3 EE2703_ASSIGN8_EE19B138.py 
"""

import pylab as p
import numpy as np
import scipy.special as sp     #Importing the required libraries

arrow = "$\\rightarrow$"       #Variable used in plot command

"""
The functions defined below are to find and plot the DFT of the signals question-wise.
First four functions take in two arguments: N, M which are the exponents of 2
This 'N' is not the same 'N' given in the assignment

In the first four functions:
Number of divisions (N given in the assignment) = 2^N
Period (T0) = (2^M)*pi

In the last function, the arguments are 'N' and 'T0'
Again, number of divisions is 2^N and the period is T0
"""

"""
Function 1: DFT of sin(5t):
In this function, DFT of the signal sin(5t) is found. To do this, a time range of (2^M)*pi is divided into
2^N points and the samples at those points are taken to find the DFT
"""
def Q1_sin(N,M):
    num = 2**N
    time_range = 2**M
    t = p.linspace(0,time_range*p.pi,num+1); t = t[:-1]
    f = p.sin(5*t)
    F = p.fftshift(p.fft(f))/num                             #DFT is found and stored. Also, the CT frequency axis
    w = p.linspace(-num/time_range,(num-2)/time_range,num)   #is generated

    p.subplot(2,1,1)
    p.plot(w,abs(F))
    p.xlim([-10,10])
    p.ylabel(r"$|Y|$"+arrow)
    p.title("Spectrum of sin(5t)")
    p.grid(True)                                             #Code to plot the magnitudes of the DFT coefficients

    p.subplot(2,1,2)
    p.plot(w,p.angle(F),'ro')
    ii = p.where(abs(F)>1e-3)[0]
    p.plot(w[ii],p.angle(F[ii]),'go')
    p.xlim([-10,10])
    p.xlabel("Frequency"+arrow)
    p.ylabel("Phase of Y"+arrow)
    p.grid(True)                                              #Code to plot the phases of the DFT coefficients


"""
Function 2: DFT of AM signal:
In this function, DFT of the signal (1+0.1cos(t))cos(10t) is found. To do this, a time range of (2^M)*pi is divided into
2^N points and the samples at those points are taken to find the DFT
"""
def Q1_modulation(N,M):
    num = 2**N
    time_range = 2**M
    t = p.linspace(0,time_range*p.pi,num+1); t = t[:-1]
    f = (1+0.1*p.cos(t))*p.cos(10*t)
    F = p.fftshift(p.fft(f))/num
    w = p.linspace(-num/time_range,(num-2)/time_range,num)

    p.subplot(2,1,1)
    p.plot(w,abs(F))
    p.xlim([-20,20])
    p.ylabel(r"$|Y|$"+arrow)
    p.title(r"Spectrum of $\left(1+0.1\cos\left(t\right)\right)\cos\left(10t\right)$")
    p.grid(True)

    p.subplot(2,1,2)
    p.plot(w,p.angle(F),'ro')
    ii = p.where(abs(F)>1e-3)[0]
    p.plot(w[ii],p.angle(F[ii]),'go')
    p.xlim([-20,20])
    p.xlabel("Frequency"+arrow)
    p.ylabel("Phase of Y"+arrow)
    p.grid(True)

"""
Function 3: DFT of cubes of sinusoids:
In this function, DFTs of the signals sin^3(t) and cos^3(t) are found. To do this, a time range of (2^M)*pi is divided 
into 2^N points and the samples at those points are taken to find the DFT
"""
def Q2(N,M,flag):
    num = 2**N
    time_range = 2**M
    t = p.linspace(0,time_range*p.pi,num+1); t = t[:-1]
    if flag==1:
        f = p.cos(t)**3
    else:
        f = p.sin(t)**3
    F = p.fftshift(p.fft(f))/num
    w = p.linspace(-num/time_range,(num-2)/time_range,num)

    p.subplot(2,1,1)
    p.plot(w,abs(F))
    p.xlim([-10,10])
    p.ylabel(r"$|Y|$"+arrow)
    if flag==1:
        p.title(r"Spectrum of cos$^3$(t)")
    else:
        p.title(r"Spectrum of sin$^3$(t)")
    p.grid(True)

    p.subplot(2,1,2)
    p.plot(w,p.angle(F),'ro')
    ii = p.where(abs(F)>1e-3)[0]
    p.plot(w[ii],p.angle(F[ii]),'go')
    p.xlim([-10,10])
    p.xlabel("Frequency"+arrow)
    p.ylabel("Phase of Y"+arrow)
    p.grid(True)

"""
Function 4: DFT of FM signal:
In this function, DFT of the signal cos(20t+5cos(t)) is found. To do this, a time range of (2^M)*pi is divided into
2^N points and the samples at those points are taken to find the DFT
"""
def Q3(N,M):   
    num = 2**N
    time_range = 2**M 
    t = p.linspace(0,time_range*p.pi,num+1); t = t[:-1]
    f = p.cos(20*t+5*p.cos(t))
    F = p.fftshift(p.fft(f))/num
    w = p.linspace(-num/time_range,(num-2)/time_range,num)

    p.subplot(2,1,1)
    p.plot(w,abs(F))
    p.xlim([-35,35])
    p.ylabel(r"$|Y|$"+arrow)
    p.title("Spectrum of cos(20t+5cos(t))")
    p.grid(True)

    p.subplot(2,1,2)
    ii = p.where(abs(F)>1e-3)[0]
    p.plot(w[ii],p.angle(F[ii]),'go')
    p.xlim([-35,35])
    p.xlabel("Frequency"+arrow)
    p.ylabel("Phase of Y"+arrow)
    p.grid(True)

"""
Function 5: DFT of the gaussian:
In this function, DFT of the signal exp(-t^2/2) is found. To do this, a time range of T0 is divided into
2^N points and the samples at those points are taken to find the DFT
"""
def Q4(N,T0,flag):
    num = 2**N
    t = p.linspace(0,T0,num+1); t = t[:-1]
    ii = p.where(t>=(T0/2))[0]
    f = p.exp((-t*t)/2)
    f[ii] = p.exp((-(t[ii]-T0)*(t[ii]-T0))/2)
    F = p.fftshift(p.fft(f))*T0/num
    lim = num*p.pi/T0
    w = p.linspace(-lim,(lim-(2*p.pi/T0)),num)
    actual_F = p.sqrt(2*p.pi)*p.exp(-w**2/2)
    error = np.max(abs(F)-actual_F)

    if flag==1:
        p.subplot(2,1,1)
        p.plot(w,abs(F))
        p.xlim([-10,10])
        p.ylabel(r"$|Y|$"+arrow)
        p.title(r"Spectrum of exp(-t$^2$/2) for period = %d and N = %d" % (T0, num))
        p.grid(True)

        p.subplot(2,1,2)
        p.plot(w,p.angle(F),'go')
        p.xlim([-10,10])
        p.xlabel("Frequency"+arrow)
        p.ylabel("Phase of Y"+arrow)
        p.grid(True)

    return t,f,error

p.figure(1)
Q1_sin(7,1)                    #Plot of DFT of the sin(t) signal with low resolution

p.figure(2)
Q1_sin(10,3)                   #Plot of DFT of the sin(t) signal with high resolution

p.figure(3)
Q1_modulation(7,1)             #Plot of DFT of the AM signal with low resolution

p.figure(4)
Q1_modulation(10,3)            #Plot of DFT of the AM signal with high resolution

p.figure(5)
Q2(10,3,0)                     #Plot of DFT of the cube of sin(t)

p.figure(6)
Q2(10,3,1)                     #Plot of DFT of the cube of cos(t)

p.figure(7)
Q3(12,5)                       #Plot of DFT of the FM signal

p.figure(8)
t,f,error = Q4(10,20,1)        #Plot of DFT of the gaussian with T0=20 and N=10 (or Number of divisions = 1024)

p.figure(9)
p.plot(t,f)
p.xlabel("Time"+arrow)
p.ylabel("Function"+arrow)
p.title("First period of Gaussian")
p.grid(True)                   #The first period of gaussian is plotted 

i=10
for j in range(5):
    period = 8*(j+1)
    p.figure(i+j)
    Q4(10,period,1)            #5 plots of DFT of the gaussian signal are plotted for different T0 (Period) values 
    
errors = []
periods = []

for j in range(100):
    period = 1.5*(j+1)
    t,f,error = Q4(10,period,0)
    periods.append(period)
    errors.append(error)      #For loop to get the max. error in the DFT plot for different period values

errors = np.array(errors)
periods = np.array(periods)

p.figure(15)
p.plot(periods,errors)
p.xlabel("Period"+arrow)
p.ylabel("Max. error in DFT"+arrow)
p.title("Max. error vs Period plot")
p.grid(True)                  #Plot of the max. errors vs the periods

beta = 5
k = [i for i in range(-20,20)]
k = np.array(k)                      #The Bessel's function vector is generated for some set of integers (denoted by k) 
bessels = ((1j**k)*sp.jv(k,5))/2     #and it is multiplied by 1j^k/2

p.figure(16)
p.subplot(2,1,1)
p.stem(k,abs(bessels))
p.xlim([-20,20])
p.title("Fourier coefficients plot")
p.ylabel(r"|a$_k$|"+arrow)
p.grid(True)                         #Subplot for plotting the magnitudes of the Bessel's functions

p.subplot(2,1,2)
ii = p.where(abs(bessels)>1e-3)
p.plot(k[ii],p.angle(bessels[ii]),'go')
p.xlim([-20,20])
p.ylabel(r"Phase of a$_k$"+arrow)
p.xlabel("Frequency"+arrow)
p.grid(True)                         #Subplot for plotting the phases of the Bessel's functions

p.show()                             #Show command to show all the plots

#End of the code