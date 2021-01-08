# MidwayPlotter
Python plotter for command line usage that can plot various files and options.

Please note that you will need to enabled graphical interface in your ssh session. I believe that "ssh -KY" should suffice.

An example command is as follows: 

"plotter.py @@FITRES FITOPT000.FITRES DES.FITRES @@VARIABLE c @@BOUNDS -.4:.42:.02"

@@FITRES Space separated list of up to two file paths. Needs to be a FITRES file. If the file names are the same, the program will look in the directory they're stored and change the name to that. If the directory name is the same, it will quit. The name of the file will be used for the legend in any plots.

@@VARIABLE Can either be a single valid FITRES parameter, or a colon delimited combination, eg, x:y. If it is a colon delimited combination, the program will read it as x:y and plot a 2d graph of the relevant variables. 2D graphs include an average value. Otherwise, it will plot a histogram. Please note that for the histogram, the counts will be normalised to the first file given. Errors are Poisson noise.

@@BOUNDS default is "loose", and will use the minimum and maximum values of VARIABLE, with 30 bins. If you include two files, default will use the minimum and maximum between the two files, not just one. This can be left unspecified for the "loose" bound option.

@@SAVE Provide a filename or custom filepath to save the output to. This can be left unspecified - by default it will not save your plot.

@@DIFF A boolean value. If True, it will show the difference in the given y variable for the same CID. This can be left unspecified and will default to False.

Can also be implemented as a space delimited list of colon entries formatted as min:max:binsize. 
For a histogram, "min:max:binsize" will suffice. 
For a 2D plot, "minX:maxX:binsizeX miny:maxY:binsizeY" is necessary. The binsizeX value will be used for calculating the average value. The bisizeY parameter is not used, but needs to be a float. 
