"""
************** Python program to solve differential equations using Laplace transforms ****************

In this program, Laplace transform techniques are used to solve various differential equations pertaining to systems
such as spring-mass arrangement, coupled springs arrangement, electrical filter, etc. using the scipy.signal library 
and the polynomial functions of the numpy library.

Done by: V. Ruban Vishnu Pandian 
Date of completion: 18/04/2021

Command line usage: ipython3 EE2703_ASSIGN6L_EE19B138.py 
"""

from __future__ import print_function     
import pylab as p
import scipy.signal as sp  #Importing the required libraries

arrow = "$\\rightarrow$"   #For labelling purposes

#Function Q12: Pertains to questions 1 and 2 of the assignment
def Q12(a=0.5,wo=1.5,wd=1.5,div=501):
    X_num = p.poly1d([1,a])
    X_den_temp = p.poly1d([1,2*a,((wd*wd)+(a*a))])
    diff_eqn = p.poly1d([1,0,wo*wo])
    X_den = p.polymul(X_den_temp,diff_eqn)       #The laplace transform of x(t) is generated

    X = sp.lti(X_num,X_den)
    t,x = sp.impulse(X,None,p.linspace(0,50,div)) #x(t) is found from X(s) using the sp.impulse function
    return t,x,a

#Function Q3: Pertains to question 3 of the assignment
def Q3(a=0.05,wo=1.5,div=501):
    wd=1.4; i=0
    H = sp.lti([1],[1,0,wo*wo])
    t = p.linspace(0,100,div)             #Transfer function and time vector are generated

    while(wd<=1.6):                       #While loop to loop over the frequencies
        p.figure(3+i)
        f = p.cos(wd*t)*p.exp(-a*t)
        y = sp.lsim(H,f,t)[1]             #Output time response is obtained using sp.lsim function
        p.plot(t,y)
        p.xlabel("t"+arrow)
        p.ylabel("x(t)"+arrow)
        p.title("x(t) vs t for w = %.2f rad/s" % wd)
        p.grid(True)                      #Output time response is plotted

        wd += 0.05; i += 1                #Frequency is incremented by 0.05 rad/s

#Function Q4: Pertains to question 4 of the assignment
def Q4(div=501):
    X = sp.lti([1,0,2],[1,0,3,0])
    Y = sp.lti([2],[1,0,3,0])
    t = p.linspace(0,20,div)
    x = sp.impulse(X,None,t)[1]
    y = sp.impulse(Y,None,t)[1]          #The responses x(t),y(t) are de-coupled and obtained for a given time vector
    return t,x,y

#Function Q56: Pertains to questions 5 and 6 of the assignment
def Q56(R=100,L=1e-6,C=1e-6,a=1e3,b=1e6):
    H = sp.lti([1],[L*C,R*C,1])
    w,mag,phi = H.bode()                 #Frequencies, magnitude response and phase response are obtained

    t1 = p.linspace(0,30*1e-6,301)
    v_in1 = p.cos(a*t1)-p.cos(b*t1)
    v_out1 = sp.lsim(H,v_in1,t1)[1]      #Output time response till 30 micro seconds is obtained

    t2 = p.linspace(0,10*1e-3,100001)
    v_in2 = p.cos(a*t2)-p.cos(b*t2)
    v_out2 = sp.lsim(H,v_in2,t2)[1]      #Output time response till 10 milli seconds is obtained

    return w,mag,phi,t1,v_out1,t2,v_out2
    
#Plot for output response of Q1 is generated
p.figure(1)
t,x,a = Q12()
p.plot(t,x)
p.grid(True)
p.xlabel("t"+arrow)
p.ylabel("x(t)"+arrow)
p.title("x(t) vs t for decay=%.2f" % a)

#Plot for output response of Q2 is generated
p.figure(2)
t,x,a = Q12(a=0.05)
p.plot(t,x)
p.grid(True)
p.xlabel("t"+arrow)
p.ylabel("x(t)"+arrow)
p.title("x(t) vs t for decay=%.2f" % a)

#Plots corresponding to different frequencies in Q3 are generated
Q3()

#Plot for output responses of Q4 is generated
p.figure(8)
t,x,y = Q4()
p.plot(t,x)
p.plot(t,y)
p.grid(True)
p.legend(["x(t)","y(t)"])
p.xlabel("t"+arrow)
p.ylabel("Outputs"+arrow)
p.title("x,y vs t")

w,mag,phi,t1,v_out1,t2,v_out2 = Q56()

#Plots for magnitude and phase responses of Q5 are generated
p.figure(9)
p.subplot(2,1,1)
p.semilogx(w,mag)
p.grid(True)
p.xlabel("Frequency (in rad/s)"+arrow)
p.ylabel("Magnitude of H(s) (in dB)"+arrow)
p.title("Magnitude response")
p.subplot(2,1,2)
p.semilogx(w,phi)
p.grid(True)
p.xlabel("Frequency (in rad/s)"+arrow)
p.ylabel("Phase of H(s) (in deg)"+arrow)
p.title("Phase response")

#Plot for output response of Q6 till 30 micro seconds is generated
p.figure(10)
p.plot(t1,v_out1)
p.grid(True)
p.xlabel("t"+arrow)
p.ylabel(r"v$_{o}$"+"(t)"+arrow)
p.title("Output voltage response (till 30 \u03BCs)")

#Plot for output response of Q6 till 10 milli seconds is generated
p.figure(11)
p.plot(t2,v_out2)
p.grid(True)
p.xlabel("t"+arrow)
p.ylabel(r"v$_{o}$"+"(t)"+arrow)
p.title("Output voltage response (till 10 ms)")

p.show()      #Show command to show all the generated plots

#End of the code




    

