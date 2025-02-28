import sys
sys.path.append('/home/eng/Dropbox/PythonProjects/SpotDIPy_GitHub/src/SpotDIPy')
from SpotDIPy import SpotDIPy


import numpy as np
import multiprocessing
import pickle
from glob import glob


DIP = SpotDIPy(cpu_num=1, platform_name='cpu')

""" Set required parameters """
DIP.set_param('t0', value=2453200.0)
DIP.set_param('period', value=1.756604)
DIP.set_param('Tphot', value=5080)
DIP.set_param('Tcool', value=3800)
DIP.set_param('Thot', value=5080)
DIP.set_param('incl', value=46)
DIP.set_param('vsini', value=21.827)
# DIP.set_param('R', value=0.78)
DIP.set_param('vrt', value=3.25)
DIP.set_param('mass', value=0.85)
DIP.set_param('dOmega', value=0.0)
DIP.set_param('resolution', value=65000)

DIP.set_limb_darkening_params(mh=-0.14, law='linear', model='mps2', mu_min=0.1, data_path="/home/eng/Storage/ExoTiC-LD_data_v3.1.2")

""" Set modes """
DIP.set_conf({
             'line': {'mode': 'on',
                    'wave_range': [5160, 5935],
                    'eqw': 0.09117,  # 0.09131
                    'scaling': {'method': 'mean'},
                    'corr': {'rv': None, 'amp': None}

                    },
             'lc': {'mode': 'off',
                    'passband': 'TESS',
                    'scaling': {'method': 'mean'},
                    'corr': {'amp': None}
                    }
             })
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Construction surface grid """
# DIP.construct_surface_grid(method='phoebe2_marching', noes=3800)
DIP.construct_surface_grid(method='trapezoid', nlats=40)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Import initial local profiles (LLP) (for photosphere, cool and hot spots) data"""
llp_vels = np.loadtxt('/home/eng/Dropbox/PythonProjects/PWAnd_new/synth_lsds/synth_T5080.0_logg4.4_mh-0.14_mic1.93_with-err_lsd.out', skiprows=2)[:, 0]
llp_phot_int = np.loadtxt('/home/eng/Dropbox/PythonProjects/PWAnd_new/synth_lsds/synth_T5080.0_logg4.4_mh-0.14_mic1.93_with-err_lsd.out', skiprows=2)[:, 1]
llp_cool_int = np.loadtxt('/home/eng/Dropbox/PythonProjects/PWAnd_new/synth_lsds/synth_T3800.0_logg4.4_mh-0.14_mic1.93_with-err_lsd.out',  skiprows=2)[:, 1]
llp_hot_int = np.loadtxt('/home/eng/Dropbox/PythonProjects/PWAnd_new/synth_lsds/synth_T5080.0_logg4.4_mh-0.14_mic1.93_with-err_lsd.out', skiprows=2)[:, 1]

DIP.set_local_profiles({'line': {'lp_vels': llp_vels, 'phot_lp_data': llp_phot_int, 'cool_lp_data': llp_cool_int,
                                 'hot_lp_data': llp_hot_int}})
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Make a test """
lats_spots = [0, 30., 60., -30.]  # spot latitudes (degrees)
longs_spots = [0., 90., 180., 270.]  # spot longitudes (degrees)
rs_spots = [15., 15, 15., 15.]  # spot radii (degrees)
cs_cools = [0.9, 0.7, 0.6, 0.8]  # cool spot contrast between 0 and 1
cs_hots = [0.0, 0.0, 0.0, 0.0]  # hot spot contrast between 0 and 1


# lats_spots = [30.]  # spot latitudes (degrees)
# longs_spots = [270.]  # spot longitudes (degrees)
# rs_spots = [20.]  # spot radii (degrees)
# cs_cools = [0.9]  # cool spot contrast between 0 and 1
# cs_hots = [0.0]  # hot spot contrast between 0 and 1

spots_params = {'lats_spots': lats_spots, 'longs_spots': longs_spots, 'rs_spots': rs_spots, 'cs_cools': cs_cools,
                'cs_hots': cs_hots}

# line_phases = np.arange(0, 1.0, 0.1)
# line_times = DIP.params['t0'] + DIP.params['period'] * line_phases

line_times = [2460594.92613, 2460594.97015, 2460595.01952, 2460595.06761, 2460595.92523, 2460595.97272,
              2460596.01977, 2460596.06687, 2460596.91335, 2460596.9596, 2460597.00919, 2460597.05649,
              2460597.10441, 2460597.15098, 2460597.1971, 2460597.24325]
line_vels = np.arange(-38, 40 + 2.3, 2.3)
line_snr = 300

# lc_phases = np.arange(0.0, 1.0 + 0.01, 0.01)
# lc_times = DIP.params['t0'] + DIP.params['period'] * lc_phases

lc_times = np.arange(2460594.92613, 2460597.24325 + 0.0024537, 0.0024537)
lc_snr = 3000

opt_params = {'alpha': 1.0, 'delta': 1.0, 'lmbd': 1, 'maxiter': 5000, 'tol': 1e-5, 'disp': True}

modes_inp = {'line': {'times': line_times, 'vels': line_vels, 'snr': line_snr},
             'lc': {'times': lc_times, 'snr': lc_snr}}

plot_params = {'line_sep_prf': 0.05, 'line_sep_res': 0.005, 'mol_sep_prf': 0.03, 'mol_sep_res': 0.01,
               'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
               'ticklabelsize': 12}

DIP.test(modes_input=modes_inp, spots_params=spots_params, opt_params=opt_params, plot_params=plot_params,
         save_data_path="test_find_per_incl.pkl")
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# recons_result = DIP.reconstructor(alpha=1.0, beta=1.0, gamma=1.0, delta=1, lmbd=7, maxiter=5500, tol=1e-5,
#                                   disp=True)
#
# DIP.plot(plot_params={'line_sep_prf': 0.06, 'line_sep_res': 0.01, 'mol_sep_prf': 0.3, 'mol_sep_res': 0.2,
#                       'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
#                       'ticklabelsize': 12})