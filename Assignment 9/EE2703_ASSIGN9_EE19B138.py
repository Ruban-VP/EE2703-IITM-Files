"""
************** Python program to analyse spectra of non-periodic signals ****************

In this program, the in-built DFT library of python is used to compute and plot DFT of non-periodic sinusoidal signals
and their periodic extensions, analyse the effect of discontinuities on the spectrum and how the hamming window reduces
that effect, find the frequency and initial phase of a sinusoidal signal from its DFT and see how the frequency components
of a chirped signal evolve with respect to time by plotting a surface plot of the DFT.

Done by: V. Ruban Vishnu Pandian 
Date of completion: 12/05/2021

Command line usage: ipython3 EE2703_ASSIGN9_EE19B138.py 
"""

import pylab as p      #Importing the required library 

#Function Q1(): This function basically contains all the example codes present in the assignment with some changes.
def Q1():

    #Code snippet to find and plot the DFT of periodic extension of sin(sqrt(2)t) with period = 2pi
    t = p.linspace(-p.pi,p.pi,65); t = t[:-1]
    y = p.sin(p.sqrt(2)*t)
    y[0] = 0
    y = p.fftshift(y)
    Y = p.fftshift(p.fft(y))/64
    w = p.linspace(-32,32,65); w = w[:-1]
    p.figure(1)
    p.subplot(2,1,1)
    p.plot(w,abs(Y))
    p.xlim([-10,10])
    p.title(r"Spectrum of $\sin\left(\sqrt{2}t\right)$")
    p.ylabel(r"$|Y|$")
    p.grid(True)
    p.subplot(2,1,2)
    p.plot(w,p.angle(Y),'ro')
    p.xlim([-10,10])
    p.xlabel(r"$\omega$")
    p.ylabel(r"Phase of Y")             
    p.grid(True)                       

    #Code snippet to plot the actual sin(sqrt(2)t) function and its periodic extension for three periods
    t1 = p.linspace(-p.pi,p.pi,65); t1 = t1[:-1]
    t2 = p.linspace(-3*p.pi,-p.pi,65); t2 = t2[:-1]
    t3 = p.linspace(p.pi,3*p.pi,65); t3 = t3[:-1]
    y = p.sin(p.sqrt(2)*t1)
    p.figure(2)
    p.plot(t1,p.sin(p.sqrt(2)*t1),'b')
    p.plot(t2,p.sin(p.sqrt(2)*t2),'r')
    p.plot(t3,p.sin(p.sqrt(2)*t3),'r')
    p.ylabel(r"$y$")
    p.xlabel(r"$t$")
    p.title(r"$\sin\left(\sqrt{2}t\right)$")
    p.grid(True)
    p.figure(3)
    p.plot(t1,y,'b')
    p.plot(t2,y,'r')
    p.plot(t3,y,'r')
    p.ylabel(r"$y$")
    p.xlabel(r"$t$")
    p.title(r"Periodic repetition of $\sin\left(\sqrt{2}t\right)$ with period 2$\pi$ and N=64")
    p.grid(True)

    #Code snippet to find and plot the magnitude of DFT of periodic extension of the signal y=t
    #with t in the interval [-pi,pi) (Period=2pi) on a logarithmic scale (dB-dec plot)
    t = p.linspace(-p.pi,p.pi,65); t = t[:-1]
    y = t
    y[0] = 0 
    y = p.fftshift(y) 
    Y = p.fftshift(p.fft(y))/64
    w = p.linspace(-32,32,65); w = w[:-1]
    p.figure(4)
    p.semilogx(abs(w),20*p.log10(abs(Y)))
    p.xlim([1,10])
    p.ylim([-20,0])
    p.ylabel(r"$|Y|$ (dB)")
    p.title(r"Spectrum of a digital ramp")
    p.xlabel(r"$\omega$")
    p.grid(True)

    #Code snippet to plot the periodic extension of the windowed version of sin(sqrt(2)t) with period = 2pi
    #for three periods
    t1 = p.linspace(-p.pi,p.pi,65); t1 = t1[:-1]
    t2 = p.linspace(-3*p.pi,-p.pi,65); t2 = t2[:-1]
    t3 = p.linspace(p.pi,3*p.pi,65); t3 = t3[:-1]
    n = p.arange(64)
    wnd = p.fftshift(0.54+0.46*p.cos(2*p.pi*n/63))
    y = p.sin(p.sqrt(2)*t1)*wnd
    p.figure(5)
    p.plot(t1,y,'b')
    p.plot(t2,y,'r')
    p.plot(t3,y,'r')
    p.ylabel(r"$y$")
    p.xlabel(r"$t$")
    p.title(r"$\sin\left(\sqrt{2}t\right)\times w(t)$ with $t$ wrapping every $2\pi$ ")
    p.grid(True)

    #Code snippet to find and plot the DFT of the windowed sin(sqrt(2)t) signal with period 2pi
    y[0] = 0
    y = p.fftshift(y)
    Y = p.fftshift(p.fft(y))/64
    w = p.linspace(-32,32,65); w = w[:-1]
    p.figure(6)
    p.subplot(2,1,1)
    p.plot(w,abs(Y))
    p.xlim([-8,8])
    p.title(r"Spectrum of $\sin\left(\sqrt{2}t\right)\times w(t)$")
    p.ylabel(r"$|Y|$")
    p.grid(True)
    p.subplot(2,1,2)
    p.plot(w,p.angle(Y),'ro')
    p.xlim([-8,8])
    p.xlabel(r"$\omega$")
    p.ylabel(r"Phase of Y")
    p.grid(True)

    #Code snippet to plot the periodic extension of the windowed version of sin(sqrt(2)t) with period = 8pi
    #for three periods
    t1 = p.linspace(-4*p.pi,4*p.pi,257); t1 = t1[:-1]
    t2 = p.linspace(-12*p.pi,-4*p.pi,257); t2 = t2[:-1]
    t3 = p.linspace(4*p.pi,12*p.pi,257); t3 = t3[:-1]
    n = p.arange(256)
    wnd = p.fftshift(0.54+0.46*p.cos(2*p.pi*n/256))
    y = p.sin(p.sqrt(2)*t1)*wnd
    p.figure(7)
    p.plot(t1,y,'b')
    p.plot(t2,y,'r')
    p.plot(t3,y,'r')
    p.ylabel(r"$y$")
    p.xlabel(r"$t$")
    p.title(r"Periodic repetition of $\sin\left(\sqrt{2}t\right)\times w(t)$ with period 8$\pi$ and N=256")
    p.grid(True)

    #Code snippet to find and plot the DFT of the windowed sin(sqrt(2)t) signal with period 8pi (For better resolution)
    y[0] = 0 
    y = p.fftshift(y) 
    Y = p.fftshift(p.fft(y))/256
    w = p.linspace(-32,32,257); w=w[:-1]
    p.figure(8)
    p.subplot(2,1,1)
    p.plot(w,abs(Y),'b')
    p.xlim([-4,4])
    p.ylabel(r"$|Y|$")
    p.title(r"Spectrum of $\sin\left(\sqrt{2}t\right)\times w(t)$")
    p.grid(True)
    p.subplot(2,1,2)
    p.plot(w,p.angle(Y),'ro')
    p.xlim([-4,4])
    p.ylabel(r"Phase of $Y$")
    p.xlabel(r"$\omega$")
    p.grid(True)

#Function Q2(): To find and plot the DFT of cube of cos(0.86t). It accepts the time range limit, number of 
#samples and flag value as inputs. Flag will determine whether the signal must be windowed or not.
def Q2(T0,N,flag):
    t = p.linspace(-T0,T0,N+1); t = t[:-1]
    y = p.fftshift(p.cos(0.86*t)**3)
    n = p.arange(N)
    wnd = 0.54+0.46*p.cos(2*p.pi*n/(N-1))
    if flag==1:
        y = y*wnd
    Y = p.fftshift(p.fft(y))/N
    Ts = 2*T0/N
    w = p.linspace(-p.pi/Ts,p.pi/Ts,N+1); w = w[:-1]
    
    p.subplot(2,1,1)
    p.plot(w,abs(Y))
    p.xlim([-8,8])
    p.ylabel(r"$|Y|$")
    if flag==1:
        p.title(r"Spectrum of cos$^3$(0.86t) with hamming window")
    else:
        p.title(r"Spectrum of cos$^3$(0.86t) without hamming window")
    p.grid(True)
    p.subplot(2,1,2)
    p.plot(w,p.angle(Y),'ro')
    p.xlim([-8,8])
    p.ylabel(r"Phase of $Y$")
    p.xlabel(r"$\omega$")             
    p.grid(True)

#Function Q3_4(): To find and plot the DFT of cos(wo*t+delta). It accepts wo, delta,time range limit, number of samples 
#and flag value as inputs. Flag will determine whether the white noise must be added or not.
def Q3_4(w0,delta,T0,N,flag):
    t = p.linspace(-T0,T0,N+1); t = t[:-1]
    y = p.fftshift(p.cos((w0*t)+delta))
    noise = 0.1*p.randn(N)
    if flag==1:
        y = y+noise
    Y = p.fftshift(p.fft(y))/N
    Ts = 2*T0/N
    w = p.linspace(-p.pi/Ts,p.pi/Ts,N+1); w = w[:-1]
 
    p.subplot(2,1,1)
    p.plot(w,abs(Y))
    p.xlim([-4,4])
    p.ylabel(r"$|Y|$")
    p.title(r"Spectrum of cos(w$_0$t+$\delta$)")
    p.grid(True)
    p.subplot(2,1,2)
    p.plot(w,p.angle(Y),'ro')
    p.xlim([-4,4])
    p.ylabel(r"Phase of $Y$")
    p.xlabel(r"$\omega$")
    p.grid(True)

    if flag==1:
        print("With white noise:")
    else:
        print("Without white noise:")

    Ymag = abs(Y)
    pos1 = p.where(w>=0)[0]
    pos2 = p.where(Ymag[pos1]>0.25)[0]
    Y_abs_new = Ymag[pos1[pos2]]
    w_new = w[pos1[pos2]]
    w_eff = sum(Y_abs_new*w_new)/sum(Y_abs_new)          #Code snippet to estimate and print wo from the DFT data
    print("The estimated frequency w0 = %.3f" % w_eff) 

    Yphase = p.angle(Y)
    pos1 = p.where(w>=w_eff)[0]
    pos2 = p.where(w<=w_eff)[0]
    a = (w[pos2])[-1]; b = (w[pos1])[0]
    if (w_eff-a)<=(b-w_eff):
        phase_eff = (Yphase[pos2])[-1]
    else:
        phase_eff = (Yphase[pos1])[0]                    #Code snippet to estimate and print delta from the DFT data
    print("The estimated phase \u03B4 (in Rad) = %.3f" % phase_eff)
    print("")

#Function Q5(): To find and plot the DFT of the chirped signal whose frequency increases linearly with time.
#The input paramters are the time range limit and the number of samples.
def Q5(T0,N):
    t = p.linspace(-T0,T0,N+1); t = t[:-1]
    arg = 16*t*(1.5+(t/(2*p.pi)))
    y = p.fftshift(p.cos(arg))
    Y = p.fftshift(p.fft(y))/N
    Ts = 2*T0/N
    w = p.linspace(-p.pi/Ts,p.pi/Ts,N+1); w = w[:-1]

    p.subplot(2,1,1)
    p.plot(w,abs(Y))
    p.xlim([-100,100])
    p.grid(True)
    p.ylabel(r"$|Y|$")
    p.title(r"Spectrum of the chirped signal cos(16(1.5+t/2$\pi$)t)")
    p.subplot(2,1,2)
    p.plot(w,p.angle(Y),'ro')
    p.xlim([-100,100])
    p.ylabel(r"Phase of $Y$")
    p.xlabel(r"$\omega$")
    p.grid(True)

#Function Q6(): This function splits the 1024 vector made of the chirp signal values into segments of 64 samples,
#finds the DFT for each segment and plots the DFT magnitude as a surface plot with the x,y axes as frequency and time
#axes respectively. This is done to see how the frequency changes with the time in a chirped signal
def Q6(num):
    t = p.linspace(-p.pi,p.pi,1025); t = t[:-1]
    arg = 16*t*(1.5+(t/(2*p.pi)))
    y = p.cos(arg)
    y = y.reshape(16,64)
    DFT_mat = p.zeros((16,64))
    for i in range(16):
        DFT_mat[i,:] = abs(p.fftshift(p.fft(y[i,:]))/64)

    t_axis = t.reshape(16,64)
    t_axis = p.mean(t_axis, axis=1)
    w_axis = p.linspace(-512,512,65); w_axis = w_axis[:-1]
    ii = p.where(abs(w_axis)<=150)[0]
    wv, tv = p.meshgrid(w_axis[ii],t_axis)

    fig2 = p.figure(num)
    ax = fig2.add_subplot(111, projection='3d')
    surf = ax.plot_surface(wv, tv, DFT_mat[:,ii], cmap=p.cm.get_cmap("plasma"))
    p.colorbar(surf,shrink=0.5,label="|Y| values")
    ax.set_xlabel(r"$\omega$")
    ax.set_ylabel(r"$t$")
    ax.set_zlabel(r"$|Y|$")
    ax.set_title("Surface plot of DFTs of various portions of the chirped signal")
    
Q1()

p.figure(9)
Q2(4*p.pi,512,0)

p.figure(10)
Q2(4*p.pi,512,1)

p.figure(11)
Q3_4(1.2,0.78,8*p.pi,1024,0)

p.figure(12)
Q3_4(1.2,0.78,8*p.pi,1024,1)

p.figure(13)
Q5(p.pi,1024)

Q6(14)             #All the 6 functions are called and the input parameters are accordingly given
 
p.show()           #Show command to show all the generated plots
#End of the code