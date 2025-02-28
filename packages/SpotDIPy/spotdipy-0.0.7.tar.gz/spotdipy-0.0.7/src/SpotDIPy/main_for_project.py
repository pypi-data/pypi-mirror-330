import numpy as np
from SpotDIPy import SpotDIPy
import multiprocessing
import pickle


if __name__ == '__main__':
    # multiprocessing.cpu_count() - 1
    DIP = SpotDIPy(cpu_num=multiprocessing.cpu_count() - 2, platform_name='cpu')

    DIP.set_param('t0', value=55006.4976)
    DIP.set_param('period', value= 3.4693)
    DIP.set_param('Tphot', value=5250)
    DIP.set_param('Tcool', value=4250)
    DIP.set_param('Thot', value=5250)
    DIP.set_param('incl', value=75)
    DIP.set_param('vsini', value=31.0)
    # DIP.set_param('R', value=1.668)
    DIP.set_param('vrt', value=0.0)
    DIP.set_param('mass', value=1.7)
    DIP.set_param('dOmega', value=-0.090554)
    DIP.set_param('resolution', value=0)
    DIP.set_limb_darkening_params(mh=0.0, law='linear', model='mps2', mu_min=0.1, data_path="/home/eng/Storage/ExoTiC-LD_data_v3.1.2")

    DIP.set_conf({
        'line': {'mode': 'off',
                 'wave_range': [4412, 7838],
                 'eqw': 0.0848368,
                 'scaling': {'method': 'mean'},
                 'corr': {'rv': None, 'amp': None}
                 },
        'lc': {'mode': 'on',
               'passband': 'Kepler',
               'scaling': {'method': 'mean'},
               'corr': {'amp': None}
               }
    })

    # DIP.construct_surface_grid(method='phoebe2_marching', noes=4000)
    # DIP.construct_surface_grid(method='healpy', nside=16)
    DIP.construct_surface_grid(method='trapezoid', nlats=10)

    llp_vels = np.loadtxt('teff5500_logg4.3_mh0.00_vmic1.7_lsd.out', skiprows=2)[:, 0]
    llp_phot_int = np.loadtxt('teff5500_logg4.3_mh0.00_vmic1.7_lsd.out', skiprows=2)[:, 1]
    llp_cool_int = np.loadtxt('teff4500_logg4.3_mh0.00_vmic1.7_lsd.out',  skiprows=2)[:, 1]
    llp_hot_int = np.loadtxt('teff6000_logg4.3_mh0.00_vmic1.7_lsd.out', skiprows=2)[:, 1]

    DIP.set_local_profiles({'line': {'lp_vels': llp_vels, 'phot_lp_data': llp_phot_int, 'cool_lp_data': llp_cool_int,
                                'hot_lp_data': llp_hot_int}})


    """ Make a test """
    lats_spots = [20., 40.]  # spot latitudes (degrees)
    longs_spots = [0., 100.]  # spot longitudes (degrees)
    rs_spots = [12., 10.]  # spot radius (degrees)
    cs_cools = [0.8, 0.8]  # cool spot contrast between 0 and 1
    cs_hots = [0.0, 0.0]  # hot spot contrast between 0 and 1

    spots_params = {'lats_spots': lats_spots, 'longs_spots': longs_spots, 'rs_spots': rs_spots, 'cs_cools': cs_cools,
                    'cs_hots': cs_hots}

    line_phases = np.arange(0, 1.0, 0.1)
    # line_phases = np.linspace(0, 1.0, 770)
    line_times = DIP.params['t0'] + DIP.params['period'] * line_phases
    line_vels = np.arange(-60, 60 + 1.75, 1.75)
    line_snr = 3000

    # lc_phases = np.arange(0, 1, 0.01)
    lc_phases = np.linspace(0, 360, 360*100)
    lc_times = DIP.params['t0'] + DIP.params['period'] * lc_phases
    lc_snr = 3000

    opt_params = {'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0, 'delta': 1.0, 'lmbd': 1, 'maxiter': 2500,
                  'tol': 1e-5, 'disp': True}

    modes_inp = {'line': {'times': line_times, 'vels': line_vels, 'snr': line_snr},
                 'lc': {'times': lc_times, 'snr': lc_snr}}


    plot_params = {'line_sep_prf': 0.06, 'line_sep_res': 0.01, 'mol_sep_prf': 0.03, 'mol_sep_res': 0.01,
                   'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
                   'ticklabelsize': 12}

    # import utils as dipu
    # dipu.draw_3D_surf(DIP.params, DIP.surface_grid, spots_params)

    DIP.test(spots_params, modes_input=modes_inp, opt_params=opt_params, plot_params=plot_params)
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    # file = open('test_idc.pkl', 'rb')
    # input_data_dict = pickle.load(file)
    # file.close()
    #
    # DIP.set_input_data(input_data_dict)
    #
    # recons_result = DIP.reconstructor(alpha=1.0, beta=1.0, gamma=1.0, delta=1.0, lmbd=5.0, maxiter=2500, tol=1e-7,
    #                             disp=True)
    #
    # DIP.plot(plot_params={'line_sep_prf': 0.06, 'line_sep_res': 0.01, 'mol_sep_prf': 0.3, 'mol_sep_res': 0.2,
    #                       'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
    #                       'ticklabelsize': 12})

