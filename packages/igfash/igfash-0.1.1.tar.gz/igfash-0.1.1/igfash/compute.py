# -*- coding: utf-8 -*-
"""
@author: ftong
"""
import numpy as np
import bisect #used for bisecting list of events by start time
from scipy.interpolate import interp1d
from igfash.window import Window
from diffKDE import diffKDE

import sys

try:    #make dask optional
    from dask import delayed
    import dask
    from dask.diagnostics import ProgressBar # use Dask progress bar
except:
    dask = lambda x: x
    
try:    #make tqdm optional
    from tqdm import tqdm
except:
    tqdm = lambda x: x

    
def time_window_length(t_input, time_unit='day'):
        
    t = assure_order(t_input, chrono='forward')
    
    n_events = len(t) # number of events in the catalog
    t_start = t[0] # time of first event, assumes event list sorted by time
    t_end = t[-1] # time of last event
    time_span= t_end-t_start #length of data set between first and last event
    
    if time_unit == 'day':
        time_span = time_span / 86400 #convert time span from seconds to days
    elif time_unit == 'hour':
        time_span = time_span / 3600 #convert time span from seconds to hours
    elif time_unit == 'minute':
        time_span = time_span / 60 #convert time span from seconds to minutes

    activity_rate = n_events / time_span
    
    window_length = np.ceil(80 / activity_rate) # use window length such that there are 80 events per window
    
    return window_length,activity_rate

def assure_order(t, chrono, x=[None]):
    
    # t is a list of time values, x must be a numpy array
    
    # check ordering of time based on first two events and reverses it if necessary
    if chrono=="forward" and t[1]<t[0] or chrono=="backward" and t[1]>t[0]:
        t_new = list(reversed(t))
        
        if len(x)>1: # x provided, so reverse also x then return both t and x
            x_new = np.flip(x)
            return t_new, x_new
        
        else: # x is empty, return only t
            return t_new

    
    else: # ordering is already as desired based on test
    
        if len(x)>1: # x provided, so return both t and x
            return t, x
        
        else: # x is empty, return only t
            return t
        
def parse_time(t, t_unit, t_step_raw, win_size_raw=False):

    t_start = t[0]
    t_end = t[-1]

    # convert step and window size to seconds
    if t_unit == 'day':
        t_step = t_step_raw*86400
        win_size = win_size_raw*86400 
    elif t_unit == 'hour':
        t_step = t_step_raw*3600
        win_size = win_size_raw*3600 
    elif t_unit == 'minute':
        t_step = t_step_raw*60
        win_size = win_size_raw*60
    
    if not win_size_raw: 
        return t_start, t_end, t_step #CNE windows
    else:
        return t_start, t_end, t_step, win_size #CTL windows


#compute KDE on windows of data from a catalog
def comp_kde(M_input, Mc, rum, t_input, t_unit, t_step_raw, t_period, win_size_raw, win_method, min_events=50, M_max=None, verbose = False, parallel = True, **kwargs):
    t, M = assure_order(t_input, chrono='backward', x=M_input)
    
    if win_method == 'CNE':
        t_start, t_end, t_step = parse_time(t, t_unit, t_step_raw)
        win_size = win_size_raw
    elif win_method == 'CTL':
        t_start, t_end, t_step, win_size = parse_time(t, t_unit, t_step_raw, win_size_raw)
    else:
        print("Abort! Please select either CNE or CTL method for windowing...")
        sys.exit()

    windows = np.arange(t_start,t_end,-t_step)
    kde = [] # KDE PDF for each window
    tc = [] # timestamp of end of each window
    nwin = len(windows)
    
    if parallel:
        print("Processing windows in parallel using Dask")
        pbar = ProgressBar()
        pbar.register()
        iter = windows
    else:
        print("Processing windows")
        iter = tqdm(windows) # use tqdm progress bar

    # Iterate through all the windows, select desired number of events and compute exceedance probability
    for idx, tt in enumerate(iter): # tt is the end time of each window

        if win_method == 'CNE':
            j = len(t) - bisect.bisect_right(t[::-1], tt)
    
            # fetch the next win_size number of events after event t[j], event times and their magnitudes
            T_sel = t[j:j+win_size] # event times for window
            M_sel = M[j:j+win_size] # event magnitudes for window
            
            if len(T_sel) < win_size:
                print("Not enough events left to fill window starting at", tt)
                break

        elif win_method == 'CTL':
            j1 = len(t) - bisect.bisect_right(t[::-1], tt)
            j2 = len(t) - bisect.bisect_right(t[::-1], tt-win_size)
            
            # fetch all events within the time window
            T_sel = t[j1:j2] # event times
            M_sel = M[j1:j2] # event magnitudes
            
            num_events = len(T_sel)
    
            if num_events<min_events:
                # print("Insufficient events at time window", tt)
                kde.append(None) # insufficient events, set to null
                tc.append(tt)
                continue            # move on to next window

        tc.append(tt)

        if parallel: #run in parallel using dask
            win = delayed(Window)(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
            # exc_pr.append(delayed(win.exc_prob)()) 
            exc_pr.append(win.exc_prob())
            

        else: #run without parallel computing
            win = Window(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
            exc_pr.append(win.exc_prob())
            
            if ci: # estimate confidence interval
                exc_pr_ci.append(win.exc_prob_ci(**kwargs))
                
            if verbose==True:
                print("\nWindow", idx+1, "of", nwin)
                print("\tbandwidth:", round(win.h,3))
                print("\texceedance probability:", round(100*exc_pr[idx],2), "%")

                # print(exc_pr[idx])
                if ci==True:
                    print("\tconfidence interval:", round(100*exc_pr_ci[idx][0],2), "to", round(100*exc_pr_ci[idx][1],2), "%")


    if parallel:
        exc_pr = dask.compute(*exc_pr, scheduler='processes')
        exc_pr_ci = dask.compute(*exc_pr_ci, scheduler='processes')
        # exc_pr = dask.compute(*exc_pr)
        exc_pr = exc_pr[::-1] #because reverse is not working when using tuples with dask    
        exc_pr_ci = exc_pr_ci[::-1]    
    else: #reverse operation is faster than slicing
        exc_pr.reverse()
        exc_pr_ci.reverse()

    tc.reverse()
    
    print("Exceedance Probability computed from", tc[0], "to", tc[-1])
    
    return exc_pr, exc_pr_ci, tc
def comp_exc_prob(M_input, Mc, rum, t_input, t_unit, t_step_raw, t_period, win_size_raw, win_method, M_max=None, verbose = False, ci = False, parallel = True, **kwargs):
    t, M = assure_order(t_input, chrono='backward', x=M_input)
    
    if win_method == 'CNE':
        t_start, t_end, t_step = parse_time(t, t_unit, t_step_raw)
        win_size = win_size_raw
    elif win_method == 'CTL':
        t_start, t_end, t_step, win_size = parse_time(t, t_unit, t_step_raw, win_size_raw)
    else:
        print("Abort! Please select either CNE or CTL method for windowing...")
        sys.exit()

    windows = np.arange(t_start,t_end,-t_step)
    exc_pr = [] # exceedance probability for each window
    exc_pr_ci = [] # confidence interval for exc_pr
    tc = [] # timestamp of end of each window
    nwin = len(windows)
    
    if parallel:
        print("Processing windows in parallel using Dask")
        pbar = ProgressBar()
        pbar.register()
        iter = windows
    else:
        print("Processing windows")
        iter = tqdm(windows) # use tqdm progress bar

    # Iterate through all the windows, select desired number of events and compute exceedance probability
    for idx, tt in enumerate(iter): # tt is the end time of each window

        if win_method == 'CNE':
            j = len(t) - bisect.bisect_right(t[::-1], tt)
    
            # fetch the next win_size number of events after event t[j], event times and their magnitudes
            T_sel = t[j:j+win_size] # event times for window
            M_sel = M[j:j+win_size] # event magnitudes for window
            
            if len(T_sel) < win_size:
                print("Not enough events left to fill window starting at", tt)
                break

        elif win_method == 'CTL':
            j1 = len(t) - bisect.bisect_right(t[::-1], tt)
            j2 = len(t) - bisect.bisect_right(t[::-1], tt-win_size)
            
            # fetch all events within the time window
            T_sel = t[j1:j2] # event times
            M_sel = M[j1:j2] # event magnitudes
            
            num_events = len(T_sel)
    
            if num_events<50:
                # print("Insufficient events at time window", tt)
                exc_pr.append(float("NaN")) # insufficient events, set to null
                exc_pr_ci.append([float("NaN"),float("NaN")]) # insufficient events, set to null
                tc.append(tt)
                continue            # move on to next window

        tc.append(tt)

        if parallel: #run in parallel using dask
            win = delayed(Window)(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
            # exc_pr.append(delayed(win.exc_prob)()) 
            exc_pr.append(win.exc_prob())
            
            if ci: # estimate confidence interval
                # exc_pr_ci.append(delayed(win.exc_prob_ci)(**kwargs))
                exc_pr_ci.append(win.exc_prob_ci(**kwargs))

        else: #run without parallel computing
            win = Window(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
            exc_pr.append(win.exc_prob())
            
            if ci: # estimate confidence interval
                exc_pr_ci.append(win.exc_prob_ci(**kwargs))
                
            if verbose==True:
                print("\nWindow", idx+1, "of", nwin)
                print("\tbandwidth:", round(win.h,3))
                print("\texceedance probability:", round(100*exc_pr[idx],2), "%")

                # print(exc_pr[idx])
                if ci==True:
                    print("\tconfidence interval:", round(100*exc_pr_ci[idx][0],2), "to", round(100*exc_pr_ci[idx][1],2), "%")


    if parallel:
        exc_pr = dask.compute(*exc_pr, scheduler='processes')
        exc_pr_ci = dask.compute(*exc_pr_ci, scheduler='processes')
        # exc_pr = dask.compute(*exc_pr)
        exc_pr = exc_pr[::-1] #because reverse is not working when using tuples with dask    
        exc_pr_ci = exc_pr_ci[::-1]    
    else: #reverse operation is faster than slicing
        exc_pr.reverse()
        exc_pr_ci.reverse()

    tc.reverse()
    
    print("Exceedance Probability computed from", tc[0], "to", tc[-1])
    
    return exc_pr, exc_pr_ci, tc

def mirror(samples, xmin):    
    samples_mirrored = np.array([2*xmin - samples, samples]).flatten()
    return samples_mirrored

def kde_m(samples, xmin, xmax, method="diffKDE", n_kde=512, pp=False): # use KDE to compute an approximate probability distribution function of magnitude

    # mirror data
    samples_mirrored = mirror(samples, xmin)
    x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde)

    if pp: #use Dask for parallel processing
        kdes = [dask.delayed(diffKDE.KDE)(samples_mirrored, xmin=x_mirrored.min(), xmax=x_mirrored.max(), n=len(x_mirrored))] 
        kde = dask.compute(*kdes)
    else: #vanilla
        kde = [diffKDE.KDE(samples_mirrored, xmin=x_mirrored.min(), xmax=x_mirrored.max(), n=len(x_mirrored))]

    kde = [np.split(kde[i][0][1:],2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE

    return kde

def get_cdf(pdf): #get cdf from a pdf
    cdf = np.cumsum(pdf)
    cdf = cdf/cdf.max()
    return cdf

def get_samples(cdf, x, n_elements): #get samples from a cdf using the inverse transform sampling method
    quantiles = np.random.uniform(cdf.min(), 1, n_elements) 
    inv_ecdf = interp1d(cdf, x, kind='linear', bounds_error=True) 
    samples = inv_ecdf(quantiles)
    return samples

def exc_pr(cdf, activity_rate, time_period):
    return 1 - np.exp(-activity_rate*time_period*(1-cdf))


def return_period(cdf, activity_rate):
    return 1/(activity_rate*(1-cdf))

# convert columns of data to rows of events
# eg. [[x1,x2],[y1,y2]] -> [[x1, y1], [x2, y2]]
def cols_to_rows(var):
    dim, n = np.array(var).shape
    return [[var[j][k] for j in range(0,dim)] for k in range(0,n)]
    
def hellinger_dist (X, Y):
    """ Calculates Hellinger distance between 2 multivariate normal distribution         
         X = X(x1, x2)
         Y = Y(y1, y2)         
    """
    if len(X) < 2 or len(Y) < 2:      return 1.
    
    meanX = np.mean(X, axis=0)
    covX = np.cov(X, rowvar=0)
    detX = np.linalg.det(covX)
    
    meanY = np.mean(Y, axis=0)
    covY = np.cov(Y, rowvar=0)
    detY = np.linalg.det(covY)
    
    detXY = np.linalg.det((covX + covY)/2)
    if (np.linalg.det(covX + covY)/2) != 0:
            covXY_inverted = np.linalg.inv((covX + covY)/2)
    else:
            covXY_inverted = np.linalg.pinv((covX + covY)/2)    
    dist = 1. - (detX**.25 * detY**.25 / detXY**.5) * np.exp(-.125 * np.dot(np.dot(np.transpose(meanX-meanY),covXY_inverted),(meanX - meanY)))        
    return min(max(dist, 0.), 1.)