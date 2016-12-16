'''
updated by Dan on 12/15
'''

import matplotlib.pyplot as plt
import seaborn

def IMshow_pupil(pupil, axnum = True):
    '''
    display a pupil function in 2D
    '''
    NY, NX = pupil.shape
    ry = int(NY/2.)
    rx = int(NX/2.)
    yy = (np.arange(NY)-ry)/ry
    xx = (np.arange(NX)-rx)/rx
    [MX, MY] = np.meshgrid(xx,yy)
    fig_2D = plt.figure(figsize=(7.5,5.8))
    ax = fig_2D.add_subplot(111)
    ax.set_ylim([-N_radius, N_radius])
    ax.set_xlim([-N_radius, N_radius])
    if (axnum == False):
        ax.get_yaxis.set_visible(False)
        ax.get_xaxis.set_visible(False)
    fig_2D.axes.get_yaxis().set_visible(False)
    pcm = ax.pcolor(MX, MY, pupil, cmap = 'RdYlBu_r')
    fig_2D.colorbar(pcm, ax = ax, extend='max')

    # plot cross section
    fig_1D = plt.figure(figsize = (7.5, 4.0))
    ax = fig_1D.add_subplot(111)
    ax.plot(pupil[:,N_radius], linewidth = 2, '--r')
    ax.plot(pupil[N_radius, :], linewidth = 2, '-g')

    return fig_2D, fig_1D  # return the fig_2Dure handle
