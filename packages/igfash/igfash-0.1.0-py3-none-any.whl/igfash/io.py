# -*- coding: utf-8 -*-
"""
@author: ftong
"""
import sys
import scipy.io
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy import read_events
import numpy as np

try:    #make pandas optional as it is only used for reading csv files
    import pandas as pd
except:
    pd = lambda x: x

def read_mat_mc(matlab_file):
    mat = scipy.io.loadmat(matlab_file) #load mc data from file
    mc = np.array([mat['outVar1'][0][0][i][0][0] for i in range(0,4)])
    mc = mc[~np.isnan(mc)] #remove null values
    return mc.max() #return high mc from the list

def read_mat_pdf(matlab_file):
    mat = scipy.io.loadmat(matlab_file) #load magnitude PDF from file
    return mat['outVar2'].flatten()

def read_mat_m(matlab_file):
    mat = scipy.io.loadmat(matlab_file) #load magnitude range from file
    return mat['outVar1'].flatten()

def read_mat_cat(matlab_file, output_datenum = False, catalog_label='Catalog', mag_label='Magnitude', lat_label ='Lat', lon_label = 'Long', depth_label = 'Depth', **kwargs):
    
    print("Looking for magnitudes with label", mag_label)
    
    mag = None
    time = None
    lat = None
    lon = None
    depth = None
    
    mat = scipy.io.loadmat(matlab_file)

    try:
        mat[catalog_label]
    except KeyError:
        catalog_label='Ctg'
        try:
            mat[catalog_label]
        except KeyError:
            catalog_label='Catalog'
            try:
                mat[catalog_label]
            except KeyError:
                print("Please provide the catalog label")
                sys.exit()
    for i in range(0,len(mat[catalog_label][0])):
        
        # Extract magnitudes
        if mat[catalog_label][0][i][0]==mag_label:
            mag_frame = mat[catalog_label][0][i]
            mag = mag_frame[2].flatten()
            # continue
    
        elif mat[catalog_label][0][i][0]==lat_label:
            lat_frame = mat[catalog_label][0][i]
            lat = lat_frame[2].flatten()
            # continue
        
        elif mat[catalog_label][0][i][0]==lon_label:
            lon_frame = mat[catalog_label][0][i]
            lon = lon_frame[2].flatten()
            # continue

        elif mat[catalog_label][0][i][0]==depth_label:
            depth_frame = mat[catalog_label][0][i]
            depth = depth_frame[2].flatten()
            # continue
    
        # Extract times
        elif mat[catalog_label][0][i][0]=='Time':
            time_frame = mat[catalog_label][0][i]
            t1 = time_frame[2].flatten()
            
            if output_datenum:
                time = t1
            else:
                datenums = np.array(t1)
                t2= pd.to_datetime(datenums-719529, unit='D') #convert from Matlab's datenum format to human readable format
                time = [UTCDateTime(str(t)) for t in t2] # convert to list of obspy UTCDateTime objects

    return time, mag, lat, lon, depth

def read_csv(csv_file,  datenum= True, **kwargs):
    
    # df = pd.read_csv(csv_file, engine="pyarrow", **kwargs) #use pyarrow for faster input
    df = pd.read_csv(csv_file, **kwargs)
    
    df.columns= df.columns.str.lower() # convert header to all lowercase letters
    header = df.columns
    
    # replace with common column names if present
    if 'time' in header:
        t_label = 'time'
    elif 't' in header:
        t_label = 't'

    if 'lon' in header:
        x_label = 'lon'
    elif 'long' in header:
        x_label = 'long'
    elif 'longitude' in header:
        x_label = 'longitude'
    elif 'x' in header:
        x_label = 'x'
        
    if 'lat' in header:
        y_label = 'lat'
    elif 'latitude' in header:
        y_label = 'latitude'
    elif 'y' in header:
        y_label = 'y'

    if 'depth' in header:
        z_label = 'depth'
    elif 'z' in header:
        z_label = 'z'

    if 'mag' in header:
        mag_label = 'mag'    
    elif 'ml' in header:
        mag_label = 'ml'
    elif 'magnitude' in header:
        mag_label = 'magnitude'

    lat = df[y_label].to_numpy()
    lon = df[x_label].to_numpy()
    depth = df[z_label].to_numpy()
    mag = df[mag_label].to_numpy()
    
    if datenum:    
        t_raw = df[t_label].to_numpy()
        timestamps = pd.to_datetime(t_raw-719529, unit='D') #convert from Matlab's datenum format to human readable format
        time = timestamps.to_numpy() # get time as numpy datetime64 objects
        time = [UTCDateTime(str(t)) for t in time] # convert to list of obspy UTCDateTime objects

    else:
        time = df[t_label].apply(UTCDateTime)
    
    return time, mag, lat, lon, depth


def read_fdsn(service, save_to_file=None, file_format="QUAKEML", **kwargs):
       
    client = Client(service)    
    cat = client.get_events(**kwargs)
    
    if save_to_file != None:
        cat.write(filename=save_to_file, format=file_format, **kwargs)
    
    return extract_from_obspy_cat(cat)


def read_obspy(file, **kwargs):
    
    cat = read_events(file)
    
    return extract_from_obspy_cat(cat)


def extract_from_obspy_cat(cat):
    
    mag = np.array([event.preferred_magnitude().mag for event in cat])
    time = [event.preferred_origin().time for event in cat]
    lat = [event.preferred_origin().latitude for event in cat]
    lon = [event.preferred_origin().longitude for event in cat]
    depth = [event.preferred_origin().depth for event in cat]
    
    return time, lat, lon, depth, mag