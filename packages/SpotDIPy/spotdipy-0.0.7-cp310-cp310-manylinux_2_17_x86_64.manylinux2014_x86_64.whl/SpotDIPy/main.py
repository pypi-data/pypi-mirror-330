import numpy as np
from SpotDIPy import SpotDIPy
import multiprocessing
import pickle


if __name__ == '__main__':
    # multiprocessing.cpu_count() - 1

    DIP = SpotDIPy(cpu_num=multiprocessing.cpu_count() - 1, platform_name='cpu')

    """ Set required parameters """
    DIP.set_param('t0', value=2454254.621769409)  # set-1 in ilk verisinden
    DIP.set_param('period', value=2.9818966628011854)  # dOmega ve eqw ile grid search ile bulmayı deniyelim   2.971640252544775
    DIP.set_param('Tphot', value=6539)  # 6539 6411 tayf fitting den
    DIP.set_param('Tcool', value=4188)  # 4188 4151 lanza dan hesaplandı
    DIP.set_param('Thot', value=7500)  # 8500 bunu bilmiyoz
    DIP.set_param('incl', value=45)  # literatüre tekrar bakılıp yazılmalı
    # DIP.set_param('vsini', value=20.138)  # 20.1579
    DIP.set_param('R', value=1.668)  # literatüra tekrar bakılıp yazılmalı 1.668
    DIP.set_param('vrt', value=6.79)  # 6.79 6.26 tayf fitting den
    DIP.set_param('mass', value=1.41)  # literatüra tekrar bakılıp yazılmalı
    DIP.set_param('dOmega', value=0.0)  # period ve eqw ile grid search ile bulmayı deniyelim -0.5555555
    DIP.set_param('resolution', value=65000)  # Narval için 65000 diyolar

    DIP.set_limb_darkening_params(mh=-0.18, law='linear', model='mps2', mu_min=0.1,  # -0.18 -0.25 mh tayf fitting den
                                  data_path='/home/eng/Storage/ExoTiC-LD_data_v3.1.2')

    """ Set modes """
    DIP.set_conf({
        'line': {'mode': 'on',
                 # 'wave_range': [4890, 5890],
                 'wave_range': [4412, 7838],
                 # 'eqw': 0.0846,  # set-1 grid ile eqw-period-dOmega, 0.08588947368421052
                 # 'eqw': 0.086115789,  # set-1 grid ile eqw-dOmega
                 # 'eqw': 0.987,  # set-3 elle
                 # 'eqw': 0.0848368,  # set-3 grid ile, 0.0851 elle
                 # 'eqw': 0.08486896551724138,  # set-3 grid ile son
                 # 'eqw': 0.0851448275862069,  # set-1 grid ile son
                 'eqw': 0.0854666666666666,  # set-1 grid ile son-2 0.0854666666666666 0.5
                 # 'eqw': 0.0853633,  # set-1 ilk bölüm grid ile, 0.0851 elle
                 # 'eqw': 0.083,  # set-1 ilk bölüm deneme
                 'scaling': {'method': 'mean'},
                 'corr': {'rv': None, 'amp': None}  # set-1 elle
                 # 'corr': {'rv': -0.17, 'amp': None}  # set-3 elle
                 # 'corr': {'rv': 'free', 'amp': 'free'}
                 },
        'lc': {'mode': 'on',
               'passband': 'CorotAS',
               'scaling': {'method': 'mean'},
               'corr': {'amp': None}
               }
    })
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    """ Construction surface grid """
    # DIP.construct_surface_grid(method='phoebe2_marching', noes=11000)  # , test=True)
    # DIP.construct_surface_grid(method='healpy', nside=32)  # , test=True)
    DIP.construct_surface_grid(method='trapezoid', nlats=25)  # , test=True)
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    """ Import initial local profiles (LLP) (for photosphere, cool and hot spots) data"""
    # llp_vels = np.loadtxt('synths/old/lsds/spectrum_6744.0_4.16_-0.01_0.07_1.71_0.00_0.00_0.0_0_lsd.out', skiprows=2)[:, 0]
    # llp_phot_int = np.loadtxt('synths/old/lsds/spectrum_6744.0_4.16_-0.01_0.07_1.71_0.00_0.00_0.0_0_lsd.out', skiprows=2)[:, 1]
    # llp_cool_int = np.loadtxt('synths/old/lsds/spectrum_4250.0_4.16_-0.01_0.07_1.71_0.00_0.00_0.0_0_lsd.out',  skiprows=2)[:, 1]
    # llp_hot_int = np.loadtxt('synths/old/lsds/spectrum_7250.0_4.16_-0.01_0.07_1.71_0.00_0.00_0.0_0_lsd.out', skiprows=2)[:, 1]

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
    # rs_spots = [15., 15, 15., 15.]  # spot radius (degrees)
    # # rs_spots = [20., 15., 20., 15.]  # spot radius (degrees)
    # cs_cools = [0.9, 0.0, 0.8, 0.0]  # cool spot contrast between 0 and 1
    # # cs_cools = [0.8, 0.6, 0.5, 0.8]  # cool spot contrast between 0 and 1
    # cs_hots = [0.0, 0.8, 0.0, 0.8]  # hot spot contrast between 0 and 1
    #
    # spots_params = {'lats_spots': lats_spots, 'longs_spots': longs_spots, 'rs_spots': rs_spots, 'cs_cools': cs_cools,
    #                 'cs_hots': cs_hots}
    #
    # line_phases = np.arange(0, 1.0, 0.1)
    # # line_phases = np.array([1.305, 1.630, 1.637, 1.995, 2.006, 2.022])
    # # line_phases = np.linspace(0, 1.0, 770)
    # line_times = DIP.params['t0'] + DIP.params['period'] * line_phases
    # line_vels = np.arange(-32, 32 + 1.0, 1.0)
    # line_snr = 3000
    #
    # # lc_phases = np.arange(1.305, 2.022 + 0.01, 0.01)
    # lc_phases = np.arange(0.0, 1.0 + 0.01, 0.01)
    # lc_times = DIP.params['t0'] + DIP.params['period'] * lc_phases
    # lc_snr = 3000
    #
    # # # light curve
    # # opt_params = {'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0, 'delta': 1.0, 'lmbd': 8, 'maxiter': 5500,
    # #               'tol': 1e-5, 'disp': True}
    #
    # # # line profiles
    # # opt_params = {'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0, 'delta': 1.0, 'lmbd': 3, 'maxiter': 5500,
    # #               'tol': 1e-5, 'disp': True}
    #
    # opt_params = {'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0, 'delta': 1.0, 'lmbd': 1, 'maxiter': 5000,
    #               'tol': 1e-5, 'disp': True}
    #
    # modes_inp = {'line': {'times': line_times, 'vels': line_vels, 'snr': line_snr},
    #              'lc': {'times': lc_times, 'snr': lc_snr}}
    #
    #
    # plot_params = {'line_sep_prf': 0.05, 'line_sep_res': 0.005, 'mol_sep_prf': 0.03, 'mol_sep_res': 0.01,
    #                'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
    #                'ticklabelsize': 12}
    #
    # # import utils as dipu
    # #
    # # dipu.draw_3D_surf(DIP.params, DIP.surface_grid, spots_params)
    #
    # DIP.test(spots_params, modes_input=modes_inp, opt_params=opt_params, plot_params=plot_params,
    #          save_data_path='test_find_per_incl.pkl')
    #          # save_data_path='test_poor-sample_only_cool_high_amp.pkl')
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    file = open('test_find_per_incl.pkl', 'rb')
    input_data_dict = pickle.load(file)
    file.close()

    DIP.set_input_data(input_data_dict)

    """ Grid Search """
    opt_params = {'alpha': 3.4, 'beta': 1.0, 'gamma': 1.0, 'delta': 0.01, 'lmbd': 1.05, 'maxiter': 5000,
                  'tol': 1e-5, 'disp': True}

    opt_params = {'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0, 'delta': 1.0, 'lmbd': 2.0, 'maxiter': 3500,
                  'tol': 1e-5, 'disp': True}

    fit_params = {
                    # 'dOmega': np.linspace(-1.0, -0.1, 20),
                    'period': np.linspace(2.5, 3.5, 2),
                    # 'vsini': np.linspace(16, 23, 10),
                    # 'R': np.linspace(1.3, 1.8, 20),
                    # 'vrt': np.linspace(0, 10, 20),
                    # 'resolution': np.linspace(0.0, 65000, 50),
                    'incl': np.linspace(10, 90, 2),
                    # 'eqw': np.linspace(0.0858 - 0.003, 0.0858 + 0.001, 50)
                    # 'Tcool': np.linspace(3800, 6539, 30),
                    # 'Thot': np.linspace(6539, 8500, 30)

                    }

    DIP.grid_search(fit_params, opt_params, minv="loss", save='sil2.pkl')
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    recons_result = DIP.reconstructor(alpha=1.0, beta=1.0, gamma=1.0, delta=1, lmbd=1, maxiter=5500, tol=1e-5,
                                      disp=True)

    DIP.plot(plot_params={'line_sep_prf': 0.06, 'line_sep_res': 0.01, 'mol_sep_prf': 0.3, 'mol_sep_res': 0.2,
                          'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
                          'ticklabelsize': 12})

# import numpy as np
# from SpotDIPy import SpotDIPy
# import multiprocessing
# import pickle
#
#
# if __name__ == '__main__':
#     # multiprocessing.cpu_count() - 1
#     DIP = SpotDIPy(cpu_num=multiprocessing.cpu_count() - 1, platform_name='cpu')
#
#     DIP.set_param('t0', value=2454254.621769409)
#     DIP.set_param('period', value=2.9631578947)
#     DIP.set_param('Tphot', value=6539)
#     DIP.set_param('Tcool', value=4188)
#     DIP.set_param('Thot', value=7000)
#     DIP.set_param('incl', value=60)
#     DIP.set_param('vsini', value=20.138)
#     # DIP.set_param('R', value=1.668)
#     DIP.set_param('vrt', value=6.79)
#     DIP.set_param('mass', value=1.41)
#     DIP.set_param('dOmega', value=0.0)
#     DIP.set_param('resolution', value=65000)
#     DIP.set_limb_darkening_params(mh=-0.18, law='linear', model='mps2', mu_min=0.1, data_path=None)
#
#     DIP.set_conf({
#         'line': {'mode': 'on',
#                  'wave_range': [4412, 7838],
#                  'eqw': 0.0848368,
#                  'scaling': {'method': 'mean'},
#                  'corr': {'rv': None, 'amp': None}  # np.arange(10) / 10
#                  },
#         'lc': {'mode': 'on',
#                'passband': 'TESS',
#                'scaling': {'method': 'mean'},
#                'corr': {'amp': None}
#                }
#     })
#
#     # DIP.construct_surface_grid(method='phoebe2_marching', noes=4000)
#     # DIP.construct_surface_grid(method='healpy', nside=16)
#     DIP.construct_surface_grid(method='trapezoid', nlats=45)
#
#     llp_vels = np.loadtxt('teff5500_logg4.3_mh0.00_vmic1.7_lsd.out', skiprows=2)[:, 0]
#     llp_phot_int = np.loadtxt('teff5500_logg4.3_mh0.00_vmic1.7_lsd.out', skiprows=2)[:, 1]
#     llp_cool_int = np.loadtxt('teff4500_logg4.3_mh0.00_vmic1.7_lsd.out',  skiprows=2)[:, 1]
#     llp_hot_int = np.loadtxt('teff6000_logg4.3_mh0.00_vmic1.7_lsd.out', skiprows=2)[:, 1]
#
#     DIP.set_local_profiles({'line': {'lp_vels': llp_vels, 'phot_lp_data': llp_phot_int, 'cool_lp_data': llp_cool_int,
#                                 'hot_lp_data': llp_hot_int}})
#
#
#     """ Make a test """
#     lats_spots = [0., 30., 60., -30.]  # spot latitudes (degrees)
#     longs_spots = [0., 90., 180., 270.]  # spot longitudes (degrees)
#     rs_spots = [20., 15., 20., 15.]  # spot radius (degrees)
#     cs_cools = [0.8, 0.0, 0.5, 0.0]  # cool spot contrast between 0 and 1
#     cs_hots = [0.0, 1.0, 0.0, 1.0]  # hot spot contrast between 0 and 1
#
#     spots_params = {'lats_spots': lats_spots, 'longs_spots': longs_spots, 'rs_spots': rs_spots, 'cs_cools': cs_cools,
#                     'cs_hots': cs_hots}
#
#     line_phases = np.arange(0, 1.0, 0.1)
#     # line_phases = np.linspace(0, 1.0, 770)
#     line_times = DIP.params['t0'] + DIP.params['period'] * line_phases
#     line_vels = np.arange(-60, 60 + 1.75, 1.75)
#     line_snr = 3000
#
#     lc_phases = np.arange(0, 1, 0.01)
#     lc_times = DIP.params['t0'] + DIP.params['period'] * lc_phases
#     lc_snr = 3000
#
#     opt_params = {'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0, 'delta': 1.0, 'lmbd': 5, 'maxiter': 5500,
#                   'tol': 1e-7, 'disp': True}
#
#     modes_inp = {'line': {'times': line_times, 'vels': line_vels, 'snr': line_snr},
#                  'lc': {'times': lc_times, 'snr': lc_snr}}
#
#
#     plot_params = {'line_sep_prf': 0.06, 'line_sep_res': 0.01, 'mol_sep_prf': 0.03, 'mol_sep_res': 0.01,
#                    'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
#                    'ticklabelsize': 12}
#
#     # import utils as dipu
#     #
#     # dipu.draw_3D_surf(DIP.params, DIP.surface_grid, spots_params)
#
#     DIP.test(spots_params, modes_input=modes_inp, opt_params=opt_params, plot_params=plot_params)
#     """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#
#     # file = open('test_idc.pkl', 'rb')
#     # input_data_dict = pickle.load(file)
#     # file.close()
#     #
#     # DIP.set_input_data(input_data_dict)
#     #
#     # recons_result = DIP.reconstructor(alpha=1.0, beta=1.0, gamma=1.0, delta=1.0, lmbd=5.0, maxiter=2500, tol=1e-7,
#     #                             disp=True)
#     #
#     # DIP.plot(plot_params={'line_sep_prf': 0.06, 'line_sep_res': 0.01, 'mol_sep_prf': 0.3, 'mol_sep_res': 0.2,
#     #                       'show_err_bars': True, 'fmt': '%0.3f', 'markersize': 2, 'linewidth': 1, 'fontsize': 15,
#     #                       'ticklabelsize': 12})
#
