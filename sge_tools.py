def sge_qacct_parse(filename):
    # Import libraries
    import pandas as pd
    
    # Parse qacct log file into dictionary 
    dicts=[]
    with open(filename, 'r') as f: 
        d = {}
        for line in f:
            if line[0:3] == "===" or line[0:18] == 'Total System Usage':
                dicts.append(d)
                d = {}
                continue
            if line[0:13] == "    WALLCLOCK":
                break
            field = line[0:13].strip()
            value = line[13:-1].strip()
            d[field] = value
    
    
    # Load data into dataframe and set correct types
    df = pd.DataFrame(dicts)
    floatfields = ['priority','ru_wallclock','ru_utime','ru_stime','ru_maxrss','ru_ixrss','ru_ismrss','ru_idrss',               'ru_isrss','ru_minflt','ru_majflt','ru_nswap','ru_inblock','ru_oublock','ru_msgsnd','ru_msgrcv',               'ru_nsignals','ru_nvcsw','ru_nivcsw','cpu','mem','io','iow','maxvmem']
    convert2Gb = {'T':1024.,'G':1.,'M':1./1024.,'K':1./1024./1024}
    for field in floatfields: 
        try: 
            df[field] = df[field].astype('float')
        except ValueError:
            df[field] = df[field].apply(lambda s: float(s[:-1])*convert2Gb[s[-1]])
            df[field] = df[field].astype('float')
    datefields = ['qsub_time','start_time','end_time']
    for field in datefields: 
        df[field] = pd.to_datetime(df[field])  #,format='%m/%d/%y %I:%M%p'
    intfields = ['slots','jobnumber','exit_status'] 
    for field in intfields: 
        df[field] = df[field].astype('int')

    return df

