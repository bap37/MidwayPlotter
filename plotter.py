#!/usr/bin/env python
import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

import argparse
from argparse import RawTextHelpFormatter
parser=argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, prefix_chars='@')
from scipy.stats import binned_statistic
import distutils.util 

parser.add_argument('@@FITRES', help='The location of your FITRES file that you need plotted. You can give a space delineated list of two different FITRES files. Please make sure they are named differently, as their names (not full filepath) will be used for labeling.', nargs="+")
parser.add_argument('@@VARIABLE', help="""The variable you want to plot. Needs to be a valid FITRES parameter. \n
If you give only one value, this will generate a histogram. If you give two colon delimited values, such as zCMB:mB it will plot zCMB (x) vs mB (y)""", nargs="+")
parser.add_argument('@@BOUNDS', default='loose', help=
"""loose (default): bounds are maximum and minimum values of specified parameter. \n 
Custom: Give a set of numbers, colon delimited. An example is min:max:binsize \n
Please note, if you are doing a two dimensional plot, you need to specify both x and y sets in order. The binsize will not be used. """, nargs = '+') 
parser.add_argument('@@SAVE', default='None', help=
"""File format to save images as. Default does not save images.""")

args = parser.parse_args()
VARIABLE = args.VARIABLE
FILENAME = args.FITRES
BOUNDS = args.BOUNDS
FORMAT = args.SAVE

def NAndR(filename):                                                                                                                                                                    
    """Takes in a FITRES file and outputs the variable names and startline for the data                                                                                                                                                                                                                                                                                        
    Outputs are [Names, Startrow]. List and number respectively.                                                                                                                        
    """                                                                                                                                                                                 
    with open(filename) as fp:                                                                                                                                                          
        for i, line in enumerate(fp):                                                                                                                                                   
            if line.startswith('VARNAMES:'):                                                                                                                                            
                line = line.replace(',',' ')                                                                                                                                            
                line = line.replace('\n','')                                                                                                                                            
                Names = line.split()                                                                                                                                                    
            elif line.startswith('SN'):                                                                                                                                                 
                Startrow = i                                                                                                                                                            
                break                                                                                                                                                                   
    return Names, Startrow  


boundsdic = {} 
if (len(BOUNDS) != 5):
    for n,i in enumerate(BOUNDS):                 
        BND = i.split(':')            
        while('' in BND): #Strip empty strings                 
            BND.remove('')                           
        boundsdic[n] = [float(i) for i in BND] 

namedic = {} #Will be used for tracking labels in the plot

for n,l in enumerate(FILENAME): #Using n as an integer to track if we've got one or two files, and what to do.
    print("Loading ",l.split("/")[-1], "...")
    namedic[n] = l.split("/")[-1] #Here we split on /, then save the last entry of each filepath to a dictionary. This last entry is always the filename, which will be used for labels.
    try:
        Names1, StartRow1 = NAndR(l) #Get info on where to start reading the file
    except FileNotFoundError or NameError:
        print('Could not find the FITRES you specified!')
        print("You were pointing to: ", FILENAME)
        sys.stdout.flush() # "dad! dad! look what got caught in the snare!" "good work, timmy, its AttributeError for dinner tonight" -Ross
        quit() #Quits if one or more files is missing
    if n == 0: #There's probably a cleaner way to do this, but this forces df1 to always be the first file loaded
        df1 = pd.read_csv(l, header=None, skiprows=StartRow1,names=Names1, delim_whitespace=True, skip_blank_lines=True, error_bad_lines=False, comment='#')
        print("Done loading!")
    else: #And df2 is the second.
        df2 = pd.read_csv(l, header=None, skiprows=StartRow1,names=Names1, delim_whitespace=True, skip_blank_lines=True, error_bad_lines=False, comment='#')
        print("Done loading!")


try:
    if namedic[0] == namedic[1]:
        print("Your filenames are identical! I'm going to go up a level and use the directory name instead of the filename.")
        for n,l in enumerate(FILENAME): #Using n as an integer to track if we've got one or two files, and what to do.                    
            print("Renaming... ",l.split("/")[-1], "..." )                                                  
            try:
                namedic[n] = l.split("/")[-2]
                print("Renamed", l.split("/")[-1], " to ", l.split("/")[-2])
            except IndexError:
                print(namedic[n], " is in your current directory. I won't rename this one.")

        if namedic[0] == namedic[1]:
            print("Both the filenames and their directories are identical. This means that you either gave me the same file twice, or you need to change some file or directory names. Quitting..")
            quit()
except KeyError: 
    pass

plotdic = {} #Used for tracking what to plot. For each file, we can accept two types of input.
#The first is a single variable, eg, c.
#Or, we can accept c:x1. We'll split on :, and then save it to plotdic in order. 
for n,i in enumerate(VARIABLE):
    VAR = i.split(':')
    while('' in VAR): #Strip empty strings
        VAR.remove('')
    plotdic[n] = VAR



for q in list(plotdic): #q in plotdic gives a list of strings of len = 1 or 2
    for i in plotdic[q]: #This takes the list and just converts it to strings
        if i not in list(df1): #Then we make sure everything's a valid parameter.
            print('You need to give a valid variable to look at! You gave me', plotdic[q])
            print('Please check your FITRES file. Quitting...')
            quit()


if (BOUNDS == 'loose') or (BOUNDS[0] == 'loose'): #checking to see if BOUNDS is default                   
    try:
        lower = min(np.amin(df1[VAR[0]].values), np.amin(df2[VAR[0]].values))
        upper = max(np.amax(df1[VAR[0]].values), np.amax(df2[VAR[0]].values))
    except NameError:
        lower = np.amin(df1[VAR[0]].values)
        upper = np.amax(df1[VAR[0]].values)
    bins = np.linspace(lower, upper, 30) #Will just use the max and min values for that parameter and 30 bins.       

elif len(BOUNDS) != 5:  #Check for custom bounds    
    bins = np.arange(boundsdic[0][0], boundsdic[0][1], boundsdic[0][2])  #Then set min, max, binsize         
else:                                           
    print('Please give a valid bounds configuration! You can use -h to find out more!') 
    print('You gave me', BOUNDS) # "oh the sweet turgid flesh of access discrepancy" - Ross                   
    print('Quitting now...')                                    
    quit()    #Quit if bounds are poorly defined.   

for n, q in enumerate(list(plotdic)): #n keeps track of what cycle we're on, while q will be used to define VAR
    VAR = plotdic[q] #This will either be length one, or two. Length one is a single parameter. Length two will be used to plot things against each other instead of a hist.
    if len(VAR) == 1: #If this is true, we're looking at a single parameter. That means we need to plot a histogram. 
        print('The upper and lower bounds are:', np.around(bins[0],4), 'and', np.around(bins[-1],4), 'respectively')
        plt.figure()
        plt.hist(df1[VAR[0]].values, bins=bins, histtype='step', lw=3, label=namedic[0], color='k') #This plots the first file
        try: #Then we try to plot the second file. If it fails, then df2 is undefined, and we quit. 
            plt.hist(df2[VAR[0]].values, bins=bins, histtype='step', lw=3, label=namedic[1]) 
        except NameError:
            pass
        plt.xlabel(VAR[0])  #In this case, VAR = [string], so we're going to strip the list.
        plt.legend()

    elif len(VAR) == 2: #however, if this is true, then we're plotting two things against each other! 
        print('Plotting', VAR[0], ' vs ', VAR[1])
        if (len(boundsdic) ==1) or (len(boundsdic) >2):
            print("You need to either give both x and y boundaries or none!")
            quit()
        plt.figure()
        plt.scatter(df1[VAR[0]].values, df1[VAR[1]].values, alpha=.3, label=namedic[0]) #This plots the first file  
        avg1 = binned_statistic(df1[VAR[0]].values, df1[VAR[1]].values, bins=bins, statistic='mean')[0]
        plt.scatter((bins[1:] + bins[:-1])/2, avg1, label=namedic[0]+" average", color='k')
        try: #Then we try to plot the second file. If it fails, then df2 is undefined, and we quit.    
            plt.scatter(df2[VAR[0]].values, df2[VAR[1]].values, alpha=.3, label=namedic[1]) #This plots the first file          
            avg2 = binned_statistic(df2[VAR[0]].values, df2[VAR[1]].values, bins=bins, statistic='mean')[0]
            plt.scatter((bins[1:] + bins[:-1])/2, avg2, label=namedic[1]+" average", color='red')
        except NameError:               
            pass          
        if len(boundsdic) != 0:
            plt.xlim(boundsdic[0][0], boundsdic[0][1])
            plt.ylim(boundsdic[1][0], boundsdic[1][1])
        plt.xlabel(VAR[0]) #In this case, VAR = [string], so we're going to strip the list.    
        plt.ylabel(VAR[1])
        plt.legend()   

if FORMAT !="None":
    plt.savefig(VARIABLE[0]+"."+FORMAT, bbox_inches="tight", format=FORMAT)
plt.show()
