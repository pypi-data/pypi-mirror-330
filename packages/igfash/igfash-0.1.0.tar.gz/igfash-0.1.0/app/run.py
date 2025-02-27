# -*- coding: utf-8 -*-
# import sys
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import MultipleLocator
from matplotlib.contour import ContourSet  # Tasos
from skimage.transform import resize
import branca

# matplotlib.use('Agg')
# from matplotlib import pyplot as plt, dates as mdates
# from timeit import default_timer as timer
from plash.io import read_mat_cat, read_mat_m, read_mat_pdf, read_csv
from plash.window import win_CTL, win_CNE
import plash.kde as kde
from plash.gm import compute_PGA_exceedance
from plash.compute import get_cdf, hellinger_dist, cols_to_rows
from plash.rate import lambda_probs, calc_bins, bootstrap_forecast_rolling
from plash.mc import estimate_mc
import numpy as np
from timeit import default_timer as timer

import dask
from dask.diagnostics import ProgressBar # use Dask progress bar
from dask.distributed import Client
from tqdm import tqdm

import kalepy as kale
# from datetime import timedelta, datetime
# from scipy.stats import bootstrap
# from scipy.stats import t as student_t
# from matplotlib.dates import DateFormatter, AutoDateLocator
from math import ceil, floor
import sys
import utm
# from pyroots import Brentq, Brenth, Ridder, Bisect

# from openquake.hazardlib.geo import Point #This class represents a geographical point in terms of longitude, latitude, and depth (with respect to the Earth surface).
# from openquake.hazardlib.geo.surface.planar import PlanarSurface
# from openquake.hazardlib.source.characteristic import CharacteristicFaultSource
# from openquake.hazardlib.mfd import ArbitraryMFD
# from openquake.hazardlib.tom import PoissonTOM
# from openquake.hazardlib.scalerel import WC1994 #Wells and Coppersmith magnitude – rupture area relationships

# from openquake.hazardlib.contexts import ContextMaker
# from openquake.hazardlib.valid import gsim
# from openquake.hazardlib.geo import Point
# from openquake.hazardlib.site import Site, SiteCollection
# from openquake.hazardlib.contexts import ContextMaker
# from openquake.hazardlib.imt import PGA, PGV, SA


#%% BEGIN PROGRAM
if __name__ == '__main__':

    # Configuration
    verbose = False
    # verbose = True
    # mode = 'M' # Magnitude distribution modeling only
    # mode = 'L' # Location distribution modeling only
    # mode = 'R' # Rate modeling only
    # mode = 'MLR'
    # mode = 'Lforecast' # forecast using input model files, build support later
    mode = 'MLRforecast' # modeling and forecasting, same as None
    # mode = None # do full forecast
    

    
    lambdas = [0.3]
    lambdas_perc = [1]
    
    windowing = False
    
    # file = "catalog_lgcd_feb16_panel2.mat" #mc=1.9, m_max=4
    # mc = 1.9
    # m_max = 4 

    file = "LGCD_catalog.mat" #mc=1.8 to 2, m_max=5
    # mc = 2
    m_max = 5 
    
    # file = "GRONINGEN_catalog.mat" #mc=1.1
    # file = "Parkfield_precursory.csv"
    # file = "Ridgecrest.csv" 
    # mc = 0.9 #Ridgecrest
    # m_max = 8 #Ridgecrest


    catalog_file = "c:/igf/data/catalogs/" + file
    catalog_label='Ctg'
    # catalog_label='Catalog'
    mag_label='Mw'
    # mag_label='ML'

    #load magnitude PDF from file
    if False:
    # if True:
        
        m_pdf = read_mat_pdf('./PDF.mat')
        m_range = read_mat_m('./m.mat')
    
        
    # Activite Rate modeling parameters; default 90 days
    time_range = 90
    time_unit = 'days'
    # time_unit = 'hours'
    # time_unit = 'weeks'
    # time_unit = 'years'
    
    #### Mdist configuration ####
    # kde_pkg = 'KDEpy-ISJ'
    # kde_pkg = 'KDEpy-silverman'
    # kde_pkg = 'KDEpy-scott'
    # kde_pkg = 'adaptiveKDE'
    kde_pkg = 'diffKDE'
    # kde_pkg = 'arviz-isj'
    # kde_pkg = 'arviz-silverman'
    # kde_pkg = 'arviz-scott'  
    m_win_overlap = 0.1
    # m_win_method = 'CNE'
    m_win_method = None
    m_win_size = 200  #number of events
    # m_win_method = "CTL"
    # m_win_size = 10



    grid_dim = 5000.0 # in metres #for 2D KDE and also for forecasting... use same grid?
    
    # exclude_low_fxy = False
    exclude_low_fxy = True
    thresh_fxy = 1e-3 #minimum fxy value (location PDF) needed to do PGA estimation (to skip low probability areas); also should scale according to number of grid points
    
    xy_win_overlap = 0.1 #not used for 'TW' mode
    
    time_D = 100 #forecast length in time_units
    
    # GMPE parameters
    # alpha = 1.25  # Intercept
    # beta = 0.31   # Magnitude coefficient
    # gamma = -1.34 # Distance attenuation coefficient
    # h = 558       # Depth factor (in meters)
    # SEE = 0.196   # Standard error of estimate
    # Cb = np.array([[0.005586, -0.000376, -0.000752], 
    #                 [-0.000376, 0.000103, -0.000111], 
    #                 [-0.000752, -0.000111, 0.000440]])  # Covariance matrix
    # num_ground_motion_records = 1196  # Number of ground motion records in GMPE estimation
    p = 0.05     # Probability of exceedance
    
    
    

    
    
    # Validate input
    # if time_unit not in ['hours', 'days']:
    #     print("Invalid time unit. Defaulting to 'days'.")
    #     time_unit = 'days'
    
    # use_pp = False
    use_pp = True #set to always True?  
    
    
    
    if use_pp:
        dask.config.set(scheduler='processes', num_workers = 8)
        # client = Client() # startup client, can view dashboard at http://localhost:8787/status

    if file[-3:] == 'mat':
        time, mag, lat, lon, depth = read_mat_cat(catalog_file, catalog_label=catalog_label, mag_label=mag_label)
    elif file[-3:] == 'csv':
        time, mag, lat, lon, depth = read_csv(catalog_file, datenum=False)
      

    mc_test = np.round(np.arange(mag.min(), mag.max(), 0.1), 2).tolist()
    ans = estimate_mc(mag, mc_test, delta_m=0.1, p_pass=0.1, stop_when_passed=True, verbose=False, n_samples=10000)
    mc = ans[3]
    print("Mc estimated at", mc)


    #remove events below Mc
    if mc != None:
        indices = np.argwhere(mag<mc)
        mag = np.delete(mag, indices)
        time = np.delete(time, indices)
        lat = np.delete(lat, indices)
        lon = np.delete(lon, indices)
    else:
        mc = mag.min() 

#%% M distribution modeling
    if 'M' in mode:
        print("M mode - Magnitude distribution modeling")
      
        n_kde=128

        
            
        if kde_pkg == None:
            print("No KDE method specified, therefore use diffKDE by default")
            kde_pkg ='diffKDE'
    
        if mag_label == None:
            print("No magnitude label of catalog specified, therefore try ML by default")
            mag_label='ML'
              
        start = timer()
        
        if m_win_method == "CTL":
            t_windowed, r_windowed = win_CTL(time, [lon, lat, mag], win_size = m_win_size, win_overlap = m_win_overlap)
        elif m_win_method == "CNE":
            t_windowed, r_windowed = win_CNE(time, [lon, lat, mag], win_size = m_win_size, win_overlap = m_win_overlap, min_events = m_win_size)
        else:
            print("Must be either CTL or CNE for windowing. Use all events in catalog.")
            t_windowed, r_windowed = win_CNE(time, [lon, lat, mag], win_size = len(mag), win_overlap = 0, min_events = 1)
    
        m_windowed = [r[2] for r in r_windowed] #extract only magnitude windows
    
            
        if kde_pkg[:5] == 'KDEpy':
            pdf = kde.compute_kde(m_windowed, xmin=mc,xmax=m_max, bw_method = kde_pkg[6:], n_kde=n_kde*2, pp=use_pp )
        elif kde_pkg == 'adaptiveKDE':
            pdf = kde.compute_adaptivekde(m_windowed, bw_method = "adaptive-local", xmin=mc, xmax=m_max, n_kde=n_kde*2, pp=use_pp)
        elif kde_pkg == 'diffKDE':
            pdf = kde.compute_diffkde(m_windowed, xmin=mc, xmax=m_max, n_kde=n_kde*2, pp=use_pp)
        elif kde_pkg[:5] == 'arviz':
            pdf = kde.compute_arvizkde(m_windowed, xmin=mc, xmax=m_max, bw_method=kde_pkg[6:], n_kde=n_kde*2, pp=use_pp)
            
        end = timer()
        print("Magnitude KDE Computation time: ", end - start, "seconds")
    
        m_pdf = 2*pdf[-1] #select last window's pdf as the one to use for forecasting
        m_range= np.linspace(mc, m_max, n_kde)
        
        bin_width=0.1 #Tasos
        bins = np.arange(min(m_windowed[-1]), max(m_windowed[-1]) + bin_width, bin_width) #Tasos

        #plot only the last window                
        figsize=(8, 6)
        dpi=300
        fig = plt.figure(dpi=dpi, figsize=figsize)   
        # fig, ax = plt.subplots(dpi=dpi, figsize=figsize)
        plt.hist(m_windowed[-1], bins=bins, color='blue', edgecolor='black', alpha=0.6, density=True, label='Magnitude bins') #Tasos
        plt.plot(m_range, m_pdf, color='red', linewidth=2.5, label='KDE') #Tasos
        plt.legend() #Tasos
        
        # Configure ticks #Tasos
        ax = plt.gca() #Tasos
        ax.xaxis.set_major_locator(MultipleLocator(0.2)) # Major ticks every 0.2 #Tasos
        ax.xaxis.set_minor_locator(MultipleLocator(0.1)) # Minor ticks every 0.1 #Tasos
        ax.tick_params(axis='x', which='major', labelsize=10)  # Labels only for major ticks #Tasos
        ax.tick_params(axis='x', which='minor', length=5, labelsize=0)  # No labels for minor ticks #Tasos
        
        # Rotate ticks by 45 degrees #Tasos
        plt.xticks(rotation=45) #Tasos
        plt.ylabel("f(M)")
        plt.xlabel("Magnitude")

        plt.show()
        
        np.savetxt('last_window_KDE_PDF.csv', np.c_[m_range, m_pdf])

#%% L location distribution modeling
    if 'L' in mode:
        print("L mode - Location distribution modeling")

        method = 'TW'
        # method = ''
        # method = 'CNE'
        # method = 'CTL'
        
        win_size = 100 #number of events
        
        # method = 'CTL'
        # win_size = 200 #number of events
    
        # if method == None:
        #     print("No method specified, therefore use CNE by default")
        #     method = 'CNE'
    
        #convert to UTM
        u = utm.from_latlon(lat, lon) 
        x = u[0]
        y = u[1]
        utm_zone_number = u[2]
        utm_zone_letter = u[3]
        #define corners of grid based on global dataset (or make it user selectable?)
        # x_min = lon.min()
        # y_min = lat.min()
        # x_max = lon.max()
        # y_max = lat.max()
        x_min = x.min()
        y_min = y.min()
        x_max = x.max()
        y_max = y.max()
        z_min = depth.min()
        z_max = depth.max()
        
        grid_x_max = int(ceil(x_max / grid_dim) * grid_dim)
        grid_x_min = int(floor(x_min / grid_dim) * grid_dim)
        grid_y_max = int(ceil(y_max / grid_dim) * grid_dim)
        grid_y_min = int(floor(y_min / grid_dim) * grid_dim)
        
        #rectangular grid
        nx = int((grid_x_max - grid_x_min) / grid_dim)+1            
        ny = int((grid_y_max - grid_y_min) / grid_dim)+1            




        # ensure a square grid is used
        if nx > ny: #enlarge y dimension to match x
            ny = nx
            grid_y_max = int(grid_y_min + (ny-1)*grid_dim)

        else: #enlarge x dimension to match y
            nx = ny
            grid_x_max = int(grid_x_min + (nx-1)*grid_dim)

        # new x and y range
        x_range = np.linspace(grid_x_min, grid_x_max, nx)
        y_range = np.linspace(grid_y_min, grid_y_max, ny)
        
       
        
        start = timer()
        
        # generate windows if that's desired
        if method == "CTL":
            # t_windowed, r_windowed = win_CTL(time, [lon, lat, depth], win_size = win_size,  win_overlap = xy_win_overlap, win_time_units = time_unit)
            t_windowed, r_windowed = win_CTL(time, [x, y, depth], win_size = win_size,  win_overlap = xy_win_overlap, win_time_units = time_unit)
        elif method == "CNE":
            # t_windowed, r_windowed = win_CNE(time, [lon, lat, depth], win_size = win_size, win_overlap = xy_win_overlap, min_events = win_size)
            t_windowed, r_windowed = win_CNE(time, [x, y, depth], win_size = win_size, win_overlap = xy_win_overlap, min_events = win_size)
        else:
            t_windowed = time
            r_windowed = [[x, y]]
    
        
        # compute inter-window Hellinger Distance    
        if 'C' in method:
            
            hld = [] #interwindow hellinger distances
            for i in range(0,len(r_windowed)-1):
                x_win1 = r_windowed[i][0]
                y_win1 = r_windowed[i][1]
                dist_win1 = cols_to_rows([x_win1, y_win1])
                
                x_win2 = r_windowed[i+1][0]
                y_win2 = r_windowed[i+1][1]                
                dist_win2 = cols_to_rows([x_win2, y_win2])

                
                hld.append(hellinger_dist(dist_win1, dist_win2))
                
                
    
        # x_windowed = [r[0] for r in r_windowed] #extract x windows
        # y_windowed = [r[1] for r in r_windowed] #extract y windows
        
        
    
    
        
        # xy_grid, pdf_kde = cat_kale.density([x_axis, y_axis], reflect=True, probability=True)
        # pdf_kde = pdf_kde.reshape((n_kde, n_kde))
        # cat_kde = [pdf_kde, np.linspace(x_min, x_max, n_kde), np.linspace(y_min, y_max, n_kde)]
    
    
        #compute KDE and extract PDF
        print("Computing KDE of each window...")
        
        if method == "TW":
            x_weights = np.linspace(0,15,len(t_windowed))
            weighting_fcn = np.exp(x_weights) #exponential weighting 
            output_kale, output_kde = kde.compute_2d_kde([grid_x_min, grid_x_max, grid_y_min, grid_y_max], r_windowed, n_kde = nx, weighting_fcn=weighting_fcn)
        else:
            output_kale, output_kde = kde.compute_2d_kde([grid_x_min, grid_x_max, grid_y_min, grid_y_max], r_windowed, n_kde = nx)
        
        #output contains a list of results from each window
        
        # # iter = tqdm(range(0,len(r_windowed)))  
        
        # #prepare axes of grid on which to perform KDE (2D only for now)
        # x_axis, y_axis = np.meshgrid(np.linspace(x_min, x_max, n_kde), np.linspace(y_min, y_max, n_kde))
        # x_axis = x_axis.flatten()
        # y_axis = y_axis.flatten()
        
        # output_kale = [] #list of KALE objects for each window
        # output_kde = [] #list of KDE PDFs for each window
        # for i_win in iter:
            
        #     x_win = r_windowed[i_win][0]
        #     y_win = r_windowed[i_win][1]
            
        #     kde_kale = kale.KDE([x_win,y_win])
        
        #     output_kale.append(kde_kale) #used later when generating samples and plots
        
        #     xy_grid, pdf_kde = kde_kale.density([x_axis, y_axis], probability=True)
        #     # xy_grid, pdf_kde = kde_kale.density([x_axis, y_axis], reflect=True, probability=True)
        #     pdf_kde = pdf_kde.reshape((n_kde, n_kde))
        #     output_kde.append([pdf_kde, np.linspace(x_min, x_max, n_kde), np.linspace(y_min, y_max, n_kde)])
        
        # # normalize the PDFs
        # for i in range(0,len(output_kde)):
        #     output_kde[i][0]=1*output_kde[i][0]/np.sum(output_kde[i][0])
        end = timer()
    
        print("2D KDE Computation time: ", end - start, "seconds")
    
        #take only the last window for use in forecasting
        xy_kale = output_kale[-1] 
        xy_kde = output_kde[-1]
        
        xy_kale_km = type(xy_kale)(xy_kale.dataset / 1000) #Tasos
        
        #plot only the last window
        # corner = kale.corner(xy_kale)
        corner = kale.corner(xy_kale_km,quantiles=[0.025, 0.16, 0.50, 0.84, 0.975],cmap='hot') #Tasos

        from matplotlib.ticker import FormatStrFormatter
        from matplotlib.ticker import MultipleLocator
        ax00 = corner[0].axes[0][0] # bottom left plot
        ax00.set_ylabel("Probability Density")
        # ax00.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))  # Ensure 4 decimal places displayed
        
        # Remove the PDF ticks below zero
        yticks = ax00.get_yticks()
        new_yticks = yticks[yticks>=0]
        ax00.set_yticks(new_yticks)

        # ax01 = corner[0].axes[0][1] # bottom right plot
        
        ax10 = corner[0].axes[1][0] # top left plot
        # ax10.set_aspect('equal')  # Makes the units equal on both axes

        ax10.set_xlabel("UTM X (km)") #Tasos
        ax10.set_ylabel("UTM Y (km)") #Tasos
        ax10.ticklabel_format(style='plain') 
        for coll in ax10.collections: #Tasos
            if isinstance(coll, ContourSet):  # Check if it's a contour plot Tasos
                ax10.clabel(coll, inline=True, fontsize='smaller', fmt="%.1f") #Tasos
        # ax10.xaxis.set_major_locator(MultipleLocator(1000))
        # ax10.yaxis.set_major_locator(MultipleLocator(1000))

        ax11 = corner[0].axes[1][1] # top right plot
        ax11.set_xlabel("Probability Density")
        # ax11.set_ylabel("UTM Y (m)")
        ax11.ticklabel_format(style='plain') 
        # ax11.yaxis.set_major_locator(MultipleLocator(1000))
        
        # Remove the PDF ticks below zero
        xticks = ax11.get_xticks()
        new_xticks = xticks[xticks>=0]
        ax11.set_xticks(new_xticks)
        ax11.set_yticklabels([])  # This removes the ytick labels # Tasos

        # ax11.xaxis.set_major_formatter(FormatStrFormatter('%.4f'))  # Ensure decimal formatting

        

        
        # for ax in corner[0].axes.flatten():
        #     ax.ticklabel_format(style='scientific', scilimits=(0, 0), axis='both')  # Scientific notation
        #     ax.set_title("UTM X")
        
        # Rotate x-axis tick labels for all bottom-row plots
        for ax in corner[0].axes[-1, :]:  # Last row corresponds to the bottom x-axes
            for label in ax.get_xticklabels():
                label.set_rotation(46)
     
        # corner[0].legend()
        corner[0].fig.savefig('2d_kd_cornerplot.png', bbox_inches = "tight", dpi=300)
        # np.savetxt('last_window_KDE_PDF.csv', np.array(xy_kale[0]))
        # plt.hist(m_windowed[-1], bins='auto', density=True)
        # plt.plot(m_range, 2*pdf[-1])
        # plt.show()
        
        # np.savetxt('last_window_KDE_PDF.csv', 2*pdf[-1])

#%% Activity Rate modeling
    if 'R' in mode:
        print("R mode - activity Rate modeling")

        if file[-3:] == 'mat':
            time, mag_dummy, lat_dummy, lon_dummy, depth_dummy = read_mat_cat(catalog_file, catalog_label=catalog_label, mag_label = mag_label, output_datenum=True)    
            datenum_data = time # REMEMBER THE DECIMAL DENOTES DAYS
            # datetime_data = [datenum_to_datetime(d) for d in datenum_data] # NOT NECESSARILY NEEDED 

        elif file[-3:] == 'csv':
            time, mag_dummy, lat_dummy, lon_dummy, depth_dummy = read_csv(catalog_file, datenum=False)
        
        # multiplicator = 1

        
        if time_unit == 'hours':
            multiplicator = 24
            # start_date = datetime_data[-1] - timedelta(days=time_range*0.04167)
            # filtered_dates = [date for date in datetime_data if start_date <= date <= datetime_data[-1]]
        elif time_unit == 'days':
            multiplicator = 1
            # start_date = datetime_data[-1] - timedelta(days=time_range)
            # filtered_dates = [date for date in datetime_data if start_date <= date <= datetime_data[-1]]
        elif time_unit == 'weeks':
            multiplicator = 1/7
        elif time_unit == 'years':
            multiplicator = 1/365

        # elif time_unit == 'months':
        #     multiplicator = 0.03285
        #     start_date = datetime_data[-1] - timedelta(days=time_range*30)
        #     filtered_dates = [date for date in datetime_data if start_date <= date <= datetime_data[-1]]
        
        # Selects dates in datenum format and procceeds to forecast value
        start_date = datenum_data[-1] - (2 * time_range / multiplicator)
        dates_calc = [date for date in datenum_data if start_date <= date <= datenum_data[-1]]
        # forecasts, bca_conf95, rate_mean = bootstrap_forecast_rolling(dates_calc, multiplicator)
        forecasts, bca_conf95, rate_mean = bootstrap_forecast_rolling(dates_calc, multiplicator)

        # print("start date", start_date)
        # print("dates calc", dates_calc)

        # FINAL VALUES OF RATE AND ITS UNCERTAINTY IN THE 5-95 PERCENTILE
        unc_bca05=[ci.low for ci in bca_conf95]; unc_bca95=[ci.high for ci in bca_conf95]
        rate_unc_high=multiplicator/np.array(unc_bca05); rate_unc_low=multiplicator/np.array(unc_bca95); 
        rate_forecast= multiplicator / np.median(forecasts) #[per time unit]

        # Plot of forecasted activity rate with previous binned activity rate
        act_rate, bin_counts, bin_edges, out, pprs, rt, idx, u_e = calc_bins(np.array(datenum_data), time_unit, time_range, dates_calc, rate_forecast, rate_unc_high, rate_unc_low, multiplicator, quiet= not verbose)


        # Assign probabilities 
        lambdas, lambdas_perc = lambda_probs(act_rate,dates_calc,bin_edges)

        print(lambdas, lambdas_perc )

        
        
        # # Check if the filtered list has less than 3 dates
        # if len(filtered_dates) < 3:
        #     raise ValueError("Needs 3 or more values to run, darling.")
            
        # dates_calc = datenum_data[-len(filtered_dates):]

        # forecasts, bca_conf95, rate_mean = bootstrap_forecast_rolling(dates_calc, time_unit, multiplicator)

        # # FINAL VALUES OF RATE AND ITS UNCERTAINTY IN THE 5-95 PERCENTILE
        # unc_bca05=[ci.low for ci in bca_conf95]
        # unc_bca95=[ci.high for ci in bca_conf95]
        # rate_unc_high=multiplicator/np.array(unc_bca05)
        # rate_unc_low=multiplicator/np.array(unc_bca95)
        # rate_forecast= multiplicator / np.median(forecasts) #[per time unit]

        # # Plot of forecasted activity rate with previous binned activity rate
        # act_rate, bin_counts, bin_edges = calc_bins(np.array(datenum_data), time_unit, time_range, dates_calc, rate_forecast, rate_unc_high, rate_unc_low, multiplicator)

        # print("Forecasted activity rate: ", rate_forecast, "events per", time_unit[:-1])

#%% Forecasting        
    if "forecast" in mode:
        
        #assume for now we do not use external input PDF/CDF
        
        # use these activity rates until final code from Tasos comes
        # lambdas = [0.5, 0.2, 1.1] # Vector of seismic activity rates for different sub-periods
        # percentages_D = [0.3, 0.2, 0.5] #Vector of percentage of D corresponding to each sub-period

        # lambdas = [rate_forecast]
        # lambdas = [1.0] #for testing
        # percentages_D = [1.0]
        
        model = 'Lasocki2013' #hard code to LGCD for now
        # products =  ['PGA', 'SA(0.1)', 'SA(0.3)', 'SA(0.6)', 'SA(1.0)']

        Mag = 5.0 #placeholder mag, must be valid for that context; will be overwritten during function call
        rupture_aratio = 1.5
        Strike = 0
        Dip = 90
        Rake = 0

 

        
        
        

        # if 'M' in mode: # sample magnitude PDF
        # print("Forecasting future event magnitudes...")
        m_cdf = get_cdf(m_pdf) 
        #     m_samples = get_samples(m_cdf, m_range, n_events)
        
        # if 'L' in mode: #sample location PDF
        # print("Forecasting future event locations...")
        # xy_samples = xy_kale.resample(size=n_events) #we no longer do this, there we can even use other 2D KDE packages!
        # plt.scatter(xy_samples[0], xy_samples[1]) #plot event locations
        
        fxy=xy_kde[0]
        print("Verification that f(x,y) is normalized; Sum of all f(x,y) values = ", np.sum(fxy))
        

              
        
        plt.imshow(fxy, origin='lower')
        plt.show()
        
        #toy debug
        # x_min = 0
        # x_max = 3
        # y_min = 0
        # y_max = 4
        # xy_samples = [[0, 1, 2], [0, 1, 2]]
        
        
        
        # calculate distance of events to points on grid
        #define grid using previously defined xmin, xmax, ymin, ymax

        #if using 1km grid cells
        # grid_dim = 100000.0 # in metres
        # grid_x_max = int(ceil(x_max / grid_dim) * grid_dim)
        # grid_x_min = int(floor(x_min / grid_dim) * grid_dim)
        # grid_y_max = int(ceil(y_max / grid_dim) * grid_dim)
        # grid_y_min = int(floor(y_min / grid_dim) * grid_dim)
        # nx = int((grid_x_max - grid_x_min) / grid_dim)+1            
        # ny = int((grid_y_max - grid_y_min) / grid_dim)+1            

        # x_range = np.linspace(grid_x_min, grid_x_max, nx)
        # y_range = np.linspace(grid_y_min, grid_y_max, ny)
        
        
        #NEW METHOD - use fxy values at all points in grid

        xx, yy = np.meshgrid(x_range, y_range, indexing='ij')         # grid points
        
        # Set a single receiver (testing only)
        # x_rx = int((grid_x_max + grid_x_min)/2) # receiver x coordinate
        # y_rx = int((grid_y_max + grid_y_min)/2) # receiver x coordinate
        # squared_distances = (xx - x_rx)**2 + (yy - y_rx)**2
        # distances = np.sqrt(squared_distances)
        
        # set every grid point to be a receiver
        x_rx = xx.flatten()
        y_rx = yy.flatten()
        
        distances = np.zeros(shape=(nx*ny, nx, ny))
        rx_lat=np.zeros(nx*ny)        
        rx_lon=np.zeros(nx*ny)
        
        # compute distance matrix for each receiver
        for i in range(nx*ny):
            # print("Receiver location:", x_rx[i], y_rx[i])
            
            # Compute the squared distances directly using NumPy's vectorized operations
            squared_distances = (xx - x_rx[i])**2 + (yy - y_rx[i])**2
            
            distances[i] = np.sqrt(squared_distances)

            # create context object for receiver and append to list            
            # most of these parameters do not have any effect as our gmpe does not use this information
            
            rx_lat[i], rx_lon[i] = utm.to_latlon(x_rx[i], y_rx[i], utm_zone_number, utm_zone_letter) #get receiver location as lat,lon
            










        
        plt.imshow(distances[0], origin='lower')
        plt.show()
        
        
        #experimental - compute PGA at grid points that have minimum probability density of thresh_fxy
        if exclude_low_fxy:
            indices = list(np.where(fxy.flatten() > thresh_fxy)[0])
        else:
            indices = range(0,len(distances))
        # r = distances.flatten()
        # fr = np.repeat(1/len(r), repeats=len(r)) #old method - equal probability at every point
        # fr = np.repeat(fxy.flatten(), repeats=int(nx*ny)) #new method, use probability distribution function directly

        #OLD METHOD - generate XY samples and calculate distance to receiver
        
        # get number of events in forecast period
        # n_events = 0
        # for count, rate_forecast in enumerate(lambdas):
        #     n_events += ceil(time_D*rate_forecast*percentages_D[count-1])
        
        # n_events = ceil(t_future*rate_forecast)
        # n_events = len(xy_samples[0])

        # # List containing a distance matrix of dimension nx by ny for each event
        # # event_distances = np.zeros(shape=(n_events,nx,ny)) #old shape         
        # event_distances = np.zeros(shape=(n_events, nx, ny))         
            
        # # go through all points of grid
        # for i in range(0,nx):
            
        #     xi = x_range[i]
            
        #     for j in range(0,ny):
                
        #         yj = y_range[j]
                
        #         for k in range(0, n_events): # go through all events

        #             x0 = xy_samples[0][k]
        #             y0 = xy_samples[1][k]
                    
        #             event_distances[k][i][j] = np.sqrt((x0-xi)**2 + (y0-yj)**2)
                   
        # f_r = np.repeat(1/n_events, repeats=n_events)

        #for testing, compute PGA exceedance for only the first cell of XY grid, i=0, j=0
        # r = event_distances[:,0,0]
        
        
        
        fr = fxy.flatten()
        
        #For each receiver compute PGA value
        print("Estimating PGA at", len(indices), "grid points...")
        start = timer()

        PGA = np.zeros(shape=(nx*ny))
        
        # for rx_index in range(len(distances)):
        #     print("*** Receiver", rx_index, "***")
        #     r = distances[rx_index].flatten(order='C')
            
        #     rx_pga = compute_PGA_exceedance(r, fr, p, lambdas, time_D, percentages_D, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 2.0)
        #     print('Estimated PGA Value:', rx_pga)
        #     PGA[rx_index] = rx_pga

        #DEBUG just do this Rx
        # i=714
        # pga = compute_PGA_exceedance(distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 2.0, rx_label = i)
        sys.exit()
        if use_pp:
            pbar = ProgressBar()
            pbar.register()
            # iter = range(0,len(distances))
            iter = indices
            
            pgas = [dask.delayed(compute_PGA_exceedance)(rx_lat[i], rx_lon[i], distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc, m_range, m_pdf, m_cdf, model, PGA_min = 0.0, PGA_max = 2.0, rx_label = i) for i in iter]
            pga = dask.compute(*pgas) 
        else:
            # iter = tqdm(range(0,len(distances)))      
            iter = tqdm(indices)      
            
            pga = []
            for i in iter:
                pga.append(compute_PGA_exceedance(distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc, m_range, m_pdf, m_cdf, ctxs[i][0], imtls, PGA_min = 0.0, PGA_max = 2.0, rx_label = i))


        # iter = [4,5,7]
        # pgas = [dask.delayed(compute_PGA_exceedance)(distances[i].flatten(), fr, p, lambdas, time_D, percentages_D, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 2.0) for i in range(0,len(distances))]



        end = timer()
        print("PGA Computation time: ", end - start, "seconds")

        pga = list(pga)
        


        if exclude_low_fxy:
            
            pga_grid_prep = []
            #insert null values into grid where we chose not to compute PGA because of low fxy 
            for i in range(0,len(distances)):
                
                if i in indices:                
                    pga_grid_prep.append(pga.pop(0))
                    
                else:
                    pga_grid_prep.append(np.nan) # use np.nan to indicate grid point excluded
                    # pga_grid_prep.append(None) # use None to indicate grid point excluded


        else:
            pga_grid_prep = pga

        #%% experimental - try again to compute PGA if solver failed
        
        #DEBUG - set some pga grid values to -1 so that we can recompute them
        # pga_grid_prep2 = pga_grid_prep.copy()
        
        # pga_grid_prep2[0] = -1
        # pga_grid_prep2[-1] = -1
        
        # idx_redo = list(np.where([math.isnan(pga_value) for pga_value in pga]))
        idx_redo = np.where([pga_value < 0 for pga_value in pga_grid_prep])[0] #list of indices where pga calculation failed
        
        
        if len(idx_redo)>0:            
            # pgas_redo = [dask.delayed(compute_PGA_exceedance)(distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 2.0, rx_label = i) for i in idx_redo]
            # pga_redo = dask.compute(*pgas_redo) 
        
        
        
            for i in idx_redo:
                # run computation again with slightly different params and hope solver finds a solution?
                pga_redone=compute_PGA_exceedance(distances[i].flatten(), fr, p, lambdas, time_D, lambdas_perc, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 2.0, rx_label = i)
        
                pga_grid_prep[i] = pga_redone
        
        
        









        # get values for log color scale
        vmin = min(x for x in pga_grid_prep if x is not np.nan)
        vmax = max(x for x in pga_grid_prep if x is not np.nan)
        # vmin = min(x for x in pga_grid_prep if x is not None)
        # vmax = max(x for x in pga_grid_prep if x is not None)
        
        #swap np.nan for None values in grid
        # pga_grid_prep = np.where(pga_grid_prep != np.nan, pga_grid_prep, None) #doesn't work yet
        
        #debug individual receivers
        # r = distances[61].flatten()
        # PGA_value = compute_PGA_exceedance(r, fr, p, lambdas, time_D, percentages_D, m_range, m_pdf, m_cdf, GMPE, PGA_min = 0.0, PGA_max = 5.0)

        # PGA = np.array(PGA, shape=(nx, ny))
        # PGA2 = np.reshape(PGA, (nx, ny), order='C') 
        pga_grid = np.reshape(pga_grid_prep, (nx, ny)).astype(dtype=np.float64)  # this reduces PGA values to 8 decimal places

        dpi=300
        fig = plt.figure(dpi=dpi)   
        # extent = [int(grid_x_min/1000), int(grid_x_max/1000), int(grid_y_min/1000), int(grid_y_max/1000)] #display extent in kilometres
        plt.imshow(pga_grid, extent= [grid_x_min/1000, grid_x_max/1000, grid_y_min/1000, grid_y_max/1000], origin='lower', cmap='viridis') #linear color bar
        # plt.imshow(pga_grid, extent= [grid_x_min/1000, grid_x_max/1000, grid_y_min/1000, grid_y_max/1000], origin='lower', cmap='viridis',  norm=colors.LogNorm(vmin=vmin, vmax=vmax)) #log color bar
        plt.xlabel('UTM X (km)')
        plt.ylabel('UTM Y (km)')
        plt.colorbar(label="PGA (g)")
        # plt.scatter(x/1000,y/1000, alpha=0.1, c='grey', marker='.', s=1.5)
        # plt.scatter(x/1000,y/1000, alpha=0.8, c='grey', marker='.', s=5)
        
        # Generate scatter plot for each magnitude range # Tasos 
        sc_offset = abs(mc)+1 if mc < 0 else 0 # Support for negative magnitudes in scatter plot Tasos
        for i in range(int(np.floor(mc)), int(np.ceil(m_max))): # Tasos
            print(i)
            mask = (mag >= i) & (mag < i + 1)  # Magnitudes in range # Tasos
            sizes =  3 * (i + sc_offset)  # Size for circles # Tasos
            plt.scatter(x[mask]/1000, y[mask]/1000, alpha=0.7, c='grey', marker='o', s=sizes,
                        edgecolors='black', linewidths=0.2, label=f'{i:.1f}–{i+1:.1f}') # Tasos
        plt.legend(title="Magnitudes", fontsize=6, title_fontsize=6) # Tasos
        
        plt.show()
        sys.exit()

        #sanity check for first event
        # test = event_distances[10]
        # levels = np.arange(0, x_max, grid_dim*50)            
        # plt.imshow(test, origin='lower')
        # # plt.contour(test, levels, colors='k', origin='lower')
        # plt.colorbar()
        # plt.show()
        






        # #sanity check for first event
        # test = event_distances[0]
        # levels = np.arange(0, x_max, grid_dim*50)            
        # plt.imshow(test, origin='lower')
        # # plt.contour(test, levels, colors='k', origin='lower')
        # plt.colorbar()
        # plt.show()
        
        # X, Y = np.meshgrid(x_range, y_range)
        # X = X.T
        # Y = Y.T

        # for each 
        # r = 
#%% Save pga grid
        # np.save("./LGCD_PGA_grid_1000m_thresh0.npy", pga_grid)


#%% Upscale grid (experimental)

        pga_grid_tmp = np.nan_to_num(pga_grid) # change nans to zeroes
        
        up_factor = 4
        # Upscale the grid
        pga_grid_hd = resize(pga_grid_tmp, (up_factor*len(pga_grid_tmp), up_factor*len(pga_grid_tmp)), mode='reflect', anti_aliasing=False)
        # pga_grid_hd = resize(pga_grid, (up_factor*len(pga_grid), up_factor*len(pga_grid)), mode='symmetric', anti_aliasing=False)
        
        pga_grid_hd[pga_grid_hd == 0.0] = np.nan # change zeroes back to nan
        
        plt.imshow(pga_grid_hd, origin='lower', extent=[0, 1, 0, 1], aspect='auto')
        plt.colorbar()
        plt.title("Upscaled Grid with NumPy")
        plt.show()


        
        figsize=(3.54,3.54)
        dpi=300
        fig, ax = plt.subplots(dpi=dpi, figsize=figsize)
        plt.imshow(pga_grid_hd, extent= [grid_x_min/1000, grid_x_max/1000, grid_y_min/1000, grid_y_max/1000], origin='lower', cmap='viridis')
        # plt.imshow(pga_grid_hd, extent= [grid_x_min/1000, grid_x_max/1000, grid_y_min/1000, grid_y_max/1000], origin='lower', cmap='viridis',  norm=colors.LogNorm(vmin=vmin, vmax=vmax)) #log color bar
        plt.xlabel('UTM X (km)')
        plt.ylabel('UTM Y (km)')
        plt.colorbar(label="PGA (g)")
        
        # Generate scatter plot for each magnitude range # Tasos 
        sc_offset = abs(mc)+1 if mc < 0 else 0 # Support for negative magnitudes in scatter plot Tasos
        for i in range(int(np.floor(mc)), int(np.ceil(m_max))): # Tasos
            mask = (mag >= i) & (mag < i + 1)  # Magnitudes in range # Tasos
            sizes =  3 * (i + sc_offset)  # Size for circles # Tasos
            plt.scatter(x[mask]/1000, y[mask]/1000, alpha=0.7, c='grey', marker='o', s=sizes,
                        edgecolors='black', linewidths=0.2, label=f'{i:.1f}–{i+1:.1f}') # Tasos
        plt.legend(title="Magnitudes", fontsize=6, title_fontsize=6) # Tasos
        
        plt.show()

        # sys.exit()

        # %% Visualization - generate overlay of PGA grid over map tiles
        
        import folium
        from folium.raster_layers import ImageOverlay
        from folium import TileLayer
        
        north, south = lat.max(), lat.min()  # Latitude range
        east, west = lon.max(), lon.min()  # Longitude range
        bounds = [[south, west], [north, east]]
        
        map_center = [np.mean([north, south]), np.mean([east, west])]
        
        # Create an image from the grid
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(pga_grid_hd, origin='lower', cmap='viridis')
        ax.axis('off')
        
        # Save the figure
        fig.canvas.draw()
        # image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8) #alt way using numpy file instead of png 
        # image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))        
        # plt.savefig("overlay_with_transparency.png", bbox_inches="tight", pad_inches=0, transparent=True)
        plt.savefig("overlay_with_transparency.svg", bbox_inches="tight", pad_inches=0, transparent=True)
        plt.close(fig)
        
        
        # Create a colormap
        viridis_colors = ["#440154", "#3B528B", "#21908C", "#5DC863", "#FDE725"]
        colormap = branca.colormap.LinearColormap(
            colors=viridis_colors,  # Define color scale
            vmin=vmin,  # Minimum value
            vmax=vmax,  # Maximum value
            caption="PGA (g)",  # Add a caption to the colormap
            text_color = 'white', #text color
        )
        
                
        # Create map
        m = folium.Map(location=map_center, zoom_start=12)
        
        # e tiles
        TileLayer(
            tiles="Cartodb dark_matter",
            # attr="toner-bcg",
            name="Cartodb dark matter",
        ).add_to(m)
        
        # Google Satellite tiles
        TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google Satellite",
            name="Satellite",
        ).add_to(m)
        

        
        
        # Add the image overlay
        image_overlay = ImageOverlay(
            # image=image, # use numpy file
            image="overlay_with_transparency.png", #use png file instead of numpy array 
            bounds=bounds,
            opacity=0.6,
            interactive=True,
            name="Estimated PGA"
        ).add_to(m)
        
        # Add the colormap then cusotmize font size and background colour
        colormap.add_to(m)
        svg_style = '<style>svg {font-size: 14px; background-color: black;}</style>'
        m.get_root().header.add_child(folium.Element(svg_style))
        
        
        
        # Add earthquake locations using FastMarkerCluster
        # Each point needs to be a tuple: (latitude, longitude, popup_content)
        from folium.plugins import MarkerCluster, FastMarkerCluster
        # FastMarkerCluster(data=list(zip(lat, lon)), disableClusteringAtZoom=True).add_to(m)
        locations=list(zip(lat, lon))
        popups = ["lon:{}<br>lat:{}".format(lon, lat) for (lat, lon) in locations]
        
        # draw_eq = """\
        # function (row) {
        #     var marker;
        #     marker = L.circle(new L.LatLng(row[0], row[1]), {background-color: 'transparent', color:'grey'});
        #     return marker;
        # };
        # """
        
        # callback = ('function (row) {' 
        #         'var circle = L.circle(new L.LatLng(row[0], row[1]), {color: "red",  radius: 10});'
        #         'return circle};')
        
        callback = ('function (row) {' 
                'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red",  radius: 10});'
                # 'var icon = L.AwesomeMarkers.icon({'
                # "icon: 'circle',"
                # "iconColor: 'black',"
                # "markerColor: 'black',"
                # "prefix: 'glyphicon',"
                # "extraClasses: 'fa-rotate-0'"
                    # '});'
                'marker.setIcon(icon);'
                "var popup = L.popup({maxWidth: '300'});"
                "const display_text = {text: row[2]};"
                "var mytext = $(`<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> ${display_text.text}</div>`)[0];"
                "popup.setContent(mytext);"
                "marker.bindPopup(popup);"
                'return marker};')
        
        marker_cluster = FastMarkerCluster(
            data=locations,
            name="Earthquake Catalog",
            # callback=callback,
            overlay=True,
            control=True,
            disableClusteringAtZoom=True,
        )
        # marker_cluster.add_to(m)
        
        # Add LayerControl for interactivity
        folium.LayerControl().add_to(m)
       
        
        # Add a JavaScript slider for opacity control
        opacity_slider = """
        <script>
            var slider = L.DomUtil.create('input', 'opacity-slider');
            slider.type = 'range';
            slider.min = 0;
            slider.max = 1;
            slider.step = 0.1;
            slider.value = 0.5;
            slider.style.position = 'absolute';
            slider.style.top = '50px';
            slider.style.right = '50px';
            slider.style.zIndex = 1000;
        
            slider.oninput = function() {
                var overlayLayer = this._map._layers;
                for (var key in overlayLayer) {
                    if (overlayLayer[key] instanceof L.ImageOverlay) {
                        overlayLayer[key].setOpacity(this.value);
                    }
                }
            };
        
            document.body.appendChild(slider);
        </script>
        """
        m.get_root().html.add_child(folium.Element(opacity_slider))
        
     
        
        m.save("index.html")