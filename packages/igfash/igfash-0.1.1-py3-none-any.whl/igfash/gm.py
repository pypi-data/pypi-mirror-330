import numpy as np
from scipy.stats import t, norm
from pyroots import Brentq, Brenth, Ridder, Bisect
from scipy.optimize import root_scalar
# from scipy.optimize.cython_optimize import brentq
from timeit import default_timer as timer

from openquake.hazardlib.geo import Point #This class represents a geographical point in terms of longitude, latitude, and depth (with respect to the Earth surface).
from openquake.hazardlib.geo.surface.planar import PlanarSurface
from openquake.hazardlib.source.characteristic import CharacteristicFaultSource
from openquake.hazardlib.mfd import ArbitraryMFD
from openquake.hazardlib.tom import PoissonTOM
from openquake.hazardlib.scalerel import WC1994 #Wells and Coppersmith magnitude – rupture area relationships
from openquake.hazardlib.site import Site, SiteCollection
from openquake.hazardlib.contexts import ContextMaker
from openquake.hazardlib.valid import gsim
from openquake.hazardlib.imt import PGA, PGV, SA

import utm
import sys

# class GMPE:
#     r"""An object containing all aspects of a GMPE (Ground Motion Prediction Equation).

#     """

#     def __init__(self, alpha, beta, gamma, h, SEE, Cb, num_records):
#         """Create a GMPE object by providing the parameters and number of
#         ground motion records used in creating the model.

#         Parameters
#         ----------
#         alpha: float
#             Intercept of regression
        
#         beta: float
#             Magnitude coefficient of regression

#         gamma: float
#             Distance attenuation coefficient of regression

#         h: integer
#             Depth factor in metres
            
#         SEE: float
#             Standard error of estimate
            
#         Cb: 3x3 numpy array
#             Covariance matrix

#         num_records: integer
#             Number of ground motion records in GMPE estimation

#         """
#         self.alpha = alpha
#         self.beta = beta
#         self.gamma = gamma
#         self.h = h
#         self.SEE = SEE
#         self.Cb = Cb
#         self.num_records = num_records
        
        

def compute_PGA_exceedance(rx_lat, rx_lon, r, fr, p, lambdas, D, percentages_D, magnitudes, magnitude_pdf, magnitude_cdf, model, products=['PGA'], PGA_min=0.01, PGA_max=2.0, rx_label=None, verbose=False, precision=5e-3):
           
    n_events = len(r)
    
    #make context here
    
    try:
        gmpes = [gsim(model)]
    except:
        print("Not a valid GMPE model")
        sys.exit() 
    
    #placeholder values that do not have any effect
    Mag = 5.0 #placeholder mag, must be valid for that context; will be overwritten in loop
    rupture_aratio = 1.5
    Strike = 0
    Dip = 90
    Rake = 0
    
    Hypocenter = Point(rx_lon, rx_lat, 0.0) #does not matter in our case; just set eq location to be same as receiver
    #according to the magnitude and MSR calculate planar surface
    planar_surface = PlanarSurface.from_hypocenter(
            hypoc=Hypocenter,
            msr=WC1994(),
            mag=Mag,
            aratio=rupture_aratio,
            strike=Strike,
            dip=Dip,
            rake=Rake,
            )

    # site for which we compute (receiver location)    
    site_collection = SiteCollection([Site(location=Point(rx_lon, rx_lat, 0))])

    imtls = {s: [0] for s in products} #required for context maker, M = 2 IMTs

    context_maker = ContextMaker('Induced', gmpes, {'imtls': imtls, 'mags': [Mag]}) #necessary contexts builder

    src = CharacteristicFaultSource(source_id = 1,
                                    name = 'rup',
                                    tectonic_region_type = 'Induced',
                                    mfd = ArbitraryMFD([Mag], [0.01]), #this does not have any effect
                                    temporal_occurrence_model = PoissonTOM(50.), #this is also not really used
                                    surface = planar_surface,
                                    rake = Rake)

    ctx = context_maker.from_srcs([src],site_collection)[0] #returns one context from the source for one rupture
     
    # @jit(nopython=True, parallel=True)
    def exceedance_root_function(a):
        exceedance_prob_sum = 0
        
        for j in range(len(lambdas)): #loop through all lambdas
            lambda_j = lambdas[j]
            D_j = percentages_D[j] * D
            
            for i in range(n_events): #loop through all events
                ri = r[i]  # Epicentral distance
                fr_i = fr[i]  # Location probability f(r)
                
                ctx.repi = ri
                              
                for k in range(len(magnitudes)): #loop through all values of magnitude pdf and cdf
                    m = magnitudes[k]
                    f_m = magnitude_pdf[k]
                    F_m = magnitude_cdf[k]
                    
                    # update context magnitude 
                    ctx.mag = m
                    
                    f_conditional = (lambda_j * D_j * f_m * np.exp(-lambda_j * D_j * (1 - F_m))) / (1 - np.exp(-lambda_j * D_j))
                    
                    mean, sig, tau, phi = context_maker.get_mean_stds(ctx) #use context maker to calculate
                    means = np.exp(mean)
                    
                    gm_predicted = means[0][0][0]
                    variance_term = sig[0][0][0]
                                        
                    residual = np.log(a) - np.log(gm_predicted)
                    
                    
                    if residual <= 0:
                        exceedance_probability = 1
                    else:
                        t_value = residual / variance_term
                        
                        if model == 'Lasocki2013':
                            num_ground_motion_records = 1196
                            F_t = t.cdf(t_value, num_ground_motion_records - 3) # student t distribution, degrees of freedom: n-3
                        else:
                            F_t = norm.cdf(t_value)
                        
                        exceedance_probability = 1 - F_t
                    
                    location_exceedance_prob = exceedance_probability * f_conditional * fr_i
                    exceedance_prob_sum += location_exceedance_prob
                
        print("Return", exceedance_prob_sum - p)
        return exceedance_prob_sum - p
    
    # Check function values at different test points
    PGA_mid = (PGA_max-PGA_min)/2
    lower_bound_value = exceedance_root_function(PGA_min)
    mid_point_value = exceedance_root_function(PGA_mid)
    upper_bound_value = exceedance_root_function(PGA_max)
    
    print('Receiver:', str(rx_label))
    print('Function value at PGA = ', str(PGA_min), f': {lower_bound_value}')
    print('Function value at PGA = ', str(PGA_mid), f': {mid_point_value}')
    print('Function value at PGA = ', str(PGA_max), f': {upper_bound_value}')
    
    if np.sign(lower_bound_value) == np.sign(upper_bound_value):
        raise ValueError('Function values at the interval endpoints must differ in sign for fsolve to work.')
    
    # Find root of function
    start = timer()
    
    # output = root_scalar(exceedance_root_function, method='brenth', bracket=[0.01, 2]) #using scipy
    # output = excitingmixing(exceedance_root_function, xin=1) # using scipy excitingmixing solver
    # print('Estimated PGA Value:', output.root)

    #use pyroots with less overhead and allows reduced precision
    # precision = 5e-3 #precision of the solution
    # precision = 1e-6 #precision of the solution
    
    # method = "Brentq"
    method = "Brenth"

    
    if method == "Brentq":
        solver = Brentq(epsilon=precision)
    elif method == "Brenth":
        solver = Brenth(epsilon=precision)
    # solver = Ridder(epsilon=precision)
    # solver = Bisect(epsilon=precision)
        
    try:
        print("Pyroots", method, "precision", precision)
        output = solver(exceedance_root_function, PGA_min, PGA_max) #use pyroots
        pga = output.x0
        
        # DEBUG
        # print("Pyroots: use bracket 0.01 to 0.1")
        # output = solver(exceedance_root_function, 0.01, 0.1) #use pyroots
        
        
        # DEBUG use scipy
        # method='brentq'
        # method='brenth'
        # method='toms748'
        # method='newton'
        # xtol = 0.01
        # rtol = 0.01
        
        # print("Scipy", method, "xtol=", xtol, "rtol=", rtol)
        # output = root_scalar(exceedance_root_function, bracket=[PGA_min, PGA_max], method=method) #use default xtol and rtol
        # output = root_scalar(exceedance_root_function, bracket=[PGA_min, PGA_max], xtol=xtol, rtol=rtol, method=method)
        # pga = output.root
        
        # print("Details:", output) if verbose else lambda *a, **k: None

        
    except Exception as error:
        print("An exception occurred while solving using pyroots Brentq:", error)
        
        
        # use Scipy solver
        try: 
            print("Now trying Scipy Brenth method...")
            method='Brenth'
            output = root_scalar(exceedance_root_function, bracket=[PGA_min, PGA_max], rtol=0.01, method=method)
            pga = output.root
            
        except Exception as error:
            print("An exception occurred:", error)
            print("Set PGA value to -1")
            # pga = np.nan
            pga = -1
        
    end = timer()
    print("PGA Computation time: ", end - start, "seconds")

    print("Estimated PGA:", pga)
    return pga