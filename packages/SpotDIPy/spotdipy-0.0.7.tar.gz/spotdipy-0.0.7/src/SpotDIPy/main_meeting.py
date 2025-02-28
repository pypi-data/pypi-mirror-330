import numpy as np
from SpotDIPy import SpotDIPy
import multiprocessing
import pickle
from glob import glob


DIP = SpotDIPy(cpu_num=multiprocessing.cpu_count() - 1, platform_name='cpu')

""" Set required parameters """
DIP.set_param('t0', value=2454254.621769)  # Refernce time [day]
DIP.set_param('period',  value=2.981897)   # Equatorial rotation period [day]
DIP.set_param('Tphot', value=6539)  # Photospheric temperature [K]
DIP.set_param('Tcool', value=4188)  # Minimum spot temperature [K]
DIP.set_param('Thot', value=7500)  # Maximum spot temperature [K]
DIP.set_param('incl', value=45)  # Axial inclination [deg]
# DIP.set_param('vsini', value=20.138)  # Equatorial rotation velocity [km/s]
DIP.set_param('R', value=1.668)  # Stellar radius [Ro]
DIP.set_param('vrt', value=6.79)  # Macroturbulence velocity [km/s]
DIP.set_param('mass', value=1.41)  # Stellar Mass [Mo]
DIP.set_param('dOmega', value=0.0)  # Delta Omega [rad/day] (for differantial rotation)
DIP.set_param('resolution', value=65000)  # Spectral resolution
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Set Lim-darkening parameters (via ExoTiC-LD Python package) """
# mh == Metallicity
# law == LD law
# model == Model atmosphere
# mu_min = Minumum mu angle
DIP.set_limb_darkening_params(mh=-0.18, law='linear', model='mps2', mu_min=0.1,
                              data_path='/media/eng/Storage/ExoTiC-LD_data_v3.1.2')
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Set modes """
DIP.set_conf({
    'line': {'mode': 'on',  # If observed spectral data is available
             'wave_range': [4412, 7838],  # Spectral wavelength range
             'eqw': 0.08547,  # Equivalent width
             'scaling': {'method': 'mean'},  # Scaling method for observed and synthetic profiles
             'corr': {'rv': None, 'amp': None}  # Radial velocity and amplitude correction
             },
    'lc': {'mode': 'on',  # If observed light curve data is available
           'passband': 'CorotAS',  # Passband of the observed light curve
           'scaling': {'method': 'mean'},  # Scaling method for observed and synthetic light curves
           'corr': {'amp': None}  # Amplitude correction
           }
})
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Construction surface grid """
# method = Method of construction surface grid --> healpy, trapezoid, phoebe2_marching
# nlats = Number of latitudes for trapezoid surface grid
# DIP.construct_surface_grid(method='phoebe2_marching', noes=11000)
DIP.construct_surface_grid(method='trapezoid', nlats=40)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Import initial local profiles (LLP) (for photosphere, cool and hot spots) data"""
llp_vels = np.loadtxt('spectrum_Teff6539_logg4.12_mh-0.18_alpha0.06_vmic1.88_vmac0.0_vsini0.0_'
                      'ld0.0_R0_with_err_lsd.out', skiprows=2)[:, 0]
llp_phot_int = np.loadtxt('spectrum_Teff6539_logg4.12_mh-0.18_alpha0.06_vmic1.88_vmac0.0_vsini0.0'
                          '_ld0.0_R0_with_err_lsd.out', skiprows=2)[:, 1]
llp_cool_int = np.loadtxt('spectrum_Teff4188_logg4.12_mh-0.18_alpha0.06_vmic1.88_vmac0.0_vsini0.0'
                          '_ld0.0_R0_with_err_lsd.out', skiprows=2)[:, 1]
llp_hot_int = np.loadtxt('spectrum_Teff7000_logg4.12_mh-0.18_alpha0.06_vmic1.88_vmac0.0_vsini0.0'
                         '_ld0.0_R0_with_err_lsd.out', skiprows=2)[:, 1]

DIP.set_local_profiles({'line': {'lp_vels': llp_vels, 'phot_lp_data': llp_phot_int, 'cool_lp_data': llp_cool_int,
                                 'hot_lp_data': llp_hot_int}})
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Make a test """
# lats_spots = [0, 30., 60., -30.]  # spot latitudes (degrees)
# longs_spots = [0., 90., 180., 270.]  # spot longitudes (degrees)
# rs_spots = [15., 15, 15., 15.]  # spot radii (degrees)
# cs_cools = [0.9, 0.0, 0.8, 0.0]  # cool spot contrast between 0 and 1
# cs_hots = [0.0, 0.8, 0.0, 0.8]  # hot spot contrast between 0 and 1
#
# spots_params = {'lats_spots': lats_spots, 'longs_spots': longs_spots, 'rs_spots': rs_spots, 'cs_cools': cs_cools,
#                 'cs_hots': cs_hots}
#
# line_phases = np.arange(0, 1.0, 0.1)
# line_times = DIP.params['t0'] + DIP.params['period'] * line_phases
# line_vels = np.arange(-32, 32 + 1.0, 1.0)
# line_snr = 3000
#
# lc_phases = np.arange(0.0, 1.0 + 0.01, 0.01)
# lc_times = DIP.params['t0'] + DIP.params['period'] * lc_phases
# lc_snr = 3000
#
# opt_params = {'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0, 'delta': 1.0, 'lmbd': 1, 'maxiter': 5000,
#               'tol': 1e-5, 'disp': True}
#
# modes_inp = {'line': {'times': line_times, 'vels': line_vels, 'snr': line_snr},
#              'lc': {'times': lc_times, 'snr': lc_snr}}
#
# plot_params = {'line_sep_prf': 0.05, 'line_sep_res': 0.005, 'mol_sep_prf': 0.03, 'mol_sep_res': 0.01,
#                'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
#                'ticklabelsize': 12}
#
# DIP.test(spots_params, modes_input=modes_inp, opt_params=opt_params, plot_params=plot_params,
#          save_data_path="test_find_per_incl.pkl")
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

file = open('test_find_per_incl.pkl', 'rb')
input_data_dict = pickle.load(file)
file.close()

# data = np.zeros((len(input_data_dict['lc']['times']), 3))
# data[:, 0] = input_data_dict['lc']['times']
# data[:, 1] = input_data_dict['lc']['data'][:, 0]
# data[:, 2] = input_data_dict['lc']['data'][:, 1]
# np.savetxt('target_lc/Test_lc.txt', data)

# for i, item in enumerate(input_data_dict['line']['times']):
#     data = input_data_dict['line']['data'][i]
#     np.savetxt('target_LSDs/Test_' + str(item) + '_lsd.out', data)

paths = glob("target_LSDs/Test_*.out")
line_times = []
line_data = []
for path in paths:
    line_times.append(float(path.split('/')[-1].split('_')[1]))
    data = np.loadtxt(path)
    line_data.append(data)

data = np.loadtxt("target_lc/Test_lc.txt")
lc_times = data[:, 0]
lc_flux = data[:, 1]
lc_err = data[:, 2]
lc_data = np.vstack((data[:, 1], data[:, 2])).T

input_data_dict = {'line': {'times': line_times, 'data': line_data},
                   'lc': {'times': lc_times, 'data': lc_data}}

DIP.set_input_data(input_data_dict)

""" Grid Search """
# opt_params = {'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0, 'delta': 1.0, 'lmbd': 2.0, 'maxiter': 3500,
#               'tol': 1e-5, 'disp': True}
#
# fit_params = {
#                 # 'dOmega': np.linspace(-1.0, -0.1, 20),
#                 'period': np.linspace(2.5, 3.5, 30),
#                 # 'vsini': np.linspace(16, 23, 10),
#                 # 'R': np.linspace(1.3, 1.8, 20),
#                 # 'vrt': np.linspace(0, 10, 20),
#                 # 'resolution': np.linspace(0.0, 65000, 50),
#                 'incl': np.arange(10, 90, 2.5),
#                 # 'eqw': np.linspace(0.0858 - 0.003, 0.0858 + 0.001, 50)
#                 # 'Tcool': np.linspace(3800, 6539, 30),
#                 # 'Thot': np.linspace(6539, 8500, 30)
#
#                 }
#
# DIP.grid_search(fit_params, opt_params, save='sil2.pkl')
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

recons_result = DIP.reconstructor(alpha=1.0, beta=1.0, gamma=1.0, delta=1, lmbd=7, maxiter=5500, tol=1e-5,
                                  disp=True)

DIP.plot(plot_params={'line_sep_prf': 0.06, 'line_sep_res': 0.01, 'mol_sep_prf': 0.3, 'mol_sep_res': 0.2,
                      'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
                      'ticklabelsize': 12})