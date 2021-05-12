"""
************** Python program to analyse active RC filters using Sympy and Scipy.signal packages ****************

In this program, active RC filters are analysed using Laplace transforms. To derive the Laplace transform expressions,
Sympy package is used. It is also used to obtain the magnitude responses of the filters. And then scipy.signal toolbox
is used to obtain the step responses, sum of sinusoids responses and damped sinusoid responses for two types of 
filters: Low pass and High pass. 

Done by: V. Ruban Vishnu Pandian 
Date of completion: 25/04/2021

Command line usage: ipython3 EE2703_ASSIGN7_EE19B138.py 
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig          #Required libraries are imported

s = sp.symbols('s')                 #Variable 's' is allocated symbol 's'
arrow = "$\\rightarrow$"            #Used in the plot command
 
#Function 1: LPF: This function obtains the LPF circuit components, computes the laplace transform of the output and 
#returns it 
def LPF(R1,R2,C1,C2,G,Vi):
    A = sp.Matrix([[0,0,1,-1/G],[-1/(1+(s*R2*C2)),1,0,0],[0,-G,G,1],[-(1/R1)-(1/R2)-(s*C1),1/R2,0,s*C1]])
    b = sp.Matrix([0,0,0,-Vi/R1])
    V = A.inv()*b; TF = V[3]
    return TF

#Function 2: HPF: This function obtains the HPF circuit components, computes the laplace transform of the output and 
#returns it 
def HPF(R1,R3,C1,C2,G,Vi):
    A = sp.Matrix([[0,0,1,-1/G],[-s*C2*R3/(1+(s*C2*R3)),1,0,0],[0,-G,G,1],[-(s*C1)-(s*C2)-(1/R1),s*C2,0,1/R1]])
    b = sp.Matrix([0,0,0,-Vi*s*C1])
    V = A.inv()*b; TF = V[3]
    return TF

#Function 3: SymtoTrans: This function accepts a sympy transfer function expression as input and returns the 
#signal toolbox LTI form of the transfer function as output
def SymtoTrans(TF):
    n,d = TF.as_numer_denom()
    num = n.as_poly(s).all_coeffs()
    den = d.as_poly(s).all_coeffs()
    num = [float(i) for i in num]
    den = [float(i) for i in den]
    H = sig.lti(num,den)
    return H

#Function 4: magresponse: This function accepts a transfer function and a frequency vector as input and returns the 
#magnitude response vector,which contains magnitudes of the transfer functions at different frequencies as output
def magresponse(TF,w):
    ss = 1j*w
    tf = sp.lambdify(s,TF,"numpy")
    return abs(tf(ss))

#Function 5: sumofsins_response: This function accepts two frequencies, time vector and signal toolbox LTI form of 
#a transfer function, does the convolution to get the output signal and returns it as output
def sumofsins_response(w1,w2,t,H):
    x = np.sin(w1*t)+np.cos(w2*t)
    vo = sig.lsim(H,x,t)[1]
    return vo

#Function 6: dampedsin_response: This function accepts the damped sinusoid frequency, decay constant,time vector and 
#signal toolbox LTI form of a transfer function, does the convolution to get the output signal and returns it as output
def dampedsin_response(wd,a,t,H):
    x = np.cos(wd*t)*np.exp(-a*t)
    vo = sig.lsim(H,x,t)[1]
    return vo

R1 = 1e4; R2 = 1e4; R3 = 1e4; C1 = 1e-9; C2 = 1e-9; G = 1.586; Vi=1 #Values of the circuit components
LPF_Trans = LPF(R1,R2,C1,C2,G,Vi)
HPF_Trans = HPF(R1,R3,C1,C2,G,Vi)   #Transfer functions are obtained

LPF_H = SymtoTrans(LPF_Trans)
HPF_H = SymtoTrans(HPF_Trans)       #Transfer functions are converted to their signal toolbox LTI form

w = np.logspace(0,12,1000)
LPF_magres = magresponse(LPF_Trans,w)
HPF_magres = magresponse(HPF_Trans,w)    #Magnitude responses vectors are generated for a given frequency vector

#Figure to plot magnitude response of LPF
plt.figure(1)
plt.loglog(w,LPF_magres)
plt.grid(True)
plt.xlabel("Frequency (in rad/s)"+arrow)
plt.ylabel("Magnitude of H(s)"+arrow)
plt.title("Magnitude response of low pass filter")

#Figure to plot magnitude response of HPF
plt.figure(2)
plt.loglog(w,HPF_magres)
plt.grid(True)
plt.xlabel("Frequency (in rad/s)"+arrow)
plt.ylabel("Magnitude of H(s)"+arrow)
plt.title("Magnitude response of high pass filter")

Vi = 1/s
LPF_Stepres = LPF(R1,R2,C1,C2,G,Vi)
HPF_Stepres = HPF(R1,R3,C1,C2,G,Vi)  #Step response laplace transforms are obtained

LPF_Stepres = SymtoTrans(LPF_Stepres)
HPF_Stepres = SymtoTrans(HPF_Stepres)  #They are converted to the signal toolbox LTI form  

t = np.linspace(0,1e-3,1000)
LPF_Stepres = sig.impulse(LPF_Stepres,None,t)[1]
HPF_Stepres = sig.impulse(HPF_Stepres,None,t)[1] #The step responses are calculated for a given time vector 

#Figure to plot the step response of LPF
plt.figure(3)
plt.plot(t,LPF_Stepres)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Response of u(t)"+arrow)
plt.title("Step response of Low pass filter")

#Figure to plot the step response of HPF
plt.figure(4)
plt.plot(t,HPF_Stepres)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Response of u(t)"+arrow)
plt.title("Step response of High pass filter")

w1 = 2000*np.pi; w2 = 2*np.pi*1e6
t = np.linspace(0,1e-3,100000)
x = np.sin(w1*t)+np.cos(w2*t)        #Sum of sinusoids signal is generated

#Figure to plot the sum of sinusoids signal
plt.figure(5)
plt.plot(t,x)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Signal"+arrow)
plt.title("Sum of sinusoids")

t1 = np.linspace(0,1e-3,100000)
t2 = np.linspace(0,1e-5,100000)
LPF_out = sumofsins_response(w1,w2,t1,LPF_H) #Output responses of the sum of sinusoids signal are generated for both
HPF_out = sumofsins_response(w1,w2,t2,HPF_H) #the filters

#Figure to plot the output response of sum of sinusoids signal of an LPF
plt.figure(6)
plt.plot(t1,LPF_out)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Output signal"+arrow)
plt.title("LPF response of sum of sinusoids")

#Figure to plot the output response of sum of sinusoids signal of a HPF
plt.figure(7)
plt.plot(t2,HPF_out)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Output signal"+arrow)
plt.title("HPF response of sum of sinusoids")

wd1 = 2*np.pi*1e3; wd2 = 2*np.pi*1e6; a=2e2
t = np.linspace(0,1e-2,100000)
x1 = np.cos(wd1*t)*np.exp(-a*t)
x2 = np.cos(wd2*t)*np.exp(-a*t)        #Damped sinusoid signals of two different frequencies are generated

#Figure to plot the low frequency damped sinusoid signal
plt.figure(8)
plt.plot(t,x1)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Signal"+arrow)
plt.title("Damped sinusoid with low frequency")

#Figure to plot the high frequency damped sinusoid signal
plt.figure(9)
plt.plot(t,x2)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Signal"+arrow)
plt.title("Damped sinusoid with high frequency")

LPF_out_low = dampedsin_response(wd1,a,t,LPF_H)
HPF_out_low = dampedsin_response(wd1,a,t,HPF_H)
LPF_out_high = dampedsin_response(wd2,a,t,LPF_H)  #Output responses of the damped sinusoid signals are obtained
HPF_out_high = dampedsin_response(wd2,a,t,HPF_H)  #for both the filters

#Figure to plot the output response of low frequency damped sinusoid when passed through an LPF
plt.figure(10)
plt.plot(t,LPF_out_low)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Output signal"+arrow)
plt.title("LPF response of damped sinusoid of low frequency")

#Figure to plot the output response of low frequency damped sinusoid when passed through a HPF
plt.figure(11)
plt.plot(t,HPF_out_low)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Output signal"+arrow)
plt.title("HPF response of damped sinusoid of low frequency")

#Figure to plot the output response of high frequency damped sinusoid when passed through an LPF
plt.figure(12)
plt.plot(t,LPF_out_high)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Output signal"+arrow)
plt.title("LPF response of damped sinusoid of high frequency")

#Figure to plot the output response of high frequency damped sinusoid when passed through a HPF
plt.figure(13)
plt.plot(t,HPF_out_high)
plt.grid(True)
plt.xlabel("Time (in sec)"+arrow)
plt.ylabel("Output signal"+arrow)
plt.title("HPF response of damped sinusoid of high frequency")

plt.show() #Show command to show all the generated plots
