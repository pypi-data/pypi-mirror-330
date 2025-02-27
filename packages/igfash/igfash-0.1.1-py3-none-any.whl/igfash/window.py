# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 14:59:48 2022

@author: ftong
"""
import numpy as np
from KDEpy import FFTKDE
from scipy.stats import norm
from inspect import signature
from resample.bootstrap import confidence_interval, resample
from scipy.optimize import root_scalar
from adaptivekde import sskernel, ssvkernel

from obspy import UTCDateTime
from tqdm import tqdm


# returns a list of time windows given a time array and a list of earthquake source parameters (mag, x, y, z)
def win_CTL(time, r, win_size = 30, win_time_units = "days", win_overlap = 0.9, min_events = 50):
    
    # convert window size time units to seconds
    if win_time_units == 'days':
        win_size = win_size*24*60*60
    elif win_time_units == 'hours':
        win_size = win_size*60*60
    elif win_time_units == 'weeks':
        win_size = win_size*7*24*60*60
    elif win_time_units == 'years':
        win_size = win_size*365*24*60*60

    print("Creating CTL windows")
    t_start = UTCDateTime(time[0].date)
    t_end = UTCDateTime(time[-1].date)+86400
    
    t = np.array(time)

    # create lists to populate
    # raw_event_counter = [] # number of events used in each window, even if kde was not performed
    # final_event_counter = [] # number of events used in each window on which kde was performed
    output_t_win = [] #start time of each window
    output_r_win = [] #windowed events
    
    
    t1 = t_start #initial t1 value
    
    while(t1<t_end):
        t2 = t1 + win_size #define endpoint of new window    
        t_win = t[(t>t1) & (t<t2)] #window of events between t1 and t2
        # raw_event_counter.append(len(t_win))
        
    
        if len(t_win) < min_events:
            t1 = t1 + win_size*(1-win_overlap) # move window forward
            print("Window:", t1, t2, len(t_win), "events - window discarded")
            continue
        
        # final_event_counter.append(len(t_win))
        
        t_indices = np.where( np.logical_and( t > t1, t < t2) )
        
        r_win_tmp = []
        for i in range(0, len(r)):
            r_win_tmp.append(r[i][t_indices[0][0]:t_indices[0][-1]+1])
            
        output_t_win.append(t1)
        output_r_win.append(r_win_tmp)
    
        print("Window:", t1, t2, len(t_win), "events")

        t1 = t1 + win_size*(1-win_overlap) # move window forward

    return output_t_win, output_r_win






def win_CNE(time, r, win_size=100, win_overlap = 0.9, min_events = 50):
    
    
    event_incr = round((1-win_overlap)*win_size) # amount of events to increment by between windows
    print("Creating CNE windows, in increments of ", event_incr, "events")

    iter = tqdm(range(0,len(time),event_incr))  
    
    t = np.array(time)

    output_t_win = [] #start time of each window    
    output_r_win = [] #windowed events
    for i in iter:
        t_win= t[i:i+win_size]
        t1 = t_win[0]
        t2 = t_win[-1]

        if len(t_win) < min_events:
            print("Window:", t1, t2, len(t_win), "events - window discarded")
            continue

        r_win_tmp = []
        for j in range(0, len(r)):
            r_win_tmp.append(r[j][i:i+win_size])

        output_t_win.append(t1)
        output_r_win.append(r_win_tmp)   
        print("Window:", t1, t2, len(t_win), "events")
 

    return output_t_win, output_r_win


class Window:
    
    
    def __init__(self, mc, rum, m, t, t_unit, t_step, t_period, **kwargs):
        
        self.mc = mc
        self.rum = rum
        self.m = m
        self.t = t
        self.t_unit = t_unit
        self.t_step = t_step
        self.t_period = t_period
        self.time_span = self.get_time_span(self.t, self.t_unit)
        self.act_rate = self.activity_rate()
        self.mm = self.doubling(self.m, self.mc)
        self.h = self.bandwidth_estimator(self.mm, **kwargs)
    
    def activity_rate(self):
        
        m = self.m
        time_span = self.time_span
        num_events = len(m)
        
        act_rate = num_events / time_span
        return act_rate
    
    def get_time_span(self, t, t_unit):
        
        time_span = (t[0]-t[-1])  # time span of window in seconds
        
        if t_unit == 'day':
            time_span = time_span/86400
        elif t_unit == 'hour':
            time_span = time_span/3600
        elif t_unit == 'minute':
            time_span = time_span/60
        else:
            print("time unit not supported")
            exit
            
        return time_span
            
    def doubling(self, m, mc):
                
        xx = np.array([- m + 2*mc, m]) #doubling
        xx = xx.flatten() # make into 1D array
        xx.sort() #sort smallest to largest
        
        return xx
    
    
    def bandwidth_estimator(self, x, bw='ISJ', **kwargs):
        
        # use scipy to estimate bandwidth
        # from scipy.stats import gaussian_kde
        # if bandwidth=="scott":            
        #     kde = gaussian_kde(xx)
        #     h = kde.scotts_factor()
        # elif bandwidth == "silverman":
        #     kde = gaussian_kde(xx)
        #     h = kde.silverman_factor()

        # use statsmodels to estimate bandwidth
        # import statsmodels.api as sm
        # if type(bandwidth)==str: #need to estimate bandwidth
        #     kde = sm.nonparametric.KDEUnivariate(xx)
        #     kde.fit(bw=bandwidth)
        #     h = kde.bw
        # else:
        #     h = bandwidth
                
        # use KDEpy to estimate bandwidth
        if bw == 'ls':
            args = self.filter_args(kwargs, self.h_plat) #filter kwargs
            h = self.h_plat(x, **args)
        elif bw == 'ss':
            args = self.filter_args(kwargs, sskernel) 
            kde = sskernel(x, **args)
            h = kde[2]
        elif bw == 'ssv':
            args = self.filter_args(kwargs, ssvkernel)
            kde = ssvkernel(x, tin=np.linspace(min(x),max(x),len(x)), **args)
            h = kde[2] #returns array of bandwidths since there is a variable bandwidth across the window
        elif type(bw)==str: 
            args = self.filter_args(kwargs, FFTKDE)
            h = FFTKDE(bw=bw, **args).fit(x).bw            
        elif type(bw)==float:
            h = bw # use user-provided value for bandwidth
        

        
        return h
    
    def bootstrap_ci(self, size=2000, **kwargs):
        
        # use pingouin for bootstrap
        # from pingouin import compute_bootci
        # CDF_CI = compute_bootci(M_sel, func=cdf_nonpar_ci, n_boot=2000, paired=False, method='cper', confidence=0.98)
        
        # use scipy for bootstrap
        # from scipy.stats import bootstrap
        # M_sel = (M_sel,) #convert array to sequence
        # CDF_CI = bootstrap(M_sel, cdf_nonpar_ci, confidence_level = 0.98, n_resamples=2000, method = 'bca', random_state=1)
                
        # use arch for bootstrap
        # from arch.bootstrap import IIDBootstrap
        # args1 = self.filter_args(kwargs, IIDBootstrap) #filter args by what function actually accepts
        # bs = IIDBootstrap(self.m, **args1)
        # args2 = self.filter_args(kwargs, bs.conf_int)        
        # ci = bs.conf_int(self.cdf_nonpar_ci, reps = size, method = 'bca', size = 0.98, **args2)
        # CDF_CI = ci.flatten()
        
        # use resample for bootstrap
        args1 = self.filter_args(kwargs, confidence_interval) #filter args by what confidence_interval function actually accepts
        args2 = self.filter_args(kwargs, resample) #because confidence_interval calls resample function
        args = args1 | args2 #merge dictionaries of arguments
        a, b = confidence_interval(self.cdf_nonpar_ci, self.m, size=size, **args)
        CDF_CI = [a,b]
        
        return CDF_CI
    
    def scaling(self, x, h):
        # EVALUATES A VECTOR OF SCALING FACTORS FOR THE NONPARAMETRIC ADAPTATIVE
        # ESTIMATION
        
        # x - the n-element column vector of data values
        # h - the optimal smoothing factor
        # ambd - the resultant n-element row vector of local scaling factors
                
        n = len(x)
        c = np.sqrt(2 * np.pi)
        gau = []
        
        # if isinstance(h, np.ndarray): #test if bandwidth is a numpy array
            # print("Adaptivle locally variable bandwidth used")

        for i in range(0,n):
            gau.append(sum(np.exp(- 0.5 * ((x[i] - x) / h) ** 2)) / c / n / h)
        
        g = np.exp(np.mean(np.log(gau)))
        ambd = np.sqrt(g / gau)
        return ambd        
        
    
    def cdf_nonpar_ci(self, M, m_max=None):    
        rum = self.rum
        Mc =  self.mc
        h = self.h
        x = self.doubling(M, Mc)
        ambd = self.scaling(x,h)        
        
        Fgau_rum = norm.cdf((rum - x) / ambd / h).mean()
        Fgau_Mc = norm.cdf((Mc - x) / ambd / h).mean()
        CDF_RUM = 2 * (Fgau_rum-Fgau_Mc)
        
        # upper limit to magnitude distribution specified
        if m_max != None: 
            Fgau_Mmax = norm.cdf((m_max - x) / ambd / h).mean()    
            mian = 2 * (Fgau_Mmax-Fgau_Mc)
            CDF_RUM = CDF_RUM / mian     
              
        return CDF_RUM
    
    def kde(self):
        #perform kde on the set of data in this window
        pdf = None
        return pdf
    
    def exc_prob(self, m_max=None):
        
        t_period = self.t_period #time period
        CDF_RUM = self.cdf_nonpar_ci(self.m, m_max)
        act_rate = self.activity_rate()
        exc_pr = 1 - np.exp(np.multiply(- act_rate * (1 - CDF_RUM),t_period))
        return exc_pr
    
    def exc_prob_ci(self, **kwargs):
        t_period = self.t_period
        act_rate = self.act_rate
        cdf_ci = self.bootstrap_ci(**kwargs)
        ci_upper = 1 - np.exp(np.multiply(- act_rate * (1 - cdf_ci[0]),t_period))
        ci_lower = 1 - np.exp(np.multiply(- act_rate * (1 - cdf_ci[1]),t_period))
        return [ci_lower, ci_upper]
    
    def filter_args(self, args, function): #filter arguments dictionary by list of arguments that the function actually accepts 
        key_list = signature(function).parameters
        filtered_args = {key: value for key, value in args.items() if key in key_list}      
        return filtered_args
    
    def funct(self, t, x):
        p2 = 1.41421356
        n = len(x)
        yy = np.zeros(n)
        for i in range(n):
            xij = (x - x[i])**2 / t**2
            y = np.exp(-xij / 4) * ((xij / 2 - 1) / p2) - 2 * np.exp(-xij / 2) * (xij - 1)
            yy[i] = np.sum(y)
        fct = np.sum(yy) - 2 * n
        return fct
    
    def h_plat(self, x, solver='brenth'):

        n = len(x)
        x = np.sort(x)
        sig = np.std(x, ddof=1)
        interval = np.array([0.1 * sig / n**0.2, 2 * sig / n**0.2])
        x1 = self.funct(interval[0], x)
        x2 = self.funct(interval[1], x)

        if x1 * x2 < 0:
            fun = lambda t: self.funct(t, x)
            sol = root_scalar(fun, method=solver, bracket=interval)
            h = sol.root
        else:
            y1 = 10 ** (np.floor(np.log10(interval[0]))) / 10
            x1 = self.funct(y1, x)
            x2 = self.funct(interval[0], x)
            if x1 * x2 < 0:
                interval[1] = interval[0]
                interval[0] = y1
                fun = lambda t: self.funct(t, x)
                sol = root_scalar(fun, method=solver, bracket=interval)
                h = sol.root
            else:
                y1 = 10 ** (np.floor(np.log10(interval[0]))) / 10
                dy = 0.05 * y1
                k = 0
                hh = []
                for i in np.arange(y1, interval[0], dy):
                    k += 1
                    hh.append(self.funct(i, x))
                k = np.argmin(np.abs(hh))
                h = y1 + (k - 1) * dy

        return h


