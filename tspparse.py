from collections import deque
import numpy as np
from scipy.spatial import distance_matrix
from math import radians, cos, sin, asin, sqrt
 
def haversine(lon1, lat1, lon2, lat2): 
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal to radian
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    # haversine
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Earth's average radius in kilometers
    return c * r * 1000

def minimal_tsp():
    return { "COMMENT"          : ""
           , "DIMENSION"        : None
           , "TYPE"             : None
           , "EDGE_WEIGHT_TYPE" : None
           , "CITIES"           : []
           , "OPT"              : []
           , "DISTANCE_MATRIX"  : []}

def scan_keywords(tsp,tspfile):
    for line in tspfile:
        words   = deque(line.split())
        keyword = words.popleft().strip(": ")

        if keyword == "COMMENT":
            tsp["COMMENT"] += " ".join(words).strip(": ")
        elif keyword == "NAME":
            tsp["NAME"] = " ".join(words).strip(": ")
        elif keyword == "TYPE":
            tsp["TYPE"] = " ".join(words).strip(": ")
        elif keyword == "DIMENSION":
            tsp["DIMENSION"] = int(" ".join(words).strip(": "))
        elif keyword == "EDGE_WEIGHT_TYPE":
            tsp["EDGE_WEIGHT_TYPE"] = " ".join(words).strip(": ")
        elif keyword == "NODE_COORD_SECTION":
            read_cities(tsp,tspfile)
        elif keyword == "EDGE_WEIGHT_SECTION":
            read_weights(tsp,tspfile)
        elif keyword == "DISPLAY_DATA_SECTION":
            read_cities(tsp,tspfile)
        elif keyword == 'EOF':
            break

def read_int(words):
    return int(words.popleft())


def read_cities(tsp,tspfile):
    tsp['CITIES'] = np.zeros([tsp['DIMENSION'],2])
    for n in range(1, tsp["DIMENSION"] + 1):
        line  = tspfile.readline()
        decode = line.split()
        tsp["CITIES"][n-1][0] = float(decode[1])
        tsp["CITIES"][n-1][1] = float(decode[2])

def read_weights(tsp,tspfile):
    tsp['DISTANCE_MATRIX'] = np.zeros([tsp['DIMENSION'],tsp['DIMENSION']])
    for n in range(1, tsp["DIMENSION"] + 1):
        line  = tspfile.readline()
        decode = line.split()
        tsp['DISTANCE_MATRIX'][n-1] = np.array(decode)

def read_opt(tsp,path):
    optfile = open(path,'r')
    for line in optfile:
        words   = deque(line.split())
        keyword = words.popleft().strip(": ")
        if keyword == 'TOUR_SECTION':
            tsp['OPT'] = np.zeros(tsp['DIMENSION'],dtype = int)
            for n in range(tsp['DIMENSION']):
                line2 = optfile.readline()
                tsp['OPT'][n] = int(line2) - 1

            
def read_tsp_file(path):
    tspfile = open(path,'r')
    tsp     = minimal_tsp()
    scan_keywords(tsp,tspfile)
    tspfile.close()
    if tsp["EDGE_WEIGHT_TYPE"] == "EUC_2D":
        tsp['DISTANCE_MATRIX'] = distance_matrix(tsp["CITIES"],tsp["CITIES"])
    elif tsp["EDGE_WEIGHT_TYPE"] == "GEO":
        print("Unsupported coordinate type: " + tsp["EDGE_WEIGHT_TYPE"])
    opt_path = path.replace('.tsp','.opt.tour')
    read_opt(tsp,opt_path)
    return tsp

if __name__ == "__main__":
    a = read_tsp_file('a280.tsp')
    print(a)