def RF(filename):                      
    """Reads an arbitrary fitres and loads it as a pandas dataframe. """
    with open(filename) as fp:                                                                                                                                                          
        for i, line in enumerate(fp):                                                                                                                                                   
            if line.startswith('VARNAMES:'):                                                                                                                                            
                line = line.replace(',',' ')                                                                                                                                            
                line = line.replace('\n','')                                                                                                                                            
                Names = line.split()                                                                                                                                                    
            elif line.startswith('SN'):                                                                                                                                                 
                Startrow = i                                                                                                                                                            
                break                                                                                                                                                                   
    return pd.read_csv(l, header=None, skiprows=StartRow,names=Names, delim_whitespace=True, skip_blank_lines=True, error_bad_lines=False, comment='#') 
