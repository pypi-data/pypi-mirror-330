# -*- coding: utf-8 -*-
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, dates as mdates
from timeit import default_timer as timer
import numpy as np
import pip



def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


def main(catalog_file, kde_pkg, win_method, win_size, win_overlap, Mc, M_max, time_unit, mag_label, use_parallel):
    """
    Python application that reads an earthquake catalog and performs non-parametric estimation of the magnitude distribtion.
    Arguments:
        catalog_file: path to input file of type 'Catalog'
    Returns:
        PNG image files containing a plot of the probability distribution function obtained by non-parametric estimation and CSV files of these PDFs.
    """
    sys.stdout = open("log.txt", "w") 
    
    install('arviz')
    install('KDEpy')
    install('adaptivekde')
    pip.main(['install', '-i https://test.pypi.org/simple/', 'eqdist==0.0']) #install eqpi from testpypi archive for now
    
    if use_parallel:
        print("Parallel computing activated, load Dask")
        install('dask')
        
    from eqdist.io import read_mat
    from eqdist.window import win_CTL, win_CNE
    import eqdist.kde as kde

    print("Inputs are:\n", catalog_file, kde_pkg, win_method, win_size, win_overlap, Mc, M_max, time_unit, mag_label, use_parallel)
    
    if kde_pkg == None:
        print("No KDE method specified, therefore use diffKDE by default")
        kde_pkg ='diffKDE'

    if mag_label == None:
        print("No magnitude label of catalog specified, therefore try ML by default")
        mag_label='ML'
    
    time, mag, lat, lon, depth = read_mat(catalog_file, mag_label=mag_label)
    
    #remove events below Mc
    if Mc != None:
        indices = np.argwhere(mag<Mc)
        mag = np.delete(mag, indices)
        time = np.delete(time, indices)
        lat = np.delete(lat, indices)
        lon = np.delete(lon, indices)

    
    start = timer()
    if win_method == "CTL":
        t_windowed, r_windowed = win_CTL(time, [lon, lat, mag], win_size = win_size, win_overlap = win_overlap)
    elif win_method == "CNE":
        t_windowed, r_windowed = win_CNE(time, [lon, lat, mag], win_size = win_size, win_overlap = win_overlap, min_events = win_size)
    else:
        print("Invalid window selection method. Must be either CTL or CNE")
        sys.exit()
        
        
    m_windowed = [r[2] for r in r_windowed] #extract only magnitude windows
    
    if kde_pkg[:5] == 'KDEpy':
        pdf = kde.compute_kde(m_windowed, xmin=Mc, xmax=M_max, bw_method = kde_pkg[6:], pp=use_parallel )
    elif kde_pkg == 'adaptiveKDE':
        pdf = kde.compute_adaptivekde(m_windowed, bw_method = "adaptive-local", xmin=Mc, xmax=M_max, pp=use_parallel)
    elif kde_pkg == 'diffKDE':
        pdf = kde.compute_diffkde(m_windowed, xmin=Mc, xmax=M_max, pp=use_parallel)
    elif kde_pkg[:5] == 'arviz':
        pdf = kde.compute_arvizkde(m_windowed, xmin=Mc, xmax=M_max, bw_method=kde_pkg[6:], pp=use_parallel)

    end = timer()
    print("Computation time: ", end - start, "seconds")

    m_range= np.linspace(Mc, M_max, 256)
    plt.hist(m_windowed[-1], bins='auto', density=True)
    plt.plot(m_range, 2*pdf[-1])
    plt.ylabel("f(M)")
    plt.xlabel("Magnitude")
    plt.show()



    
    # if use_ci:
    #     plt.plot(t_plot,exc_pr_ci_lower_plot)
    #     plt.plot(t_plot,exc_pr_ci_upper_plot)
    #     csv_array = np.vstack((tc, exc_pr_plot, exc_pr_ci_lower_plot, exc_pr_ci_upper_plot))
    #     csv_array = csv_array.T          
    #     np.savetxt('exc_pr.csv', csv_array, delimiter=",", header="time,exceedance_probability(%),confidence_interval_lower,confidence_interval_upper", fmt="%s,%f,%f,%f")
    # else:
    #     csv_array = np.vstack((tc, exc_pr_plot))
    #     csv_array = csv_array.T          
    #     np.savetxt('exc_pr.csv', csv_array, delimiter=",", header="time,exceedance_probability(%)", fmt="%s,%f")

    plt.savefig('last_window_KDE.png')