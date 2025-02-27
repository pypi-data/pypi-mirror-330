import numpy as np
from datetime import timedelta, datetime
import matplotlib.dates as mdates 
from matplotlib.dates import DateFormatter, AutoDateLocator
import matplotlib.pyplot as plt
from scipy.stats import bootstrap
import Rbeast as rb
import pandas as pd

def datenum_to_datetime(datenum):
    # MATLAB epoch starts at year 0, Python's datetime starts at year 1
    matlab_epoch = datetime(1, 1, 1)
    days = datenum - 367  # Subtracting the offset for MATLAB's epoch BUT THIS COULD BE PROBLEMATIC
    return matlab_epoch + timedelta(days=days)

def apply_beast(act_rate, **kwargs):
    """
    Applies BEAST to the smmothed rate data using different smoothing windows.
    Input
    act_rate : The activity rate data array to smooth and apply BEAST.
    Output
    out : A list of BEAST results for each smoothed rate array.
    prob : A list of probabilities and change points extracted from BEAST results.
    """
    out = []; prob = []
    # Define the range of smoothing windows based on 15-20% of the size of rate array
    ll = int(np.ceil(0.15 * len(act_rate)))
    ul = int(np.ceil(0.20 * len(act_rate)))
    
    # Apply BEAST for each smoothed rate array
    for ii in range(ll, ul + 1):
        # Apply Gaussian smoothing with window size ~15-20%
        bb=pd.Series(act_rate).rolling(window=ii, win_type='gaussian', center=True, min_periods=1).mean(std=ii).to_numpy()  
        # Apply BEAST on the smoothed array discarding periodicity
        beast_result = rb.beast(bb, season='none', **kwargs)
        out.append(beast_result)
        
    # Extract probabilities and change points from BEAST results
    # Gets the median number of changepoints or if median = 0 gets 90th percentile
    for result in out:
        if result.trend.ncp_median != 0:
            ncp_median = int(np.max(result.trend.ncp_median))  #Ensure it's integer
            cp_probs = result.trend.cpPr[:ncp_median]
            cps = result.trend.cp[:ncp_median]
        else:
            ncp_pct90 = int(np.max(result.trend.ncp_pct90))  #Ensure it's integer
            cp_probs = result.trend.cpPr[:ncp_pct90]
            cps = result.trend.cp[:ncp_pct90]
            
        # Sort the change points and corresponding probabilities
        sorted_indices = np.argsort(cps)
        sorted_cps = cps[sorted_indices]
        sorted_probs = cp_probs[sorted_indices]
        
        # Store the sorted change points and probabilities
        prob.append(np.column_stack((sorted_probs, sorted_cps)))
        
    return out, prob

def merge_rt(rt, idx, u_e):
    """
    Merges consecutive values of rate, IF difference smaller thn 0.002
    unless only two values
    Input : rate (rt), id of changepoints (idx), unique elements of changepoint vectors (u_e)
    Output : The same as input, but merged if needed
    """
    rt_n = []
    i = 0
    while i < len(rt):
        gr = [rt[i]]
        while i < len(rt)-1 and abs(rt[i + 1] - rt[i]) < 0.002 and len(rt) > 2:
            idx[i + 1:] = [x - 1 for x in idx[i + 1:]]  # Subtract 1 from each element in idx[i+1:]
            idx = np.delete(idx, i)  # Remove element at index i
            u_e = np.delete(u_e, i + 1)  # Remove element at index i + 1
            i += 1  # Increment i
            gr.append(rt[i])  # Append the current rt[i] to gr
        rt_n.append(np.mean(gr))
        i += 1
    return rt_n, idx, u_e

def av_rates(act_rate,pprs):
    """
    Decides on which changepoints to use based on percentile of occurances
    and then calculates the average rates for periods between changepoints
    Input : activity rate (act_rate), changepoint probabilities (pprs)
    Output 
    av : average rate between changepoints
    idx : the array id of changepoint occurences in the top 75 %
    u_e : the unique elements of the changepoint probabilities (pprs)
    """
    # Decision on changepoints
    if len(pprs) > 0:
        u_e, ind = np.unique(pprs, return_inverse=True)
        occurr = np.bincount(ind)
        # Selection base on percentile based on number  of changepoints occurences from multiple Rbeast runs
        idx = np.where(occurr >= np.percentile(occurr, 25))[0] 
        neighbors = []
        
        # Check if two points are neighboring and choose the latter
        for i in range(len(idx) - 1):
            current = u_e[idx[i]]
            next_elem = u_e[idx[i + 1]]
            if next_elem == current + 1:  # Check if next element is a neighbor
                neighbors.append(idx[i])

        # Remove neighbors as changepoints
        idx = np.setdiff1d(idx, neighbors)

        # Calculate average rate between changepoints
        # Assumes that the changepoint value belongs to the next period
        rt = []
        for i in range(len(idx)):
            # Calculates first and second value
            if i == 0 and len(idx) > 1:  
                rt.append(np.mean(act_rate[:int(u_e[idx[i]]) - 1]))
                rt.append(np.mean(act_rate[int(u_e[idx[i]]):int(u_e[idx[i + 1]])]))
            # Calculates first and last value when only two periods
            elif i == 0 and len(idx) == 1:  
                rt.append(np.mean(act_rate[:int(u_e[idx[i]]) - 1]))
                rt.append(np.mean(act_rate[int(u_e[idx[i]]):]))
            # Calculates final value
            elif i == len(idx) - 1 and len(idx) > 1:  
                rt.append(np.mean(act_rate[int(u_e[idx[i]]):]))
            # Calculates intermediate values
            else:  
                rt.append(np.mean(act_rate[int(u_e[idx[i]]):int(u_e[idx[i + 1]])]))

        # Merge consecutive rate values smaller than 0.002 unless only two values
        if len(rt)>2:
            rt, idx, u_e = merge_rt(rt, idx, u_e)
    else:
        rt=[]; idx=[]; u_e=[]
        print('-----------------------------------------------------')
        print('No changepoints detected by BEAST (Zhao et al., 2019)')
        print('-----------------------------------------------------')
    return rt, idx, u_e

def calc_bins(dates, unit, bin_dur, dates_calc, rate_forecast, rate_unc_high, rate_unc_low, multiplicator, filename = "activity_rate.png", **kwargs):

    start_date = dates.min()
    end_date = dates.max()
    end_date_dt=datenum_to_datetime(end_date)

    # Unit and duration check, default to 15 DAYS or 12 HOURS
    # valid_units = ['hours', 'days']
    # if unit not in valid_units:
    #     unit = 'days'
    #     bin_dur = 15

    # Adjust to '12 hours' if data duration is less than 15 days
    # if (end_date - start_date) < 15 and unit == 'days':
    #     unit = 'hours'
    #     bin_dur = 12

    # -------- bin, bin edges, bin midpoint calc -------------
    # Determine number of bins
    bin_edges=[end_date]
    while bin_edges[-1] > start_date:
        bin_edges.append(bin_edges[-1] - (bin_dur/multiplicator))
    bin_edges = bin_edges[::-1]
    bin_edges_dt = [datenum_to_datetime(d) for d in bin_edges]  
    # Discretize the time data
    bin_counts, _ = np.histogram(dates, bins=bin_edges)
    # Calculate the rate
    act_rate = [count / ((bin_edges[i + 1] - bin_edges[i]) * multiplicator) * multiplicator for i, count in enumerate(bin_counts)]
    
    # ---------Apply BEAST (Zhao et al., 2019) 10 times--------
    ppr_all = []
    for _ in range(10):
        out, ppr = apply_beast(act_rate, **kwargs)  # Apply BEAST
        ppr_iter = np.concatenate([p for p in ppr if p is not None], axis=0)  # Concatenate results
        ppr_all.append(ppr_iter[:, 1])
    # Concatenate all probabilities from all BEAST runs
    pprs = np.concatenate(ppr_all, axis=0)
    pprs = pprs[~np.isnan(pprs)]
    
    # -------Changepoint decision and rate calculations--------
    rt, idx, u_e = av_rates(act_rate, pprs)
    
    # --------------------- Line Plot -------------------------
    fig, ax = plt.subplots(figsize=(14, 5))
    
    # Plot activiry rate for all catalog
    ax.plot(bin_edges_dt[1:len(bin_edges)], act_rate, '-o', linewidth=2, markersize=6)
    
    # Plot forecasted value with uncertainties with red line connected to last value
    next_date = end_date + (bin_dur/multiplicator) 
    ax.plot(datenum_to_datetime(next_date), rate_forecast, 'ro', label='Forecasted Rate', markersize=6)
    ax.plot([bin_edges_dt[-1], datenum_to_datetime(next_date)], [act_rate[-1], rate_forecast], 'r-')
    ax.vlines(datenum_to_datetime(next_date), rate_unc_low, rate_unc_high, colors='r', linewidth=2, label='Bootstrap uncertainty')  # Vertical line for the uncertainty range
    
    # Format the x-axis with dates
    ax.xaxis.set_major_locator(AutoDateLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%d-%b-%Y'))
    plt.xticks(rotation=45)
    plt.title(f'Activity rate (Time Unit: {unit}, Time Window Duration: {bin_dur} {unit})')
    plt.xlabel('Time (Window Center Date)')
    plt.ylabel('Activity rate per selected time window')
    plt.grid(True)
    
    # Add Vertical Line and Shaded Area
    sel_data = bin_edges[-3]
    sel_data_dt=datenum_to_datetime(sel_data)
    ax.axvline(sel_data_dt, color='r', linestyle='--', linewidth=2,  label='Time window used')
    def convert_dates_to_num(dates):
        return [mdates.date2num(date) if isinstance(date, datetime) else date for date in dates]
    
    # Shade the area to the right of the vertical line
    ylim = ax.get_ylim()
    
    # Add the shaded area using the Polygon function
    ax.fill_between([sel_data_dt, end_date_dt], 0.0, ylim[1]+0.1, color='r', alpha=0.5)
    
    # Add rates and changepoints from BEAST - changepoint belongs to NEXT period
    if 'rt' in locals():
        for i in range(len(idx)):
            # Plot first period
            if i == 0 and len(idx) > 1:
                ax.plot(bin_edges_dt[1:len(bin_edges)][:int(u_e[idx[i]])], [rt[i]] * int(u_e[idx[i]]), linewidth=2)
            # Plot Last and second to last periods when more than 1 changepoints
            elif i == len(idx) - 1 and len(idx) > 1:
                ax.plot(bin_edges_dt[1:len(bin_edges)][int(u_e[idx[i - 1]]):int(u_e[idx[i]])], 
                        [rt[i]] * (int(u_e[idx[i]]) - int(u_e[idx[i - 1]])), linewidth=2)
                ax.plot(bin_edges_dt[1:len(bin_edges)][int(u_e[idx[i]]):], 
                        [rt[i + 1]] * (len(act_rate)  - int(u_e[idx[i]])), linewidth=2)
            # Plot first and last period if only one changepoint
            elif i == 0 and len(idx) == 1:
                ax.plot(bin_edges_dt[1:len(bin_edges)][:int(u_e[idx[i]])], [rt[i]] * int(u_e[idx[i]]), linewidth=2)
                ax.plot(bin_edges_dt[1:len(bin_edges)][int(u_e[idx[i]]):], 
                         [rt[i + 1]] * (len(act_rate) - int(u_e[idx[i]])), linewidth=2)
            # Plot intermediate value if it's only one 
            elif len(bin_edges_dt[1:len(bin_edges)][int(u_e[idx[1 - 1]]):int(u_e[idx[1]])])==1:
                nnn = multiplicator / bin_dur
                ax.plot(bin_edges_dt[1:len(bin_edges)][int(u_e[idx[i - 1]]):int(u_e[idx[i]]) + 1], 
                        [rt[i]] * (int(u_e[idx[i]]) + 1 - int(u_e[idx[i - 1]])), linewidth=2)                
            # Plot intermediate periods    
            else:
                ax.plot(bin_edges_dt[1:len(bin_edges)][int(u_e[idx[i - 1]]):int(u_e[idx[i]])], 
                        [rt[i]] * (int(u_e[idx[i]]) - int(u_e[idx[i - 1]])), linewidth=2)

    plt.legend(loc='best')
    plt.savefig(filename, dpi=600)
    plt.show()
    
    return act_rate, bin_counts, bin_edges, out, pprs, rt, idx, u_e

# Bootstrap forecasts
# A values is forecasted from the values of a window that is double the requestd forecasted range 
def bootstrap_forecast_rolling(data,multiplicator):
    window_data=[]; bca_conf95 = []; forecasts = []
    
    for i in range(1,len(data)):
        data_diff=(data[i]-data[i-1])
        window_data.append(data_diff)
        
    window_data=np.array(window_data)
    window_data=window_data*multiplicator
        
    # Calculate the mean of the window data
    rate_mean_data = 1/np.mean(window_data)
    
    # Get Bootstrap samples - BCa method
    if len(window_data)>=5:
        res95 = bootstrap((window_data,), np.mean, confidence_level=0.95, method='BCa', n_resamples=1000)
    else:
        res95 = bootstrap((window_data,), np.mean, confidence_level=0.95, method='BCa', n_resamples=len(window_data**(len(window_data))))
    forecasts.append(np.mean(res95.bootstrap_distribution))
    bca_conf95.append(res95.confidence_interval)       
    
    return forecasts, bca_conf95, rate_mean_data

def lambda_probs(act_rate,dates_calc,bin_edges):
    smaller_elements = [b for b in bin_edges if b < dates_calc[0]]
    first_used_bin = min(smaller_elements, key=lambda x: abs(dates_calc[0] - x))
    bin_index = np.digitize(first_used_bin, bin_edges)
    lambdas_perc=[]; dur=[]; lambdas=[]
    for i in range(bin_index,len(bin_edges)):
        if i == bin_index:
            dur.append(bin_edges[i]-first_used_bin)
        else:
            dur.append(bin_edges[i]-bin_edges[i-1])
    for i in range(len(dur)):
        lambdas_perc.append(dur[i]/sum(dur))
        lambdas.append(act_rate[-i-1])
        
    return lambdas, lambdas_perc 