from plot_attributes import *
from scipy.interpolate import griddata
from scipy.signal import spectrogram
from map_probes import \
    sp_name_dict, imp_name_dict, \
    imp_rads, imp_phis8

## Plots the power spectrum for the DMD
# @param y0 The y0s determined from any DMD algorithm
# @param omega The complex DMD frequencies
# @param inj_freq Injector frequency
# @param filename Name of the file corresponding to the shot
# @param typename type string indicating which algorithm is being used
def power_spectrum(y0,omega,inj_freq,filename,typename):
    plt.figure(1000,figsize=(figx, figy+12))
    plt.subplot(4,1,4)
    oscillation = np.imag(omega)/(pi*2)
    decay = abs(np.real(omega)/(pi*2))
    sort1 = np.argsort(oscillation)
    power1 = (y0[sort1]*np.conj(y0[sort1])).astype('float')
    power1 = power1/np.max(power1)
    if typename=='DMD':
        plt.semilogy(np.sort(oscillation)/1000.0, \
            power1, \
            color='b',linewidth=lw, \
            label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename=='sparse DMD':
        plt.semilogy(np.sort(oscillation)/1000.0, \
            power1, \
            color='r',linewidth=lw, \
            label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename=='optimized DMD':
        plt.semilogy(np.sort(oscillation)/1000.0, \
            power1, \
            color='g',linewidth=lw, \
            label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename[9]=='=':
        plt.semilogy(np.sort(oscillation)/1000.0, \
            power1, \
            color=np.ravel(np.random.rand(1,3)),linewidth=lw, \
            label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    plt.legend(loc='upper left',fontsize=ls-8,ncol=3)
    plt.ylabel(r'$|b_k|^2/|b_{max}|^2$',fontsize=fs)
    plt.xlabel('f (kHz)',fontsize=fs)
    plt.xlim(-3*inj_freq,3*inj_freq)
    h=plt.ylabel(r'$|b_k|^2/|b_{max}|^2$',fontsize=fs)
    plt.xlabel(r'f (kHz)',fontsize=fs+4)
    #plt.xlim(-120,120)
    plt.xlim(-3*inj_freq,3*inj_freq)
    plt.grid(True)
    ax = plt.gca()
#    ax.set_xticks([-3*inj_freq,-2*inj_freq,-inj_freq, \
#        0,inj_freq,2*inj_freq,3*inj_freq])
#    ax.set_xticklabels([r'$-f_3$',r'$-f_2$',r'$-f_1$', \
#        '0',r'$f_1$',r'$f_2$',r'$f_3$'])
 
    #ax.set_xticks([-120,-5*inj_freq,-3*inj_freq,-inj_freq, \
    #    inj_freq,3*inj_freq,5*inj_freq,120])
    #ax.set_xticklabels([-120,r'$-f_5$',r'$-f_3$',r'$-f_1$', \
    #    r'$f_1$',r'$f_3$',r'$f_5$',120])
    plt.ylim((1e-21,1e0))
    #ax.set_yticks([1e-12,1e-10,1e-8,1e-6,1e-4,1e-2,1e0])
    #ax.set_yticklabels([1e-10,1e-8,1e-6,1e-4,1e-2,1e0])
    ax.set_xticks([-3*inj_freq,-2*inj_freq,-inj_freq,0, \
        inj_freq,2*inj_freq,3*inj_freq])
    ax.set_xticklabels([r'$-f_3$',r'$-f_2$',r'$-f_1$',0, \
        r'$f_1$',r'$f_2$',r'$f_3$'])
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    plt.grid(True)
    plt.yticks([1e-21,1e-14,1e-7,1e0])
    plt.savefig(out_dir+filename)

## Plots real part vs imag part of the oscillation frequencies
# @param y0 The y0s determined from any DMD algorithm
# @param omega The complex DMD frequencies
# @param inj_freq Injector frequency
# @param filename Name of the file corresponding to the shot
# @param typename type string indicating which algorithm is being used
def freq_phase_plot(y0,omega,inj_freq,filename,typename):
    amp = abs(y0)/np.max(abs(y0))*2500 #/np.max(abs(y0))
    camp = np.log(abs(y0)/np.max(abs(y0))) #/np.max(abs(y0))
    for j in range(len(amp)):
        amp[j] = max(amp[j],400.0)
    sort = np.argsort(amp)
    amp = amp[sort]
    real_f = np.real(omega[sort])/1000.0/(2*pi)
    imag_f = np.imag(omega[sort])/1000.0/(2*pi)
    plt.figure(1000,figsize=(figx, figy+12))
    #plt.subplot(2,1,1)
    if typename=='DMD':
        plt.subplot(4,1,1)
        for snum in range(len(real_f)):
            plt.scatter(imag_f[snum],real_f[snum],c='b',s=amp[snum], \
                linewidths=3,edgecolors='k', \
                label=typename,alpha=transparency)
    elif typename=='sparse DMD':
        plt.subplot(4,1,3)
        for snum in range(len(real_f)):
            plt.scatter(imag_f[snum],real_f[snum],c='r',s=amp[snum], \
                linewidths=3,edgecolors='k', \
                label=typename,alpha=transparency) 
        #plt.scatter(imag_f,real_f,c=amp,s=amp,cmap=plt.cm.get_cmap('Reds'), \
        #    linewidths=2,edgecolors='k', \
        #    label=typename,alpha=transparency)
        #plt.xlabel(r'f (kHz)',fontsize=fs)
    elif typename=='optimized DMD':
        plt.subplot(4,1,2)
        for snum in range(len(real_f)):
            plt.scatter(imag_f[snum],real_f[snum],c='g',s=amp[snum], \
                linewidths=3,edgecolors='k', \
                label=typename,alpha=transparency)
        #plt.scatter(imag_f,real_f,c=amp,s=300.0,cmap=plt.cm.get_cmap('Greens'), \
        #    linewidths=2,edgecolors='k', \
        #    label=typename,alpha=transparency)
    plt.ylim(-1e3,1e1)
    plt.yscale('symlog',linthreshy=1e-2)
    ax = plt.gca()
    ax.set_yticks([-1e3,-1,-1e-2,1e-2,1e1])
    plt.axhline(y=0,color='k',linewidth=3,linestyle='--')
    #ax.set_yticklabels([r'$-10^2$','',r'$-10^1$','',r'$-10^{-1}$','',0,'',r'$10^{-1}$','',r'$10^1$'])
    #plt.xscale('symlog')
    plt.ylabel(r'$\delta_k$ (kHz)',fontsize=fs+4)
    #plt.title(typename,fontsize=fs)
    plt.xlim(-120,120)
    #plt.xlim(-inj_freq*3,inj_freq*3)
    plt.grid(True)
    ax.set_xticks([-120,-5*inj_freq,-3*inj_freq,-inj_freq, \
        inj_freq,3*inj_freq,5*inj_freq,120])
    #ax.set_xticks([-3*inj_freq,-2*inj_freq,-inj_freq, \
    #    0,inj_freq,2*inj_freq,3*inj_freq])
    ax.set_xticklabels([])
    #ax.set_xticklabels(['-100',r'$-f_5$',r'$-f_3$',r'$-f_1$', \
    #    '0',r'$f_1$',r'$f_3$',r'$f_5$','100'])
    #ax.set_xticklabels([r'$-f_3$',r'$-f_2$',r'$-f_1$', \
    #    '0',r'$f_1$',r'$f_2$',r'$f_3$'])
    #ax.tick_params(axis='x', which='major', labelsize=ts)
    #ax.tick_params(axis='x', which='minor', labelsize=ts)
    ax.tick_params(axis='y', which='major', labelsize=ts)
    ax.tick_params(axis='y', which='minor', labelsize=ts)
    plt.savefig(out_dir+filename)

## Creates a sliding window animation
# @param dict A psi-tet dictionary
# @param inj_freq Injector frequency of the dictionary
# @param numwindows Number of sliding windows
# @param dmd Flag to indicate what type of dmd algorithm is being used
def dmd_animation(dict,inj_freq,numwindows,dmd):
    typename = 'sparse DMD'
    t0 = dict['t0']
    tf = dict['tf']
    data = dict['SVD_data']
    time = dict['sp_time'][t0:tf]
    dt = dict['sp_time'][1] - dict['sp_time'][0]
    r = np.shape(data)[0]
    tsize = np.shape(data)[1]
    windowsize = int((tsize-1)/float(numwindows))
    if tsize > windowsize:
        starts = np.linspace(0, \
            tsize-windowsize-1,numwindows, dtype='int')
        ends = starts + np.ones(numwindows,dtype='int')*windowsize
    else:
        print('windowsize > tsize, dmd invalid')
    if numwindows > 1:
        for flag in dmd:
            if flag == 1:
                moviename = out_dir+'dmd_movie.gif'
            elif flag == 2:
                moviename = out_dir+'sdmd_movie.gif'
            elif flag == 3:
                moviename = out_dir+'odmd_movie.gif'
            fig = plt.figure(200+flag,figsize=(figx, figy))
            ani = animation.FuncAnimation( \
                fig, dmd_update, range(numwindows), \
                fargs=(dict,inj_freq,windowsize, \
                    numwindows,starts,ends,typename,flag),
                    repeat=False, \
                    interval=100, blit=False)
            ani.save(moviename,fps=5)
    else:
        print('Using a single window,'+ \
            ' aborting dmd sliding window animation')

## Update function for making the sliding window spectrogram movies
# @param i The ith frame
# @param dict A psi-tet dictionary
# @param inj_freq The injector frequency
# @param windowsize The size of the sliding window
# @param numwindows The number of windows that are used
# @param starts The start points of each of the windows 
# @param ends The end points of each of the windows 
# @param flag Which DMD method to use
def dmd_update(i,dict,inj_freq,windowsize,numwindows,starts,ends,flag):
    if flag == 1:
        dmd_b = dict['dmd_b']
        b_inj = dict['dmd_b_inj']
        b_eq = dict['dmd_b_eq']
        y0 = np.asarray(dict['dmd_y0'])[i,:]
        omega = np.asarray(dict['dmd_omega'])[i,:]
    if flag == 2:
        dmd_b = dict['sdmd_b']
        b_inj = dict['sdmd_b_inj']
        b_eq = dict['sdmd_b_eq']
        y0 = np.asarray(dict['sdmd_y0'])[i,:]
        omega = np.asarray(dict['sdmd_omega'])[i,:]
    if flag == 3:
        dmd_b = dict['odmd_b']
        b_inj = dict['odmd_b_inj']
        b_eq = dict['odmd_b_eq']
        y0 = np.asarray(dict['odmd_y0'])[i,:]
        omega = np.asarray(dict['odmd_omega'])[i,:]
    t0 = dict['t0']
    tf = dict['tf']
    data = dict['SVD_data']
    time = dict['sp_time'][t0:tf]
    dt = dict['sp_time'][1] - dict['sp_time'][0]
    r = np.shape(data)[0]
    fig=plt.figure(200+flag,figsize=(figx, figy))
    plt.subplot(2,2,1)
    ax1 = plt.gca()
    ax1.clear()
    plt.grid(True)
    index = np.shape(dict['sp_Bpol'])[0]
    inj_index = 2
    if dict['is_HITSI3']:
        inj_index = 3
    plt.plot(time*1000, \
        #dict['tcurr'][:len(dict['tcurr'])-1]/1000.0,'k',label='Itor')
        dict['SVD_data'][index+inj_index,:]*1e4,'k',
        label='B_L01T000',linewidth=lw)

    plt.plot(time[starts[i]:ends[i]]*1000,dmd_b[index+inj_index,starts[i]:ends[i]]*1e4,'r',\
        label='sparse DMD',linewidth=lw)
        #dict['tcurr'][t0:tf]/1000.0,'r')
    plt.axvline(dict['sp_time'][t0+starts[i]]*1000,color='k')
    plt.axvline(dict['sp_time'][t0+ends[i]]*1000,color='k')
    plt.xlabel('Time (ms)',fontsize=fs)
    plt.ylabel('B (G)',fontsize=fs)
    ax1.tick_params(axis='both', which='major', labelsize=ts)
    ax1.tick_params(axis='both', which='minor', labelsize=ts)
    plt.xlim(time[0]*1000,time[len(time)-1]*1000)
    #plt.ylim(-500,1000)
    plt.ylim(-150,300)
    ax1.set_yticks([-150,0,150,300])
    #ax1.set_yticks([-500,0,500,1000])
    ax1.set_xticks([0,1,2])
    ax1.set_xticklabels([0,1,2])
    plt.legend(fontsize=ls-10,loc='upper left')
    real_f = np.real(omega)/1000.0/(2*pi)
    imag_f = np.imag(omega)/1000.0/(2*pi)

    plt.subplot(2,2,2)
    ax2 = plt.gca()
    ax2.clear()
    sort = np.argsort(imag_f)
    power = y0[sort]*np.conj(y0[sort])
    plt.plot(np.sort(imag_f), \
        power/np.max(power), \
        'r',label=r'$|b_k|^2/|b_{max}|^2$',linewidth=lw, \
         path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
         pe.Normal()])

    plt.yscale('log')
    plt.legend(fontsize=ls-8,loc='lower right')
    #plt.xlim(-100,100)
    plt.xlim(-3*inj_freq,3*inj_freq)
    plt.grid(True)
    ax2.set_xticks([-3*inj_freq,-2*inj_freq,-inj_freq, \
        0,inj_freq,2*inj_freq,3*inj_freq])
    ax2.set_xticklabels([r'$-f_3$','',r'$-f_1$', \
        '',r'$f_1$','',r'$f_3$'])
    #ax2.set_xticks([-5*inj_freq,-3*inj_freq,-inj_freq, \
    #    0,inj_freq,3*inj_freq,5*inj_freq])
    #ax2.set_xticklabels([r'$-f_5$','',r'$-f_1$', \
    #    '',r'$f_1$','',r'$f_5$'])
 
    plt.ylim((1e-20,1e0))
    ax2.set_yticks([1e-20,1e-15,1e-10,1e-5,1e0])
    plt.xlabel(r'f (kHz)',fontsize=fs)
    ax2.tick_params(axis='both', which='major', labelsize=ts)
    ax2.tick_params(axis='both', which='minor', labelsize=ts)

    plt.subplot(2,2,3)
    plt.grid(True)
    ax3 = plt.gca()
    num_signals = np.shape(b_inj[:,starts[i]:ends[i]])[0]
    nseg = int((tf-t0)/numwindows)
    spectros=np.zeros((66,numwindows))
    #spectros=np.zeros((113,numwindows))
    sample_freq = 1.0/dict['dt']
    for j in range(num_signals):
        freq, stime, spec = spectrogram( \
            np.real(dmd_b[j,:numwindows*nseg]), \
            sample_freq, \
            nperseg=nseg, \
            scaling='spectrum', \
            noverlap=0)
        spectros += spec
        print('j=: ',j,', shape=, ',np.shape(b_inj[j,:numwindows*nseg]))
    print((time[0]+stime)*1000,time[0],stime,sample_freq,nseg,tf,t0,numwindows)
    ptime = np.hstack(([0.0],(stime+stime[0])*1000.0))
    pcm = plt.pcolormesh(ptime, freq/1e3, spectros, \
        norm=colors.LogNorm(vmin=1e-10, \
        vmax=1e0),cmap=colormap)
    for starti in range(len(starts)):
        plt.axvline(dict['sp_time'][t0+starts[starti]]*1000,color='k')
    #plt.axvline(dict['sp_time'][t0+ends[i]]*1000,color='k')
    #plt.axvline(dict['sp_time'][t0+starts]*1000,color='k')
 
    ax3 = plt.gca()
    ax3.set_xticks([0,1,2])
    ax3.set_xticklabels([0,1,2])
    ax3.set_yticks([0,inj_freq,2*inj_freq,3*inj_freq])
    #ax3.set_yticks([0,inj_freq,3*inj_freq,5*inj_freq,100])
    ax3.set_yticklabels([0,r'$f_1$',r'$f_2$',r'$f_3$'])
    #ax3.set_yticklabels([0,r'$f_1$',r'$f_3$',r'$f_5$',100])
    try:
        cb=ax3.collections[-2].colorbar
        cb.remove()
    except:
        print("nothing to remove")
    #cb = plt.colorbar(pcm,ticks=[1e-8,1e-6,1e-4,1e-2])
    #cb = plt.colorbar(pcm,ticks=[1e-8,1e-6,1e-4,1e-2,1e0])
    #cb.ax.tick_params(labelsize=ts)
    #plt.ylim(0,100)
    plt.ylim(0,3*inj_freq)
    plt.title('All modes',fontsize=fs-14)
    plt.xlabel('Time (ms)',fontsize=fs)
    h=plt.ylabel(r'f (kHz)',fontsize=fs)
    ax3.tick_params(axis='both', which='major', labelsize=ts)
    ax3.tick_params(axis='both', which='minor', labelsize=ts)

    plt.subplot(2,2,4)
    plt.grid(True)
    ax4 = plt.gca()
    ax4.set_xticks([0,1,2])
    ax4.set_xticklabels([0,1,2])
 
    ax4.set_yticks([0,inj_freq,2*inj_freq,3*inj_freq])
    #ax4.set_yticks([0,inj_freq,3*inj_freq,5*inj_freq,100])
    ax4.set_yticklabels([0,r'$f_1$',r'$f_2$',r'$f_3$']) 
    #ax4.set_yticklabels([0,r'$f_1$',r'$f_3$',r'$f_5$',100]) 
    nseg = int((tf-t0)/numwindows)
    spectros=np.zeros((66,numwindows+1))
    #spectros=np.zeros((113,numwindows+1))
    sample_freq = 1/dict['dt']
    for j in range(num_signals):
        freq, stime, spec = spectrogram( \
            np.real(b_inj[j,:numwindows*nseg]), \
            sample_freq, \
            nperseg=nseg, \
            scaling='spectrum')
        print(j,np.shape(b_inj[j,:numwindows*nseg]))
        spectros += spec
    print((time[0]+stime)*1000,time[0],stime,sample_freq,nseg,tf,t0,numwindows)
    pcm = plt.pcolormesh(ptime, freq/1e3, spectros, \
        norm=colors.LogNorm(vmin=1e-10, \
        vmax=1e0),cmap=colormap)
    for starti in range(len(starts)):
        plt.axvline(dict['sp_time'][t0+starts[starti]]*1000,color='k')
    #plt.axvline(dict['sp_time'][t0+ends[i]]*1000,color='k')
    plt.title('Only $f_1$ mode',fontsize=fs-14)
    try:
        cb=ax4.collections[-2].colorbar
        cb.remove()
    except:
        print("nothing to remove")
    #cb = plt.colorbar(pcm,ticks=[1e-8,1e-6,1e-4,1e-2])
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7]) 
    cb = plt.colorbar(pcm,ticks=[1e-10,1e-8,1e-6,1e-4,1e-2,1e0])#,cax=cbar_ax)
    cb.ax.tick_params(labelsize=ts)
    plt.xlabel('Time (ms)',fontsize=fs)
    #plt.ylim(0,100)
    plt.ylim(0,3*inj_freq)
    ax4.tick_params(axis='both', which='major', labelsize=ts)
    ax4.tick_params(axis='both', which='minor', labelsize=ts)
    plt.savefig(out_dir+'spectrogram_'+str(i)+'.png')

## Tests the DMD methods on forecasting by 
## dividing into test/train data and using
## the full DMD reconstructions
# @param dict A psi-tet dictionary
# @param inj_freq Injector frequency
def DMD_forecast(dict,inj_freq):
    dictname = dict['filename']
    t0 = dict['t0']
    tf = dict['tf']
    data = dict['SVD_data']
    time = dict['sp_time'][t0:tf]
    dt = dict['sp_time'][1] - dict['sp_time'][0]
    inj_curr_end = 2
    if dict['is_HITSI3'] == True:
        inj_curr_end = 3
    plt.figure(30000,figsize=(figx, figy))
    plt.grid(True)
    size_bpol = np.shape(dict['sp_Bpol'])[0]
    index = size_bpol 
    time = dict['sp_time'][t0:tf]*1000
    for i in range(1,4):
        plt.subplot(3,1,i)
        plt.plot(time, \
            dict['SVD_data'][index+inj_curr_end,:]*1e4,'k',
            linewidth=lw)
    r = np.shape(data)[0]
    tsize = np.shape(data)[1]
    trainsize = int(tsize*3.0/5.0)
    testsize = tsize-trainsize
    trunc = min(r,trainsize)
    dmd_data = np.zeros((r,tsize),dtype='complex')
    sdmd_data = np.zeros((r,tsize),dtype='complex')
    odmd_data = np.zeros((r,tsize),dtype='complex')
    dmd_data[:,0:trainsize] = data[:,0:trainsize]
    sdmd_data[:,0:trainsize] = data[:,0:trainsize]
    odmd_data[:,0:trainsize] = data[:,0:trainsize]
    dmd_y0 = dict['dmd_y0']
    dmd_omega = np.ravel(dict['dmd_omega'])
    dmd_phi = dict['dmd_phi']
    sdmd_y0 = dict['sdmd_y0']
    sdmd_omega = np.ravel(dict['sdmd_omega'])
    sdmd_phi = dict['sdmd_phi']
    odmd_y0 = dict['odmd_y0']
    odmd_omega = np.ravel(dict['odmd_omega'])
    odmd_phi = dict['odmd_phi']
    for i in range(testsize-1):
        dmd_data[:,trainsize+i+1] = 0.5*np.dot( \
            dmd_y0*np.exp(dmd_omega*(time[i]-time[0])/1000.0), \
            np.transpose(dmd_phi))
        sdmd_data[:,trainsize+i+1] = 0.5*np.dot( \
            sdmd_y0*np.exp(sdmd_omega*(time[i]-time[0])/1000.0), \
            np.transpose(sdmd_phi))
        odmd_data[:,trainsize+i+1] = 0.5*np.dot( \
            odmd_y0*np.exp(odmd_omega*time[i]/1000.0),np.transpose(odmd_phi))
    dmd_data[:,trainsize+1:] += np.conj(dmd_data[:,trainsize+1:])
    sdmd_data[:,trainsize+1:] += np.conj(sdmd_data[:,trainsize+1:])
    odmd_data[:,trainsize+1:] += np.conj(odmd_data[:,trainsize+1:])
    err1 = np.linalg.norm(data[:,trainsize+1:] \
        -dmd_data[:,trainsize+1:],'fro') \
        /np.linalg.norm(data[:,trainsize+1:],'fro')
    err2 = np.linalg.norm(data[:,trainsize+1:] \
        -sdmd_data[:,trainsize+1:],'fro') \
        /np.linalg.norm(data[:,trainsize+1:],'fro')
    err3 = np.linalg.norm(data[:,trainsize+1:] \
        -odmd_data[:,trainsize+1:],'fro') \
        /np.linalg.norm(data[:,trainsize+1:],'fro')
    print('dmderr,sdmd_err,odmderr=',err1,' ',err2,' ',err3)
    plt.subplot(3,1,1)
    plt.plot(time, \
        dmd_data[index+inj_curr_end,:]*1e4,'b',label='DMD Forecast', \
        linewidth=lw, \
        path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
        pe.Normal()])

    plt.subplot(3,1,3)
    plt.plot(time, \
        sdmd_data[index+inj_curr_end,:]*1e4,'r',label='sparse DMD Forecast', \
        linewidth=lw, \
        path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
        pe.Normal()])
    plt.subplot(3,1,2)
    plt.plot(time, \
        odmd_data[index+inj_curr_end,:]*1e4,'g',label='optimized DMD Forecast', \
        linewidth=lw, \
        path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
        pe.Normal()])
    for i in range(1,4):
        plt.subplot(3,1,i)
        if i==1:
            plt.title(dict['filename'][7:13]+', Probe: B_L01T000', \
                fontsize=fs)
        if i==3:
            plt.xlabel('Time (ms)',fontsize=fs)
        plt.ylabel('B (G)',fontsize=fs)
        plt.axvline(x=time[trainsize],color='k', \
            linewidth=lw)
        plt.legend(loc='upper left',fontsize=ls)
        ax = plt.gca()
        ax.tick_params(axis='both', which='major', labelsize=ts)
        ax.tick_params(axis='both', which='minor', labelsize=ts)
        plt.ylim(-150,300)
        #plt.ylim(-500,1000)
        #ax.set_yticks([-500,0,500,1000])
        ax.set_yticks([-150,0,150,300])
    plt.savefig(out_dir+'sdmd_forecasting.png')

## Shows reconstructions using the DMD methods
## of a particular SP and a particular IMP probe
# @param dict A psi-tet dictionary
# @param types A list of the DMD methods which were used
def make_reconstructions(dict,types):
    t0 = dict['t0']
    tf = dict['tf']
    dictname = dict['filename']
    data = dict['SVD_data']
    size_bpol = np.shape(dict['sp_Bpol'])[0]
    size_btor = np.shape(dict['sp_Btor'])[0]
    index = size_bpol
    imp_index = size_bpol+size_btor+8
    inj_index = 2
    if dict['is_HITSI3']:
        inj_index = 3
    time = dict['sp_time'][t0:tf]*1000
    tsize = len(time)
    for i in range(len(types)):
        typename = types[i]
        if typename==1:
            reconstr = dict['dmd_b']
            labelstring = 'DMD'
            color = 'b'
        elif typename==2:
            reconstr = dict['sdmd_b']
            labelstring = 'sparse DMD'
            color = 'r'
        elif typename==3:
            reconstr = dict['odmd_b']
            labelstring = 'optimized DMD'
            color = 'g'
        elif typename==7:
            continue
        plt.figure(2000,figsize=(figx, figy))
        plt.subplot(len(types),1,i+1) #plt.subplot(len(types),1,i+2)
        plt.plot(time, \
            data[index+inj_index,:]*1e4,'k',linewidth=lw)
        plt.plot(time[:tsize-1], \
            reconstr[index+inj_index,:tsize-1]*1e4,color,\
            label=labelstring+' reconstruction',linewidth=lw, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
        #plt.subplot(len(types),1,i+1) # get rid of this
        if i==0:
            plt.title(dict['filename'][7:13]+', Probe: B_L01T000', \
                fontsize=fs)
        plt.grid(True)
        ax = plt.gca()
        ax.tick_params(axis='both', which='major', labelsize=ts)
        ax.tick_params(axis='both', which='minor', labelsize=ts)
        plt.legend(fontsize=ls,loc='upper left')
        if i == len(types)-1:
            plt.xlabel('Time (ms)',fontsize=fs)
        plt.ylabel('B (G)',fontsize=fs)
        plt.ylim((-150,300))
        #plt.ylim((-500,1000))
        #ax.set_yticks([-500,0,500,1000])
        ax.set_yticks([-150,0,150,300])
        plt.figure(3000,figsize=(figx, figy))
        plt.subplot(len(types),1,i+1) #plt.subplot(len(types),1,i+2)
        plt.plot(time, \
            data[imp_index+inj_index,:]*1e4,'k',linewidth=3)
        plt.plot(time[:tsize-1], \
            reconstr[imp_index+inj_index,:tsize-1]*1e4,color,\
            label=labelstring+' reconstruction',linewidth=3) #, \
            #path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            #pe.Normal()])
        if i==0:
            plt.title('BIG-HIT, Probe: IMP #8', \
                fontsize=fs)
        plt.grid(True)
        ax = plt.gca()
        ax.tick_params(axis='both', which='major', labelsize=ts)
        ax.tick_params(axis='both', which='minor', labelsize=ts)
        plt.legend(fontsize=ls,loc='upper left')
        if i == len(types)-1:
            plt.xlabel('Time (ms)',fontsize=fs)
        plt.ylabel('B (G)',fontsize=fs)
    plt.figure(2000)
    plt.savefig(out_dir+'reconstructions'+str(dictname)+'_sp.png')
    plt.figure(3000)
    plt.savefig(out_dir+'reconstructions'+str(dictname)+'_imp.png')

## Makes (R,phi) contour plots of B_theta (poloidal B field)
# @param dict A psi-tet dictionary
# @param flag which DMD method to use
def toroidal_plot(dict,flag):
    t0 = dict['t0']
    tf = dict['tf']
    time = dict['sp_time'][t0:tf]*1000.0
    tsize = len(time)
    offset = 2
    if dict['is_HITSI3']:
        offset = 3
    bpol_size = np.shape(dict['sp_Bpol'])[0]
    btor_size = np.shape(dict['sp_Btor'])[0]
    bpol_imp_size = np.shape(dict['imp_Bpol'])[0]
    phis_imp = np.zeros(160*8)
    rads_imp = np.zeros(160*8)
    for i in range(8):
        phis_imp[i*160:(i+1)*160] = np.ones(160)*imp_phis8[i]
        rads_imp[i*160:(i+1)*160] = np.ones(160)*imp_rads
    if flag == 2:
        tstep = 500
        bpol_eq_imp = dict['sdmd_b_eq'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_inj_imp = dict['sdmd_b_inj'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_imp = dict['sdmd_b'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_extra_imp = dict['sdmd_b_extra'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_inj_phase_imp = dict['sdmd_b_inj_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_phase_imp = dict['sdmd_b_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_inj_phase_imp = dict['sdmd_b_inj_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_eq_phase_imp = dict['sdmd_b_eq_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_extra_phase_imp = dict['sdmd_b_extra_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
    elif flag == 3:
        tstep = 500
        bpol_eq_imp = dict['odmd_b_eq'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_inj_imp = dict['odmd_b_inj'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_imp = dict['odmd_b'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_extra_imp = dict['odmd_b_extra'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_phase_imp = dict['odmd_b_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_inj_phase_imp = dict['odmd_b_inj_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_eq_phase_imp = dict['odmd_b_eq_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_extra_phase_imp = dict['odmd_b_extra_phase'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]

    is_phase = False
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_reconstruction.gif'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time,is_phase),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=5)

    bpol_imp = bpol_imp - bpol_inj_imp - bpol_eq_imp
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_subtracted_reconstruction.gif'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time,is_phase),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=5)

    bpol_imp = bpol_extra_imp
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_Extra_reconstruction.gif'
    ani = animation.FuncAnimation( \
       fig, update_tor_Rphi, range(0,tsize,tstep), \
       fargs=(movie_bpol,midplaneR,midplanePhi, \
       rorig,phiorig,time,is_phase),repeat=False, \
       interval=100, blit=False)
    ani.save(moviename,fps=5)

    bpol_imp = bpol_extra_imp
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads[35:110],midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_Extra_reconstruction_zoomed.gif'
    ani = animation.FuncAnimation( \
       fig, update_tor_Rphi, range(0,tsize,tstep), \
       fargs=(movie_bpol,midplaneR,midplanePhi, \
       rorig,phiorig,time,is_phase),repeat=False, \
       interval=100, blit=False)
    ani.save(moviename,fps=5)

    bpol_imp = bpol_eq_imp
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_Eq_reconstruction.gif'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time,is_phase),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=5)

    bpol_imp = bpol_inj_imp
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_inj_reconstruction.gif'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time,is_phase),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=5)

    is_phase = True
    bpol_imp = bpol_phase_imp+pi
    print(np.min(bpol_phase_imp),np.max(bpol_phase_imp))
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_full_phase_reconstruction.gif'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time,is_phase),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=5)

    bpol_imp = bpol_extra_phase_imp+pi
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_extra_phase_reconstruction.gif'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time,is_phase),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=5)

    bpol_imp = bpol_eq_phase_imp+pi
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_eq_phase_reconstruction.gif'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time,is_phase),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=5)

    bpol_imp = bpol_inj_phase_imp+pi
    bpol_imp_frame = bpol_imp[:,0]
    bpol_imp_frame_periodic = np.ravel([bpol_imp_frame, \
        bpol_imp_frame, bpol_imp_frame])
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rorig = np.ravel([rads_imp[::10], rads_imp[::10], rads_imp[::10]])
    phiorig = np.ravel([phis_imp[::10]-2*pi, phis_imp[::10], phis_imp[::10]+2*pi])
    plt.plot(rorig,phiorig,'ko',markersize=10)
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    grid_bpol = np.asarray( \
        griddata((rorig,phiorig),bpol_imp_frame_periodic, \
        (midplaneR,midplanePhi),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    plt.xlim(0,1.2849)
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.ylim((0,2*pi))
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    moviename = out_dir+'toroidal_Rphi_inj_phase_reconstruction.gif'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time,is_phase),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=5)

## Update function for FuncAnimation object
## for the (R,Z) contour plots
# @param frame A movie frame number
# @param Bpol Poloidal B in the plane
# @param bowtieR Radial coordinates of the bowtie boundary
# @param bowtieZ Z coordinates of the bowtie boundary
# @param R Radial coordinates of the 2D mesh
# @param Z Z coordinates of the 2D mesh
# @param time Array of times
def update_tor_XY(frame,Bpol,midplaneX,midplaneY,x,y,time):
    print(frame)
    plt.clf()
    plt.xlabel('X (m)',fontsize=fs)
    h = plt.ylabel('Y (m)',fontsize=fs)
    h.set_rotation(0)
    plt.title('Time = '+'{0:.3f}'.format(time[frame])+' ms',fontsize=fs)
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    # plot the probe locations
    plt.plot(x, y,'ko',label='Probes')
    circle = Circle((0,0),radius=1.34)
    patches = [circle]
    p = PatchCollection(patches, alpha = 1.0)
    p.set_edgecolors('k')
    p.set_facecolors('w')
    ax.add_collection(p)
    Bpol_frame = Bpol[:,frame]
    grid_bpol = np.asarray( \
        griddata((x,y),Bpol_frame, \
        (midplaneX,midplaneY),'cubic'))
    v = np.linspace(-1,1,11)
    #v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneX,midplaneY, \
        grid_bpol,v,cmap=colormap) #, \
        #norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    cbar.ax.tick_params(labelsize=ts)
    plt.xlim(0,1.2849)
    plt.legend(fontsize=fs-12,loc='lower center')

## Update function for FuncAnimation object
## for the (R,phi) contour plots
# @param frame A movie frame number
# @param Bpol Poloidal B in the plane
# @param midplaneR Radial coordinates where we interpolate
# @param midplanePhi Toroidal coordinates where we interpolate
# @param R Radial coordinates of the probes
# @param phi Toroidal coordinates of the probes
# @param time Array of times
# @param is_phase Whether or not to plot contours of the phase of Bpol
def update_tor_Rphi(frame,Bpol,midplaneR,midplanePhi,R,phi,time,is_phase):
    print(frame)
    plt.clf()
    plt.xlabel('R (m)',fontsize=fs)
    h = plt.ylabel(r'$\phi$',fontsize=fs+5)
    h.set_rotation(0)
    plt.title('Time = '+'{0:.3f}'.format(time[frame])+' ms',fontsize=fs)
    #plt.locator_params(axis='y', nbins=9)
    ax = plt.gca()
    #ax.yaxis.set_major_formatter(FuncFormatter(format_fn))
    #ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    # plot the probe locations
    plt.plot(R, phi,'ko',markersize=ms,label='Probes')
    plt.plot([(1.0+0.625)/2.0,(1.0+0.625)/2.0], \
        [pi/8.0,pi+pi/8.0],'ro',markersize=ms, \
        markeredgecolor='k',label='X Injector Mouths')
    plt.plot([(1.0+0.625)/2.0,(1.0+0.625)/2.0], \
        [pi/2.0+pi/8.0,3*pi/2.0+pi/8.0],'yo', \
        markersize=ms,markeredgecolor='k',label='Y Injector Mouths')
    #ax.set_yticks([0,pi/4,pi/2,3*pi/4,pi, \
    #    5*pi/4,3*pi/2,7*pi/4,2*pi])
    ax.set_yticks([0,pi/2,pi,3*pi/2,2*pi])
    ax.set_yticklabels(clabels)
    #plt.xlim((imp_rads[60],imp_rads[119]))
    ax.tick_params(axis='x', which='major', labelsize=ts)
    ax.tick_params(axis='x', which='minor', labelsize=ts)
    ax.tick_params(axis='y', which='major', labelsize=ts+10)
    ax.tick_params(axis='y', which='minor', labelsize=ts+10)
    #ax.set_xticks([0.2,0.4,0.6,0.8,1.0,1.2])
    Bpol_frame = Bpol[:,frame]
    if is_phase:
        grid_bpol = np.asarray( \
            griddata((R,phi),Bpol_frame,(midplaneR,midplanePhi),'cubic'))
        v = np.linspace(0,2*pi,13)
        for i in range(np.shape(grid_bpol)[0]):
            for j in range(np.shape(grid_bpol)[1]):
                if grid_bpol[i,j] < 0.0:
                    grid_bpol[i,j] = grid_bpol[i,j]+2*pi
                elif grid_bpol[i,j] > 2*pi:
                    grid_bpol[i,j] = grid_bpol[i,j]-2*pi

        #grid_bpol = np.nan_to_num(grid_bpol)
        print(np.min(grid_bpol),np.max(grid_bpol))
        contour = plt.contourf(midplaneR,midplanePhi, \
            grid_bpol,v,cmap='twilight_shifted',label=r'$B_\theta$') #, \
    else:
        grid_bpol = np.asarray( \
            griddata((R,phi),Bpol_frame,(midplaneR,midplanePhi),'cubic'))
        #v = np.linspace(-1,1,11)
        v = np.logspace(-3,0,10)
        v = np.ravel([-np.flip(v),v])
        grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
        contour = plt.contourf(midplaneR,midplanePhi, \
            grid_bpol,v,cmap=colormap,label=r'$B_\theta$', \
            norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    cbar = plt.colorbar(ticks=v,extend='both')
    cbar.ax.tick_params(labelsize=ts)
    ax.set_xticklabels([0,0.25,0.5,0.75,1.0,1.25])
    if is_phase:
        cbar.ax.set_yticklabels(cbarlabels)
    plt.legend(fontsize=ls-12,loc='lower right')
    plt.ylim((0,2*pi))
    plt.xlim(0,1.2849)

