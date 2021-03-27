# script to generate data files for the least squares assignment
from pylab import *
import scipy.special as sp
N=101                           # no of data points
k=9                            # no of sets of data with varying noise

# generate the data points and add noise
t=linspace(0,10,N)              # t vector
y=1.05*sp.jn(2,t)-0.105*t       # f(t) vector
y.shape = (N, 1)
Y=meshgrid(y,ones(k),indexing='ij')[0] # make k copies
scl=logspace(-1,-3,k)           # noise stdev
n=dot(randn(N,k),diag(scl))     # generate k vectors
yy=Y+n                          # add noise to signal
yy2=c_[yy,y]                    # concatenate the true value column at last8
labels = []                     # list for creating the labels

for i in range(len(scl)):
    st = '\u03C3{0}'.format(chr(0x2080 + i+1))
    labels.append(st+" = %.3f" % scl[i])

labels.append("True value")

# shadow plot
plot(t,yy2)
legend(labels)
xlabel(r'$t$',size=20)
ylabel(r'$f(t) + noise$',size=20)
title(r'Q4: Data to be fitted to theory',size=20)
grid(True)
savetxt("fitting2.dat",c_[t,yy]) # write out matrix to file
show()

