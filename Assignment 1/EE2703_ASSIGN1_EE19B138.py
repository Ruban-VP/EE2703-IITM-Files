"""
************** Python program that prints an LTSpice netlist in reverse ************

This code reads an LTSpice netlist file, extracts the netlist data line-by-line, prints the contents in reverse in terms of the words
and reports the errors in the netlist (if any).

Done by: V. Ruban Vishnu Pandian 
Date of completion: 17/02/2021

Command line usage: python (or ipython3) EE2703_ASSIGN1_EE19B138.py <Netlist filename>
Note: Ensure that the netlist file is in the PWD (Present working directory)

In this code, a lot of print statements are used without any content in them. They just serve as newlines as in Python, a print
statement by default shifts to a newline after printing the contents present in it. These newlines are printed for aesthetic purposes
and to make the output more ordered. 
"""

from __future__ import print_function
from sys import argv, exit                      #Importing the libraries needed for the code

Circuit = '.circuit'
End = '.end'
Netlist = '.netlist'
VC = ['e','E','g','G']
CC = ['h','H','f','F']
NC = ['r','R','l','L','c','C','v','V','i','I']
volts = []
comp = VC+CC+NC
suffix = {1:'st',2:'nd',3:'rd'}
suffix.update(suffix.fromkeys([0,4,5,6,7,8,9,11,12,13],'th'))
flags = []
lines = []
contents = []                                   #Pre-defining and initialising some useful variables

if len(argv)!=2:
    print("\nNumber of arguments not sufficient. Usage: %s\n" % argv)    #If the number of arguments is not exactly 2, this error message is printed
    exit()

try:                                            #Try block opened to handle the exception of file not opening (maybe due to invalid filename)
    with open(argv[1]) as f:
        if argv[1].find(Netlist) == -1:
            print("\nThe filename provided doesn't correspond to an LTSpice netlist file. Provide a valid netlist file.\n")
                                               #If the file is not a '.netlist' file, then this error message is printed
            exit()

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
    
    if start+1 < fin:
        print("")
        for i in range(start+1, fin):                             #For loop which loops over the netlist lines
            temp = lines[fin+start-i].split()                     #Lines accessed from the end are stored in a temporary variable 'temp'
            temp2 = lines[i].split()                              #Lines accessed from the start are stored in a temporary variable 'temp2'
            if temp2 != []:
                contents.append(lines[i].split())                 #Non-empty lines accessed from the start are stored in the list 'Contents'
            if temp != []:
                n = len(temp)                                       
                for i in range(n):
                    print(temp[n-1-i], end=" ")                   #Non-empty lines accessed from the end are printed in reverse in terms of the words they have
                print("")
        print("")
    else:
        print("\nInvalid netlist\n1. '.circuit' comes after '.end' (or)\n2. Doesn't have any netlist data (or)\n3. '.circuit','.end' not found\n") 
                                        #If '.circuit' comes after '.end' or if they are missing or if they don't contain any data, this error
                                        #message is printed
        exit()
 
except IOError:
    print("\nInvalid filename. Usage %s\n" % argv)  #If the filename is not valid or if the file is not in the PWD, then this error message is printed
    exit()

for line in contents:
    if line[0][0] in ['v','V']:           #This for loop is used to store the different names voltage sources can have. All the different names
        volts.append(line[0])             #are stored in a list called 'volts'. This is used to check the validity of current controlled sources' definitions.

for i in range(len(contents)):            #For loop which loops over the lines in the netlist
    flag = 0                              #Flag variable, useful for validity checking and some print statements, is initialised with 0 
    line = contents[i]                    #Current line accessed and stored in temporary variable 'line'
    num = len(line)
    if ((i+1)%100) in suffix:
        tup = (i+1, suffix[(i+1)%100], line)
    else:
        tup = (i+1, suffix[(i+1)%10], line) #Some suffix fixing is done to display '1st', '2nd', '3rd', '4th', etc. correctly without explicit 'If' conditions
    
    #This 'If-else' ladder present below checks whether the line is having valid number of parameters, i.e., either 4 or 5 or 6. If not the appropriate
    #error message is printed depending on the case
    if num!=4 and num!=5 and num!=6:
       print("Invalid %d%s component definition: %s (Invalid number of parameters)\n" %  tup)
    elif line[0][0] in VC and (num==4 or num==5):
       print("Invalid %d%s component definition: %s (Voltage controlled source definition not present with 6 parameters)\n" % tup)
    elif line[0][0] in CC and (num==4 or num==6):
       print("Invalid %d%s component definition: %s (Current controlled source definition not present with 5 parameters)\n" % tup)
    elif line[0][0] in NC and (num==5 or num==6):
       print("Invalid %d%s component definition: %s (Non-controlled component defintion not present with 4 parameters)\n" % tup)
    else:
        flag=1  #If the line contains valid number of elements, the flag variable is changed to 1, signifying the line could be sent for data validity checking
    
    """
    The set of 'If' conditions and 'Try-Except' blocks present below check for the validity of data. This includes:

    1. Whether the component name is valid and corresponds to a valid component
    2. Whether the nodes are having alphanumeric names
    3. Whether the physical quantity corresponding to a component is a valid numerical value
    4. Whether the voltage source, whose current is a controlling current, is defined or not 

    Depending on the case, the appropriate type of error is printed. Even if one of the blocks 
    come across an invalidity, then the flag is assigned value 2, signifying that the current line is not a valid component definition
    """
    if flag==1:
        try:
            comp.index(line[0][0])
        except ValueError:
            print("Invalid %d%s component definition: %s (Invalid component name)" %  tup)
            flag=0
 
        if num!=5:
            for j in range(1, num-1):
                if line[j].isalnum() == False:
                    print("Invalid %d%s component definition: %s (Node names must be alphanumeric)" %  tup)
                    flag=0
                    break
        else:
            for j in [1,2]:
                if line[j].isalnum() == False:
                    print("Invalid %d%s component definition: %s (Node names must be alphanumeric)" %  tup)
                    flag=0
                    break

        try:
            float(line[num-1])
        except Exception as ex:
            print("Invalid %d%s component definition: %s (Invalid component value)" %  tup)
            flag=0

        if num==5:
            try:
                volts.index(line[num-2])
            except Exception as ex:
                print("Invalid %d%s component definition: %s (Voltage source pertaining to controlling current not found)" %  tup)
                flag=0

        if flag==0:
            print("")      #Print statement used for aesthetic purposes

    flags.append(flag)     #Flags are getting stored in a list named 'Flags'

if 0 in flags:
    print("These are the errors present in the netlist. Correct them and provide a valid netlist.\n") 
    #Even if atleast there's one 0, that line is not a valid component definition. Hence, this message is printed which 
    #asks the user to correct the errors present in the netlist
else:
    print("The netlist is valid.\n")
    #If the netlist contains valid data, then this message is printed which confirms to the user that the data is valid
