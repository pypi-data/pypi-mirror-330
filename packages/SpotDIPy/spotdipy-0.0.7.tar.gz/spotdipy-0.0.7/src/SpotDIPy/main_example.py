# import sys
# sys.path.insert(1, '/home/eng/Dropbox/PythonProjects/SpotDIPy_GitHub/src/SpotDIPy')
from SpotDIPy import SpotDIPy
from glob import glob
import numpy as np
import multiprocessing


if __name__ == '__main__':
    DIP = SpotDIPy(cpu_num=multiprocessing.cpu_count() - 1, platform_name='cpu')

    DIP.set_param('t0', value=2449950.55)
    DIP.set_param('period', value=1.353378)
    DIP.set_param('Tphot', value=5750)
    DIP.set_param('Tcool', value=5000)
    DIP.set_param('Thot', value=5750)
    DIP.set_param('incl', value=60)
    DIP.set_param('vsini', value=38.1)
    # DIP.set_param('R', value=1.668)
    DIP.set_param('vrt', value=3.0)
    DIP.set_param('mass', value=1.017)
    DIP.set_param('dOmega', value=0.0)
    DIP.set_param('resolution', value=30000)

    DIP.set_limb_darkening_params(mh=0.0, law='linear', model='mps2', mu_min=0.1, data_path=None)

    DIP.set_conf({
            'line': {'mode': 'on',
                     'wave_range': [4550, 7000],
                     'eqw': 0.0848368,
                     'scaling': {'method': 'mean'},
                     'corr': {'rv': 0.0, 'amp': None}
                     },
            'lc': {'mode': 'off',
                   'passband': 'TESS',
                   'scaling': {'method': 'mean'},
                   'corr': {'amp': None}
                   }
        })

    DIP.construct_surface_grid(method='healpy', nside=16)

    llp_phot = np.loadtxt('synth_LSDs/T5750.0_logg4.3_M-0.04_mic1.8_others0_lsd.out', skiprows=2)
    llp_cool = np.loadtxt('synth_LSDs/T5000.0_logg4.3_M-0.04_mic1.8_others0_lsd.out', skiprows=2)
    llp_hot = np.loadtxt('synth_LSDs/T5750.0_logg4.3_M-0.04_mic1.8_others0_lsd.out', skiprows=2)

    DIP.set_local_profiles({'line': {'lp_vels': llp_phot[:, 0], 'phot_lp_data': llp_phot[:, 1],
                                     'cool_lp_data': llp_cool[:, 1], 'hot_lp_data': llp_hot[:, 1]}})

    obsPaths = glob('target_LSDs/*_lsd.out')
    obsData = []
    obsMidTimes = np.arange(0)
    for obsPath in obsPaths:
        midTime = float(obsPath.split('/')[-1].split('_')[3].split('=')[1])
        obsMidTimes = np.hstack((obsMidTimes, midTime))
        data = np.loadtxt(obsPath, skiprows=2)
        obsData.append(data)
    obsData = np.array(obsData)



    DIP.set_input_data(data=obsData, midTimes=obsMidTimes)
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#
# """ Import initial local line profiles (LLP) (for photosphere and spot) data"""
# Standards
LLPvels = np.loadtxt('/home/eng/Dropbox/PycharmProjects/V889Her/lsds/standards/Combined-Spectrum_OBJ=HD143761_DATE-MID=2020-09-04T20&35&16_BJDTDB-MID=2459097.3571044_BRVCOR-MID=-16.45757_rvcorrected_lsd.out',
                     skiprows=2)[:, 0]
LLPphotInt = np.loadtxt('/home/eng/Dropbox/PycharmProjects/V889Her/lsds/standards/Combined-Spectrum_OBJ=HD143761_DATE-MID=2020-09-04T20&35&16_BJDTDB-MID=2459097.3571044_BRVCOR-MID=-16.45757_rvcorrected_lsd.out',
                        skiprows=2)[:, 1]
LLPspotInt = np.loadtxt('/home/eng/Dropbox/PycharmProjects/V889Her/lsds/standards/Combined-Spectrum_OBJ=HD22049_DATE-MID=2020-09-04T22&11&02_BJDTDB-MID=2459097.4272621_BRVCOR-MID=23.96179_rvcorrected_lsd.out',
                        skiprows=2)[:, 1]

SDI.set_bm_LLPs(LLPvels=LLPvels, LLPs={'phot': LLPphotInt, 'spot': LLPspotInt})
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Grid search """
# fitparams = {
#              'vsini': np.linspace(36, 40, 20),
#              # 'rv_corr': np.linspace(-1.5, 1.5, 20),
#              'eqw': np.arange(0.0897, 0.0915, 0.0002),
#              # 'vrt': np.linspace(0.0, 6.0, 20),
#              }
# fss = SDI.grid_search(fitparams, lmbd=[15], maxiter=1000, ind_vel_cor=1, output_path='grid_search_V889Her_set-1_dotsgrid.txt')
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" Reconstruct surface map """
# lmbds = np.arange(1, 100, 1)
# lmbds = np.arange(1, 7.5, 0.5)**2
lmbds = [10]  # dg --> 10, dg --> 13
result, fchi, _, _, _, _ = SDI.reconstructor(regtype='mem', lmbds=lmbds, maxiter=550, iprint=True,
                                             ind_vel_cor=1, disp=True, phaInfo=True)

print('Total fs= ', SDI.get_total_fs())

# fs = SDI.get_fs(result.x, SDI.phases)
# np.savetxt('bjd_vs_fs_v889her_set-1.txt', np.vstack((SDI.midTimes, fs)).T)

# plt.figure()
# plt.plot(SDI.phases, fs, 'bo')
# plt.show()

SDI.plot()
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# """ Article figures """
#
# SOLP = SDI.generateSyntProf(SDI.fss, SDI.rvcsx)
# # print(SOLP)
# SOLP['obsData'] = SDI.obsData.copy()
# ILP = SDI.generateSyntProf(fss=np.ones(len(SDI.fss)), rvcs=SDI.rvcsx)
# SOLP['ILP'] = ILP['prfs'].copy()
#
# fig = plt.figure(figsize=(10, 10))
# ax1 = plt.subplot2grid((1, 2), (0, 0))
# ax2 = plt.subplot2grid((1, 2), (0, 1))
#
# shfProf = 0.05
# shfRes = 0.015
# sinds = np.argsort(SOLP['phases'])
# for i, sind in enumerate(sinds):
#
#     maxv = max(SOLP['vels'])
#     maxi = max(SOLP['obsData'][sind][:, 1]) + i * shfProf
#     residual = SOLP['obsData'][sind][:, 1] - SOLP['prfs'][:, sind]
#     maxir = max(residual + i * shfRes)
#
#     ax1.errorbar(SOLP['vels'], SOLP['obsData'][sind][:, 1] + i * shfProf,
#                                        yerr=SOLP['obsData'][sind][:, 2], fmt='o', color='k', ms=2)
#     ax2.errorbar(SOLP['vels'], residual + i * shfRes,
#                                        yerr=SOLP['obsData'][sind][:, 2], fmt='o', color='k', ms=2)
#
#     ax1.plot(SOLP['vels'], SOLP['ILP'][:, sind] + i * shfProf, 'b', zorder=2)
#     ax1.plot(SOLP['vels'], SOLP['prfs'][:, sind] + i * shfProf, 'r', zorder=3)
#     ax1.annotate(str('%0.3f' % round(SOLP['phases'][sind], 3)),
#                                        xy=(maxv - maxv / 3.2, maxi + shfProf / 10.),
#                                        color='g', fontsize=15)
#     ax2.annotate(str('%0.3f' % round(SOLP['phases'][sind], 3)), xy=(maxv - maxv / 3.2, maxir + shfRes / 10.),
#                                        color='g', fontsize=15)
#     ax2.axhline(i * shfRes, color='r', zorder=3)
#
# # ax1.set_xlabel('Velocity (km/s)', fontsize=20)
# # ax1.set_ylabel('I/Ic', fontsize=20)
# # ax2.set_xlabel('Velocity (km/s)', fontsize=20)
# # ax2.set_ylabel('Residuals', fontsize=20)
#
# ax1.set_xlabel('Dikine Hız (km/s)', fontsize=20)
# ax1.set_ylabel('I/Ic', fontsize=20)
# ax2.set_xlabel('Dikine Hız (km/s)', fontsize=20)
# ax2.set_ylabel('Artıklar', fontsize=20)
#
# ax1.tick_params(labelsize=20)
# ax2.tick_params(labelsize=20)
#
# # shf = 0.01
# # for i, phase in enumerate(SOLP['phases']):
# #     plt.plot(SOLP['vels'], obsData[i] + shf * i, 'ko')
# #     plt.plot(SOLP['vels'], SOLP['prfs'][:, i] + shf * i, 'r')
# #     ran = abs(max(SOLP['vels']) - min(SOLP['vels']))
# #     plt.text(max(SOLP['vels']) - ran * 0.1, max(SOLP['prfs'][:, i]) + shf * i,
# #              SOLP['phases'][i], color='gray')
#
# plt.tight_layout()
#
# plt.savefig('/home/eng/Dropbox/Tez/figures/tez_profs_set1_v889her_bm.png', dpi=600, format='png')
# # plt.savefig('profs_dec2015.png', dpi=600, format='png')
# # plt.savefig('profs_dec2015.eps', dpi=600, format='eps')
#
# # plt.show()
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# fig = plt.figure(figsize=(13, 9))
# ax = fig.add_subplot(111, projection='mollweide')
#
# rmap = SDI.fss[SDI.iptr].reshape(SDI.nlats, SDI.nlonrct)
#
# xlats = (SDI.blats[1:] + SDI.blats[:-1]) / 2.
# bxlongs = SDI.blongs[np.argmax(SDI.nlons)]
# xlongs = (bxlongs[1:] + bxlongs[:-1]) / 2.
#
# fmap = 1.0 - rmap.copy()
# cmap = 'gray_r'
# # cmap = 'gist_heat_r'
#
# obslong = 360 * (1.0 - SDI.phases) - 180
#
# pc = ax.pcolormesh(xlongs - np.pi, xlats, fmap, cmap=cmap)
# # ax.plot(np.deg2rad([obslong, obslong]), np.deg2rad([-30, -15]), 'k')
# ax.set_xticks(np.deg2rad(np.arange(-120, 180, 60)))
# ax.set_yticks(np.deg2rad(np.arange(-90, 120, 30)))
# tick_labels = np.arange(60, 360, 60)
# ax.set_xticklabels(tick_labels, zorder=15)
# ax.grid(True)
# # ax.set_xlabel('Longitude ($\degree$)', fontsize=20)
# # ax.set_ylabel('Latitude ($\degree$)', fontsize=20)
# ax.set_xlabel('Boylam ($\degree$)', fontsize=20)
# ax.set_ylabel('Enlem ($\degree$)', fontsize=20)
# ax.tick_params(labelsize=20)
# ax.xaxis.set_label_coords(0.5, -0.100)
#
# clb = fig.colorbar(pc, ax=ax, location='bottom', shrink=0.7, )
# clb.set_label('fs', fontsize=20)
# clb.ax.tick_params(labelsize=20)
#
# for obl in obslong:
#     ax.text(obl/60, -0.3, '|', color='b', fontsize=15)
#
# plt.tight_layout()
#
# # ff = open('spdi_1d_set-1.txt', 'w')
# # ff.write(str(len(xlats)) + ' ' + str(len(xlongs)) + ' ' + str(len(SDI.fss)) + '\n')
# # data = np.hstack((xlats, xlongs, SDI.fss))
# # for item in data:
# #     ff.write(str(item) + '\n')
# # ff.close()
#
# np.savetxt('spdi_map_v889her_set-1.txt', fmap)
# np.savetxt('spdi_coord_v889her_set-1.txt', np.hstack(([len(xlats), len(xlongs)], xlats, xlongs)))
#
#
# plt.savefig('/home/eng/Dropbox/Tez/figures/tez_map_set1_v889her_bm.png', dpi=600, format='png')
# # plt.savefig('map_dec2015.png', dpi=600, format='png')
# # plt.savefig('map_dec2015.eps', dpi=600, format='eps')
# plt.show()
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""