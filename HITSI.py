## @package HITSI
## Takes a large list of command line arguments
## and collects the files in dictionaries,
## gets their SVD, calls all the DMD methods
## and then plots all the results.
from plot_attributes import *
from psitet_load import loadshot
from utilities import SVD, \
    plot_itor, plot_chronos,
    write_Bfield_csv, \
    bar_plot
from dmd import DMD_slide
from dmd_plotting import \
    make_reconstructions, \
    toroidal_plot
import click

@click.command()
@click.option('--dmd', \
    default=0, \
    multiple=True, \
    help='Chooses which DMD method to use: '+ \
        'DMD options are dmd, sparse dmd, and optimized dmd, '+ \
        'corresponding to 1-3, (0 for no dmd)')
@click.option('--numwindows', \
    default=1, \
    help='Number of windows to use for DMD')
@click.option('--directory', \
    default='/media/removable/SD Card/Two-Temperature-Post-Processing/', \
    help='Directory containing the .mat files')
@click.option('--filenames', \
    default=['exppsi_129499.mat'],multiple=True, \
    help='A list of all the filenames, which '+ \
        'allows a large number of shots to be '+ \
        'compared')
@click.option('--freqs', \
    default=14.5,multiple=True, \
    help='A list of all the injector frequencies (kHz) which '+ \
        'correspond to the list of filenames')
@click.option('--imp', \
    default=0,type=int, \
    help='Number of IMP signals')
@click.option('--limits', \
    default=(22.7,28.5),type=(float,float),multiple=True, \
    help='Time limits for each of the discharges')
@click.option('--nprocs', \
    default=1,type=int, \
    help='Number of threads for numba to use (only relevant for oDMD). '+\
        'Note that this does not guarantee numba will use all these threads.')
@click.option('--trunc', \
    default=10,type=int, \
    help='Where to truncate the SVD')

## Main program that accepts python 'click' command line arguments.
## Note that options with multiple=true must have multiple values added
## separately so that the command line command would be --dmd 1 --dmd 2
## rather than --dmd 1 2 or something. This format could also be done
## by declaring --dmd to be of type (int,int). If a description
## of the various click options is desired, just type
## python HITSI.py --help
def analysis(dmd,numwindows,directory,filenames,freqs, \
    imp,limits,nprocs,trunc):

    print('Running with the following command line options: ')
    print('DMD method(s) = ',dmd)
    print('Truncation number for the SVD = ', trunc)
    print('Number of windows = ',numwindows)
    print('Directory where the files to analyze reside: ',directory)
    print('File(s) to load = ',filenames)
    print('Frequencies corresponding to those files = ',freqs)
    print('Time limits for each of the files = ',limits)
    print('Number of threads for numba = ',nprocs)

    is_HITSI3 = False
    if(len(filenames[0])==9):
        is_HITSI3=True
    filenames=np.atleast_1d(filenames)
    freqs=np.atleast_1d(freqs)
    all_dicts = []
    for i in range(len(filenames)):
        filename = filenames[i]
        f_1 = np.atleast_1d(freqs[i])
        if filenames[i][0:10]=='Psi-Tet-2T':
            temp_dict = loadshot('Psi-Tet-2T',directory, \
                int(f_1),True,True,is_HITSI3,limits[i])
        elif filenames[i][0:3]=='Psi':
            temp_dict = loadshot('Psi-Tet',directory, \
                int(f_1),True,False,is_HITSI3,limits[i])
        else:
            temp_dict = loadshot(filename,directory, \
                np.atleast_1d(int(f_1)),False,False, \
                is_HITSI3,limits[i])
        if imp == 0:
            temp_dict['use_IMP'] = False
            temp_dict['num_IMPs'] = 0
        else:
            temp_dict['use_IMP'] = True
            temp_dict['num_IMPs'] = imp
        temp_dict['nprocs'] = nprocs
        temp_dict['trunc'] = trunc
        temp_dict['f_1'] = f_1
        all_dicts.append(temp_dict)

    all_dicts = np.asarray(all_dicts).flatten()
    for i in range(len(filenames)):
        SVD(all_dicts[i])
        plot_itor(all_dicts[i])
        plot_chronos(all_dicts[i])

    for k in range(len(dmd)):
        if dmd[k] > 0 and dmd[k] < 4:
            DMD_slide(all_dicts,numwindows,dmd[k])
            make_reconstructions(all_dicts[0],dmd[k])
            if all_dicts[0]['use_IMP']:
                if k == len(dmd)-1:
                    toroidal_plot(all_dicts[0],dmd[k])
        else:
            print('Invalid --dmd option, will assume no dmd')
    bar_plot(all_dicts[0])

if __name__ == '__main__':
    analysis()
