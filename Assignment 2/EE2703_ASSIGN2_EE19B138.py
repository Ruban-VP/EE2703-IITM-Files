"""
************** Python program to solve a linear circuit netlist ************

This code reads an LTSpice netlist file, solves for the node voltages and currents through voltage sources and prints the 
AC and DC components seperately.

Done by: V. Ruban Vishnu Pandian 
Date of completion: 24/02/2021

Command line usage: ipython3 EE2703_ASSIGN2_EE19B138.py <Netlist filename>
Note: Ensure that the netlist file is in the PWD (Present working directory)

In this code, a lot of print statements are used without any content in them. They just serve as newlines as in Python, a print
statement by default, shifts to a newline after printing the contents present in it. These newlines are printed for aesthetic purposes
and to make the output more ordered. 

General instructions:

1. Don't address a single node by two different names. Provide it a unique name and use only it in the lines where you want to define that node.
2. Don't address components connected across different node pairs with the same name. Provide them with distinct names.
3. If the sources are purely DC, then there is no need of the .ac line. Don't add it if all the sources are DC as it would cause an error.
4. DC sources can be present even if the frequency of operation is non-zero. The code will print the seperate components.
5. This code does not support controlled sources. So don't use this code to solve circuits with controlled sources.
6. This code works under the assumption that the circuit is operated under a single frequency which is given in the line: '.ac' <Frequency in Hertz>.
7. Assign one node as a 'GND' node. Netlist without any ground nodes can't be processed by this code.
"""

from __future__ import print_function
from sys import argv, exit    
import numpy as np                   
import cmath                           #Importing the libraries needed for the code

acflag=0
Circuit = '.circuit'
End = '.end'
Netlist = '.netlist'
passives = ['r','R','l','L','c','C']
sources = ['v','V','i','I']
comp = passives+sources
suffix = {1:'st',2:'nd',3:'rd'}
suffix.update(suffix.fromkeys([0,4,5,6,7,8,9,11,12,13],'th'))

w=0               #By default, AC angular frequency is zero
dc_w = 1e-50      #DC angular frequency is zero in theory. But to avoid infinte admittance due to inductors, a very small DC angular frequency
                  #which is 1e-50 is defined
flags = []
lines = []
contents = []                                   
vardict = {'GND':0}
volts = []                         #Pre-defining and initialising some useful variables


#The three functions present below are the companion functions which help us form the conductance matrix and the source vector

def RLC(mat, n1, n2, value):
    mat[n1][n1] += value
    mat[n1][n2] -= value
    mat[n2][n1] -= value
    mat[n2][n2] += value
    return mat

def Volt(mat, vec, n1, n2, tu, value):
    mat[n1][tu] = mat[tu][n1] = 1
    mat[n2][tu] = mat[tu][n2] = -1
    vec[tu] = value
    return mat, vec

def Curr(vec, n1, n2, value):
    vec[n1] -= value
    vec[n2] -= value
    return vec

if len(argv)!=2:
    print("\nNumber of arguments not sufficient. Usage: %s\n" % argv)    #If the number of arguments is not exactly 2, this error message is printed
    exit()

try:                                            #Try block opened to handle the exception of file not opening (maybe due to invalid filename)
    with open(argv[1]) as f:
        if argv[1].find(Netlist) == -1:
            print("\nThe filename provided doesn't correspond to an LTSpice netlist file. Provide a valid netlist file.\n")
            exit()                #If the file is not a '.netlist' file, then this error is printed

        for line in f.readlines():
            lines.append((line.split('#')[0]).replace("\n",""))   #File is read and the lines are stored in a list called 'Lines'
                                                                  #The lines are also filtered from comments and the newlines are removed
    f.close()                                                     #File closed after contents are obtained

    
    try:                                                          #Try block opened to handle the exception of '.circuit' or '.end' not being found
        start = lines.index(Circuit)                              
        fin = lines.index(End)                                    #Locations of lines '.circuit' and '.end' are stored
    except ValueError:
        start = 2                                                 #If '.circuit' and '.end' aren't found, variables start and end are assigned values
        fin = 1                                                   #in such a way that start exceeds end (Characteristic of an invalid netlist)
    """
    The if-else block given below reads the netlist, splits the lines into tokens ans stores it into a list called 'contents'.
    Also this if block detects if any .ac line is present. If it is present, it stores the frequency into a variable called 'w' and assigns
    1 to a variable known as 'acflag' 
    """
    if start+1 < fin: 
        for i in range(start+1,fin):                 
            temp = lines[i].split()                              
            if temp != []:
                if temp[0]=='.ac':
                    try:
                        w = 2*np.pi*float(temp[1])
                        if w==0:
                            print("\nFrequency is zero meaning the sources are DC. So remove the ac tag and provide a single line definition for the DC source.")
                            print("For example:\n.ac 0\nV1 n1 GND ac 20 0\nV1 n1 GND dc 5")
                            print("is an invalid definition since the frequency is already zero. Instead you should provide:")
                            print("V1 n1 GND dc 25\n(ac line should not be there since the sources are anyway DC)\n")
                            exit()     #If .ac line contains frequency as zero, this error message is printed
                        else:
                            acflag=1
                    except Exception as Ex:
                        print("\nFrequency is not a valid number. Provide a correct numerical value.\n")
                        exit()
                else:
                    contents.append(lines[i].split())    
    else:
        print("\nInvalid netlist\n1. '.circuit' comes after '.end' (or)\n2. Doesn't have any netlist data (or)\n3. '.circuit','.end' not found\n") 
        exit()           #If the netlist doesn't contain any data or if the .circuit and .end lines aren't placed correctly, this error message is printed


except IOError:
    print("\nInvalid filename. Usage %s\n" % argv)  #If the filename is not valid or if the file is not in the PWD, then this error message is printed
    exit()

print("")
"""
Error checking For loop:
                        The for loop present below basically detects the standard errors that could be present in the netlist. Some of the examples are 
the node names being non-alphanumeric, the values being special chaarcters instead of digits, etc. The types of errors that are detected by this for loop 
are listed below:

1. Validity of component name
2. Number of parameters in the component definition
3. Checking whether node names are alphanumeric
4. Checking whether Ac sources contain the 'ac' tag/ DC sources contain the 'dc' tag
5. Validity of the values of the components
"""
for i in range(len(contents)):            
    flag=0
    line = contents[i] 
    num = len(line)
    if ((i+1)%100) in suffix:
        tup = (i+1, suffix[(i+1)%100], line)
    else:
        tup = (i+1, suffix[(i+1)%10], line) #Some suffix fixing is done to display '1st', '2nd', '3rd', '4th', etc. correctly without explicit 'If' conditions

    if line[0][0] not in comp: 
        print("Invalid %d%s component definition: %s (Invalid component name)\n" %  tup) 
    elif line[0][0] in comp and (num!=4 and num!=5 and num!=6):
        print("Invalid %d%s component definition: %s (Invalid number of parameters)\n" %  tup)
    elif line[0][0] in passives and num!=4:
        print("Invalid %d%s component definition: %s (Passive component definition not present with 4 parameters)\n" %  tup)                           
    else:
        flag=1

        for temp in [line[1], line[2]]:
            if temp.isalnum() == False:
                print("Invalid %d%s component definition: %s (Node names should be alphanumeric)" %  tup); flag=0 
                break  

        if line[0][0] in passives:
            try:
                float(line[num-1])
            except Exception as ex:
                print("Invalid %d%s component definition: %s (Invalid component value)" %  tup); flag=0 
        
        elif line[0][0] in sources:
            if acflag==0:
                if len(line)==5 and line[3] not in ['dc','DC','Dc','dC']:
                    print("Invalid %d%s component definition: %s (DC source definition with 5 parameters doesn't have a 'dc' tag)" %  tup); flag=0

                if len(line)==6:
                    print("Invalid %d%s component definition: %s (DC source definition has 6 parameters which is not valid)" %  tup); flag=0
                elif len(line)!=6:
                    try:
                        float(line[num-1])
                    except Exception as ex:
                        print("Invalid %d%s component definition: %s (Invalid component value)" %  tup); flag=0

            elif acflag==1:
                if len(line)==6 and line[3] not in ['ac','AC','Ac','aC']:
                    print("Invalid %d%s component definition: %s (AC source definition doesn't have an 'ac' tag)" %  tup); flag=0
                elif len(line)==5 and line[3] not in ['dc','DC','Dc','dC']:
                    print("Invalid %d%s component definition: %s (DC source definition with 5 parameters doesn't have a 'dc' tag)" %  tup); flag=0

                if len(line)==6:
                    try:
                        float(line[num-1])
                        float(line[num-2])
                    except Exception as ex:
                        print("Invalid %d%s component definition: %s (Invalid component value)" %  tup); flag=0
                else:
                    try:
                        float(line[num-1])
                    except Exception as ex:
                        print("Invalid %d%s component definition: %s (Invalid component value)" %  tup); flag=0

        if flag==0:
            print("")

    flags.append(flag) #Basically the line is errorless if the 'flag' variable is 1 at this point. Even if the for loop detects one error, the flag will
                       #become 0. Hence, all flags are stored in a list 'flags' so that even if one of them is zero, an error message can be printed

for f in flags:
    if f==0:
        print("These are the errors present in the netlist. Correct them and provide a valid netlist.\n") 
        exit()         #This if block checks whether the 'flags' list contains atleast one zero flag. If yes, then this message is printed asking the user
                       #to provide a valid netlist

"""
For loop to determine the conductance matrix dimensions:
                                                        The variables which must be solved are the node voltages and currents through voltage sources.
To determine how may such variables are present in a given netlist, the following For loop is used. It checks whether a node/voltage source is already
read or not. If not,then it adds the uppercase node name to a dictionary named 'vardict' as a key and assigns it a numerical value 'count'. Count basically
keeps track of how may distinct variables have been read so far. In case a voltage source is read, the current through it should also be treated as a seperate
variable. To do this, the tuple containing the from and to node names (Eg: (N1, GND)) is added as a key to the dictionary 'vardict' and 'count' is assigned 
as its value. The 'vardict' dictionary is initialised with key='GND' and value=0 by default. 
"""
count=1; 
for line in contents:
    temp1 = line[1].upper()
    temp2 = line[2].upper()
    tup = (temp1, temp2)

    if temp1 not in vardict:
        vardict[temp1]=count; count += 1
    if temp2 not in vardict:
        vardict[temp2]=count; count += 1
    if (line[0][0] in ['v','V']) and (line[0] not in volts):
        vardict[tup]=count; count += 1; volts.append(line[0])    #A list 'volts' is used to keep track of how many distinct voltage sources have been read

"""
Four numpy arrays are initialised:

1. Conductance matrix AC (con_mat_ac)
2. Source vector AC (sor_vec_ac)
3. Conductance matrix DC (con_mat_dc)
4. Source vector DC (sor_vec_dc)    
"""
con_mat_ac = np.zeros((count, count), dtype=complex)
con_mat_dc = np.zeros((count, count), dtype=complex)
sor_vec_ac = np.zeros((count,1), dtype=complex)
sor_vec_dc = np.zeros((count,1), dtype=complex)         

"""
Matrices/Source vectors forming For loop:
                                         This for loop reads the lines, detects the type of element and based on it, it updates the conductance matrices and
source vectors. It also checks whether there are any AC sources and updates the con_mat_ac and sor_vec_ac arrays seperately. There is one special case.
When we have DC inputs, inductors offer infinite admittance at steady state. Hence, to practically implement it, a small value which is 1e-50 is considered
as the DC angular frequency.  
"""
for line in contents:
    num = len(line)
    val = float(line[num-1])
    temp = line[0][0]
    temp1 = line[1].upper()
    temp2 = line[2].upper()
    a = vardict[temp1]
    b = vardict[temp2]
    if temp in ['v','V']:
        c = vardict[(temp1, temp2)]

    if temp in ['r','R']:
        con_mat_dc = RLC(con_mat_dc, a, b, 1/val)

    elif temp in ['c','C']:
        g = 1j*dc_w*val
        con_mat_dc = RLC(con_mat_dc, a, b, g)

    elif temp in ['l','L']:
        g = 1/(1j*dc_w*val)
        con_mat_dc = RLC(con_mat_dc, a, b, g)
    
    elif temp in ['v','V'] and num!=6:
        con_mat_dc, sor_vec_dc = Volt(con_mat_dc, sor_vec_dc, a, b, c, val)
    
    elif temp in ['i','I'] and num!=6:
        sor_vec_dc = Curr(sor_vec_dc, a, b, val)                  #The DC arrays get updated

    if acflag==1:
        if temp in ['r','R']:
            con_mat_ac = RLC(con_mat_ac, a, b, 1/val)
       
        elif temp in ['c','C']:
            g = 1j*w*val
            con_mat_ac = RLC(con_mat_ac, a, b, g)
       
        elif temp in ['l','L']:
            g = 1/(1j*w*val)
            con_mat_ac = RLC(con_mat_ac, a, b, g)
       
        elif temp in ['v','V'] and num==6:
            amp = float(line[num-2])/2
            phasor = amp*np.exp(1j*val*np.pi/180)
            con_mat_ac, sor_vec_ac = Volt(con_mat_ac, sor_vec_ac, a, b, c, phasor)

        elif temp in ['i','I'] and num==6:
            amp = float(line[num-2])/2
            phasor = amp*np.exp(1j*val*np.pi/180)
            sor_vec_ac = Curr(sor_vec_ac, a, b, phasor)        #If 'acflag'==1, i.e., if there are AC sources, then the AC arrays are also updated

con_mat_ac[0] = con_mat_dc[0] = 0             #The first row of the matrices correspond to the KVL equation of the GND node, i.e., V_Gnd = 0
sor_vec_ac[0] = sor_vec_dc[0] = 0             #Hence, the first element of first row is set to 1. Also, the first element of the source vectors
con_mat_ac[0][0] = con_mat_dc[0][0] = 1       #are set to zero. Basically, this will translate into the equation: V_Gnd = 0

flag1 = flag2 = 0
if np.linalg.det(con_mat_dc)!=0 and not np.all((sor_vec_dc == 0)):
    dc_vals = np.linalg.solve(con_mat_dc, sor_vec_dc)
    flag1 = 1

if np.linalg.det(con_mat_ac)!=0 and not np.all((sor_vec_ac == 0)):
    ac_vals = np.linalg.solve(con_mat_ac, sor_vec_ac)         #These two if blocks solve for the variables vectors: dc_vals and ac_vals. 
    flag2 = 1  


#If the solutions are available, then they are printed with the details, i.e., which node voltage is being printed, which current is being printed, etc.
#Else, a message is displayed telling either there are no DC/AC sources or the solution does not exist. This applies for both the if blocks present below
#Also if you see voltage or current values dropping to low, say 2.51e-29, it mostly means they are zero (Unless the inputs themselves are that low).
#But assuming nominal limits for inputs, these low values correspond to actual zeros.
if flag1==1:
    print("The DC output values are (Currents flow from first node to second node):\n")
    for key in vardict:
        mag, ang = cmath.polar(dc_vals[vardict[key]])
        if abs(ang)<(cmath.pi/2):                         #If the phase in DC is less than 90 deg, the DC voltage (or current) is positive
            temp_mag = mag
        else:                                             #Else it's negative (Note that cmath.polar returns a phase in range (-pi, pi])
            temp_mag = -mag
        
        if type(key) is tuple:
            tup = (key[0], key[1], temp_mag)
            print("Current through voltage source present between node %s and node %s is: %e" % tup)
        else:
            tup = (key, temp_mag)
            if key=='GND':
                print("Voltage of node %s is: %f" % tup)
            else:
                print("Voltage of node %s is: %e" % tup)
else:
    print("Either no non-zero DC sources are present (or) DC steady state solution not present")

print("")

if flag2==1:
    print("The AC output values (magnitude, phase in degrees) are (Currents flow from first node to second node):\n")
    for key in vardict:
        val = cmath.polar(ac_vals[vardict[key]])
        if type(key) is tuple:
            tup = (key[0], key[1], val[0], val[1]*180/np.pi)
            print("Current through voltage source present between node %s and node %s is: %e, %f" % tup)
        else:
            tup = (key, val[0], val[1]*180/np.pi)
            if key=='GND':
                print("Voltage of node %s is: %f, %f" % tup)
            else:
                print("Voltage of node %s is: %e, %f" % tup)
else:
    print("Either no non-zero AC sources are present (or) AC steady state solution not present")

print("") #For aesthetic purposes
#End of the code

