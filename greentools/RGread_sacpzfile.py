# -------------------------------
#| Robert Green   GFZ Potsdam    |
#| 2017-10-09                    |
# -------------------------------
def read_sacpzfile(file):
    ''' Reads a sac format poles-zero file
    Expects ZEROS, POLES and CONSTANT as keywords
    Returns a paz dictionary  
    Gain is set to 1. 
    Sensitivity is set to CONSTANT 
    Notes about obspy pole-zero dictionaries
    (1) "poles" should be a list of tuples, e.g. [(x+yj),(r+sj)]\n
    (2) "zeros" should be a list of complexes, e.g. [0j,0j]\n",
    (3) "digitizer gain" and "seismometer gain" are floats but are 
        passive and there for reference. Multiplied together they give 
        the "sensitivity" Sensitivity is used if remove_sensitivity=true
    (4) "gain" is actually the A0 normalisation factor, the factor that 
    defines the amplitude of pole-zero curve at 1 Hz."
     '''
    from obspy.core import UTCDateTime
    fid=open(file)
    instpaz={'gain':1.}
    Z=False
    P=False
    zeros=[];poles=[]
    for line in fid:
        line=line.rstrip()
        line=line.split()
        if line[0] == 'CONSTANT':
            instpaz['sensitivity']=float(line[1])
            continue
        if line[0] == 'ZEROS':
            numofZ=int(line[1])
            Z=True
            zcount=0
            continue
        if Z:
            zeros.append(complex(float(line[0]),float(line[1])))
            zcount+=1
            if zcount == numofZ:
                Z=False
                instpaz['zeros']=zeros
        if line[0] == 'POLES':
            numofP=int(line[1])
            P=True
            pcount=0
            continue
        if P:
            poles.append(complex(float(line[0]),float(line[1])))
            pcount+=1
            if pcount == numofP:
                P=False
                instpaz['poles']=poles
    fid.close()
    return instpaz

