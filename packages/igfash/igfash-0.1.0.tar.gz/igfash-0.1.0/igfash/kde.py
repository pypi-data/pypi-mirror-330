# -*- coding: utf-8 -*-
"""
@author: ftong
"""
import numpy as np
from KDEpy import FFTKDE, NaiveKDE, TreeKDE
import adaptivekde
# from fastkde import fastKDE
from diffKDE import diffKDE
# from lightkde import kde_1d
import kalepy as kale
import arviz
import dask
# import kdetest.kde
from scipy.optimize import root_scalar
from pathlib import Path

def mirror(samples, xmin):    
    samples_mirrored = [np.array([2*xmin - samples[i], samples[i]]).flatten() for i in range(0,len(samples))]
    return samples_mirrored

    
def select_subset(samples, n_elements):   
    samples_subset = [samples[i][:n_elements] for i in range(0,len(samples))]
    return samples_subset

def compute_2d_kde(grid_corners, r_windowed, n_kde=512, weighting_fcn = [None]):
    
    [x_min, x_max, y_min, y_max] = grid_corners
    #prepare axes of grid on which to perform KDE (2D only for now)
    x_axis, y_axis = np.meshgrid(np.linspace(x_min, x_max, n_kde), np.linspace(y_min, y_max, n_kde))
    x_axis = x_axis.flatten()
    y_axis = y_axis.flatten()
    
    output_kale = [] #list of KALE objects for each window
    output_kde = [] #list of KDE PDFs for each window
    for i_win in range(0,len(r_windowed)):
        
        x_win = r_windowed[i_win][0]
        y_win = r_windowed[i_win][1]
        
        
        if len(weighting_fcn) > 1:
            #x_weights = np.linspace(0,15,len(x_win))
            t_weights = weighting_fcn 
            # t_weights = np.exp(x_weights) #exponential weighting 
            # t_weights = np.ones(len(x_subset)) #equal weighting            
            kde_kale = kale.KDE([x_win,y_win], weights=t_weights)            
        else:
            kde_kale = kale.KDE([x_win,y_win])

                        
            
        output_kale.append(kde_kale) #used later when generating samples and plots
    
        xy_grid, pdf_kde = kde_kale.density([x_axis, y_axis], probability=True)
        # xy_grid, pdf_kde = kde_kale.density([x_axis, y_axis], reflect=True, probability=True)
        pdf_kde = pdf_kde.reshape((n_kde, n_kde))
        output_kde.append([pdf_kde, np.linspace(x_min, x_max, n_kde), np.linspace(y_min, y_max, n_kde)])
    
    # normalize the PDFs
    for i in range(0,len(output_kde)):
        output_kde[i][0]=1*output_kde[i][0]/np.sum(output_kde[i][0])
        
    return output_kale, output_kde

def compute_kde(samples, xmin, xmax, bw_method, n_kde=512, kernel='gaussian', kdepy_comp_method="fft", save_kde_path=None, mirror_data=True, pp=False):
      
    if mirror_data:    # mirror data
        samples_mirrored = mirror(samples, xmin)
        x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde)        
    else:
        samples_mirrored = samples
        x_mirrored = np.linspace(xmin, xmax, n_kde)

    if kdepy_comp_method=="fft":
        if pp:
            kdes = [dask.delayed(FFTKDE)(kernel=kernel, bw=bw_method).fit(samples_mirrored[i]).evaluate(grid_points=x_mirrored) for i in range(0,len(samples_mirrored))]
            kde = dask.compute(*kdes) 
        else:
            kde = [FFTKDE(kernel=kernel, bw=bw_method).fit(samples_mirrored[i]).evaluate(grid_points=x_mirrored) for i in range(0,len(samples_mirrored))]
    elif kdepy_comp_method=="naive":
        if pp:
            kdes = [dask.delayed(NaiveKDE)(kernel=kernel, bw=bw_method).fit(samples_mirrored[i]).evaluate(grid_points=x_mirrored) for i in range(0,len(samples_mirrored))]
            kde = dask.compute(*kdes) 
        else:
            kde = [NaiveKDE(kernel=kernel, bw=bw_method).fit(samples_mirrored[i]).evaluate(grid_points=x_mirrored) for i in range(0,len(samples_mirrored))]
    elif kdepy_comp_method=="tree":
        if pp:
            kdes = [dask.delayed(TreeKDE)(kernel=kernel, bw=bw_method).fit(samples_mirrored[i]).evaluate(grid_points=x_mirrored) for i in range(0,len(samples_mirrored))]
            kde = dask.compute(*kdes) 
        else:
            kde = [TreeKDE(kernel=kernel, bw=bw_method).fit(samples_mirrored[i]).evaluate(grid_points=x_mirrored) for i in range(0,len(samples_mirrored))]
    else:
        print("Specified KDEpy computation method not supported")
        return None

    if mirror:
        kde = [np.split(kde[i],2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE
    else:
        kde = [kde[i][1] for i in range(0,len(kde))]
        
    if save_kde_path!=None:    
        kde_save =[kde[i].astype(np.float32) for i in range(0,len(kde))]#convert from float64 to float32 to save space
        # np.save(save_kde_path, kde_save)
        Path(save_kde_path).mkdir(parents=True, exist_ok=True)
        np.savez_compressed(save_kde_path, kde_save) #save in compressed .npz format    
    
    return kde


def compute_arvizkde(samples, xmin, xmax, bw_method, n_kde=512, kernel='gaussian', save_kde_path=None, adaptive=True, mirror_data=True, pp=False):

    if mirror_data:    # mirror data
        samples_mirrored = mirror(samples, xmin)
        x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde)        
    else:
        samples_mirrored = samples
        x_mirrored = np.linspace(xmin, xmax, n_kde)

    if pp:
        kdes = [dask.delayed(arviz.kde)(samples_mirrored[i], bw=bw_method, grid_len=n_kde, bw_return=True, custom_lims=(x_mirrored[0],x_mirrored[-1]), adaptive=adaptive) for i in range(0,len(samples_mirrored))]
        arviz_kde = dask.compute(*kdes)
        # grid = [arviz_kde[i][0] for i in range(0,len(arviz_kde))]
        kde = [arviz_kde[i][1] for i in range(0,len(arviz_kde))]
        # bandwidth = [arviz_kde[i][2] for i in range(0,len(arviz_kde))]

    else:
        arviz_kde = [arviz.kde(samples_mirrored[i], bw=bw_method, grid_len=n_kde, bw_return=True, custom_lims=(x_mirrored[0],x_mirrored[-1]), adaptive=adaptive) for i in range(0,len(samples_mirrored))]
        # grid = [arviz_kde[i][0] for i in range(0,len(arviz_kde))]
        kde = [arviz_kde[i][1] for i in range(0,len(arviz_kde))]
        # bandwidth = [arviz_kde[i][2] for i in range(0,len(arviz_kde))]

    kde = [np.split(kde[i],2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE

    if save_kde_path!=None:    
        kde_save =[kde[i].astype(np.float32) for i in range(0,len(kde))]#convert from float64 to float32 to save space
        # np.save(save_kde_path, kde_save)
        Path(save_kde_path).mkdir(parents=True, exist_ok=True)
        np.savez_compressed(save_kde_path, kde_save) #save in compressed .npz format    
    
    return kde
    

def compute_adaptivekde(samples, xmin, xmax, bw_method, n_kde=512, save_kde_path=None, mirror_data=True, pp=False, **kwargs):
    
    if mirror_data:    # mirror data
        samples_mirrored = mirror(samples, xmin)
        x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde)        
    else:
        samples_mirrored = samples
        x_mirrored = np.linspace(xmin, xmax, n_kde)

    
    if bw_method=="adaptive-global":
        if pp: #use Dask for parallel processing
            # LIST COMPREHENSION style
            kdes = [dask.delayed(adaptivekde.sskernel)(samples_mirrored[i], tin = x_mirrored, **kwargs) for i in range(0,len(samples_mirrored))] 
            kde = dask.compute(*kdes) 
        else: #vanilla
            kde = [adaptivekde.sskernel(samples_mirrored[i], tin = x_mirrored, **kwargs) for i in range(0,len(samples_mirrored))]

    elif bw_method=="adaptive-local":
        if pp:
            # LIST COMPREHENSION style
            kdes = [dask.delayed(adaptivekde.ssvkernel)(samples_mirrored[i], tin = x_mirrored, **kwargs) for i in range(0,len(samples_mirrored))] 
            kde = dask.compute(*kdes) 
        else: #vanilla
            print("yes")
            kde = [adaptivekde.ssvkernel(samples_mirrored[i], tin = x_mirrored, **kwargs) for i in range(0,len(samples_mirrored))]
    
    kde = [np.split(kde[i][0],2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE
    # t = np.array([kde[i][1].astype(np.float32) for i in range(0,len(kde))])
    # bw = np.array([kde[i][2].astype(np.float32) for i in range(0,len(kde))])

    
    if save_kde_path!=None:
        kde_save = np.array([kde[i].astype(np.float32) for i in range(0,len(kde))]) #convert from float64 to float32 to save space
        # t_save = np.array([t[i].astype(np.float32) for i in range(0,len(kde))])
        # bw_save = np.array([bw[i].astype(np.float32) for i in range(0,len(kde))])
        
        Path(save_kde_path).mkdir(parents=True, exist_ok=True)
        np.savez_compressed(save_kde_path, kde_save) #save in compressed .npz format 
    
    return kde

def compute_diffkde(samples, xmin, xmax, n_kde=512, save_kde_path=None, mirror_data=True, pp=False):

    if mirror_data:    # mirror data
        samples_mirrored = mirror(samples, xmin)
        x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde)        
    else:
        samples_mirrored = samples
        x_mirrored = np.linspace(xmin, xmax, n_kde)

    if pp: #use Dask for parallel processing
        kdes = [dask.delayed(diffKDE.KDE)(samples_mirrored[i], xmin=x_mirrored.min(), xmax=x_mirrored.max(), n=len(x_mirrored)) for i in range(0,len(samples_mirrored))] 
        kde = dask.compute(*kdes)
    else: #vanilla
        kde = [diffKDE.KDE(samples_mirrored[i], xmin=x_mirrored.min(), xmax=x_mirrored.max(), n=len(x_mirrored)) for i in range(0,len(samples_mirrored))] # adaptive kernel

    kde = [np.split(kde[i][0][1:],2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE

    if save_kde_path!=None:    
        kde_save = np.array([kde[i].astype(np.float32) for i in range(0,len(kde))]) #convert from float64 to float32 to save space
        Path(save_kde_path).mkdir(parents=True, exist_ok=True)
        np.savez_compressed(save_kde_path, kde_save) #save in compressed .npz format 

    return kde


def compute_fastkde(samples, xmin, xmax, n_kde=512+1, save_kde_path=None, mirror_data=True, pp=False):
    
    if mirror_data:    # mirror data
        samples_mirrored = mirror(samples, xmin)
        x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde)        
    else:
        samples_mirrored = samples
        x_mirrored = np.linspace(xmin, xmax, n_kde)
    
    if pp: #use Dask for parallel processing
        kdes = [dask.delayed(fastKDE.pdf)(samples_mirrored[i], numPoints = n_kde) for i in range(0,len(samples_mirrored))] 
        kde = dask.compute(*kdes)
    else: #vanilla        
        kde = [fastKDE.pdf(samples_mirrored[i], numPoints = n_kde) for i in range(0,len(samples_mirrored))]
    
    kde = [np.split(kde[i][0][1:],2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE

    if save_kde_path!=None:    
        kde_save = np.array([kde[i].astype(np.float32) for i in range(0,len(kde))]) #convert from float64 to float32 to save space
        Path(save_kde_path).mkdir(parents=True, exist_ok=True)
        np.savez_compressed(save_kde_path, kde_save) #save in compressed .npz format 

    return kde

def compute_lightkde(samples, xmin, xmax, n_kde=512, save_kde_path=None, pp=False):
    
    # mirror data
    samples_mirrored = mirror(samples, xmin)
    x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde)

    if pp: #use Dask for parallel processing
        kdes = [dask.delayed(kde_1d)(sample_vec=samples_mirrored[i], n_x_vec=n_kde, x_min=x_mirrored.min(), x_max=x_mirrored.max()) for i in range(0,len(samples_mirrored))]
        kde = dask.compute(*kdes)
    else:
        kde = [kde_1d(sample_vec=samples_mirrored[i], n_x_vec=n_kde, x_min=x_mirrored.min(), x_max=x_mirrored.max()) for i in range(0,len(samples_mirrored))]
        
    kde = [np.split(np.array(kde[i][0]),2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE and discard x vector

    
    if save_kde_path!=None:    
        kde_save = np.array([kde[i].astype(np.float32) for i in range(0,len(kde))]) #convert from float64 to float32 to save space
        Path(save_kde_path).mkdir(parents=True, exist_ok=True)
        np.savez_compressed(save_kde_path, kde_save) #save in compressed .npz format 
    
    return kde

def compute_kalekde(samples, xmin, xmax, n_kde=512, save_kde_path=None, pp=False):
    
    # mirror data
    samples_mirrored = mirror(samples, xmin)
    x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde)

    if pp: #use Dask for parallel processing
        kdes = [dask.delayed(density)(samples_mirrored[i], points=x_mirrored) for i in range(0,len(samples_mirrored))]
        kde = dask.compute(*kdes)
    else:
        kde = [density(samples_mirrored[i], points=x_mirrored) for i in range(0,len(samples_mirrored))]
        
    kde = [np.split(np.array(kde[i][1]),2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE and discard x vector
    
    if save_kde_path!=None:    
        kde_save = np.array([kde[i].astype(np.float32) for i in range(0,len(kde))]) #convert from float64 to float32 to save space
        Path(save_kde_path).mkdir(parents=True, exist_ok=True)
        np.savez_compressed(save_kde_path, kde_save) #save in compressed .npz format 
    
    return kde


def h_plat(x, solver):

    n = len(x)
    x = np.sort(x)
    sig = np.std(x, ddof=1)
    interval = np.array([0.1 * sig / n**0.2, 2 * sig / n**0.2])
    x1 = funct(interval[0], x)
    x2 = funct(interval[1], x)

    if x1 * x2 < 0:
        fun = lambda t: funct(t, x)
        # sol = root_scalar(fun, method='bisect', bracket=interval)
        sol = root_scalar(fun, method=solver, bracket=interval)
        h = sol.root
    else:
        y1 = 10 ** (np.floor(np.log10(interval[0]))) / 10
        x1 = funct(y1, x)
        x2 = funct(interval[0], x)
        if x1 * x2 < 0:
            interval[1] = interval[0]
            interval[0] = y1
            fun = lambda t: funct(t, x)
            sol = root_scalar(fun, bracket=interval)
            h = sol.root
        else:
            y1 = 10 ** (np.floor(np.log10(interval[0]))) / 10
            dy = 0.05 * y1
            k = 0
            hh = []
            for i in np.arange(y1, interval[0], dy):
                k += 1
                hh.append(funct(i, x))
            k = np.argmin(np.abs(hh))
            h = y1 + (k - 1) * dy

    return h


def funct(t, x):
    p2 = 1.41421356
    n = len(x)
    yy = np.zeros(n)
    for i in range(n):
        xij = (x - x[i])**2 / t**2
        y = np.exp(-xij / 4) * ((xij / 2 - 1) / p2) - 2 * np.exp(-xij / 2) * (xij - 1)
        yy[i] = np.sum(y)
    fct = np.sum(yy) - 2 * n
    return fct

def compute_lskde(samples, xmin, xmax, n_kde=512, kernel='gaussian', solver='brenth', save_kde_path=None, pp=False):

    # mirror data
    samples_mirrored = mirror(samples, xmin)
    x_mirrored = np.linspace(2*xmin-xmax, xmax, n_kde) # new way
    # x_mirrored = np.linspace(xmin-5, xmin+5, n_kde) # old way (runs 1 to 4)

    h = h_plat(samples_mirrored, solver)
    print(h)
    if pp:
        kdes = [dask.delayed(arviz.kde)(samples_mirrored[i], bw=h, grid_len=n_kde, custom_lims=(x_mirrored[0],x_mirrored[-1])) for i in range(0,len(samples_mirrored))]
        arviz_kde = dask.compute(*kdes)
        # grid = [arviz_kde[i][0] for i in range(0,len(arviz_kde))]
        kde = [arviz_kde[i][1] for i in range(0,len(arviz_kde))]

    else:
        # arviz_kde = [arviz.kde(samples_mirrored[i], bw=h, grid_len=n_kde, custom_lims=(x_mirrored[0],x_mirrored[-1])) for i in range(0,len(samples_mirrored))]
        # kde = [arviz_kde[i][1] for i in range(0,len(arviz_kde))]
        
        kde = [FFTKDE(kernel=kernel, bw=h).fit(samples_mirrored[i]).evaluate(grid_points=x_mirrored) for i in range(0,len(samples_mirrored))]


    kde = [np.split(kde[i],2)[1] for i in range(0,len(kde))] #keep only one half of the full KDE

    if save_kde_path!=None:    
        kde_save =[kde[i].astype(np.float32) for i in range(0,len(kde))]#convert from float64 to float32 to save space
        # np.save(save_kde_path, kde_save)
        Path(save_kde_path).mkdir(parents=True, exist_ok=True)
        np.savez_compressed(save_kde_path, kde_save) #save in compressed .npz format    
    
    return kde