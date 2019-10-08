import numpy as np
import precession as pr
import argparse
import itertools
import pandas as pd
import os
####### Parse Arguments #######

parser = argparse.ArgumentParser()
parser.add_argument('-rlf','--random-locations-file', type = str,
                    help = 'Location of pandas datafram with bank of \
                            randomly drawn merger locations and escape \
                            velocities',
                    required = True)
parser.add_argument('-out', '--out_directory', type=str, required=True)

parser.add_argument('-N','--Nsamps',type=int,
                    help = 'Number of kicks and merger locations to sample \
                            per (amag1,amag2,q)',
                    default = 100)
parser.add_argument('-maxkick','--maxkick', action='store_true')
parser.add_argument('-Na','--Na', type = int, default = 10)
parser.add_argument('-Nq','--Nq', type = int, default = 10)
parser.add_argument('-l','--label',type = str, default='')
parser.add_argument('-Nbatch','--Nbatch',type = int, default = 1)
parser.add_argument('-batch','--batch',type=int,default=1)
###############################

def _get_kicks(amag1,amag2,q,Nsamps,maxkick):
    
    v_kicks = []

    M,m1,m2,S1,S2 = pr.get_fixed(q,amag1,amag2)
    t1 = np.random.uniform(-1,1,Nsamps)
    t2 = np.random.uniform(-1,1,Nsamps)
    phi = np.random.uniform(0,2*np.pi,Nsamps)
    for ii in range(Nsamps):
        kick =  pr.finalkick(np.arccos(t1[ii]),np.arccos(t2[ii]),phi[ii],
                                   q,S1,S2,maxkick=maxkick,kms=True
                                   )
                      




        v_kicks.append(kick)

    return np.array(v_kicks)

def retention_fraction(a1a2q,vescs,Nsamps,maxkick=True):
    a1,a2,q = a1a2q
    v_kicks = _get_kicks(a1,a2,q,Nsamps,maxkick)
    v_mean = np.mean(v_kicks)
    v_median = np.median(v_kicks)
    vesc_samples = np.random.choice(vescs,Nsamps)
    return float(len(np.where(v_kicks<
                              vesc_samples)[0]))/len(v_kicks),v_mean,v_median
    
def run_retention_grid(Na, Nq, vescs, Nsamps, Nbatch, batch, maxkick):
    a1s = np.linspace(0,1,Na)
    a2s = np.linspace(0,1,Na)
    qs = np.linspace(.001,1,Nq)
    
    A1A2Q_all =list(itertools.product(a1s,a2s,qs))
    batchsize = len(A1A2Q_all)/Nbatch
    A1A2Q = A1A2Q_all[batch*batchsize:(batch+1)*batchsize]
    for ii in range(len(A1A2Q)):
        print(ii)
        rf, v_mean, v_median = retention_fraction(A1A2Q[ii],vescs,Nsamps,maxkick)
        A1A2Q[ii]=np.append(A1A2Q[ii],[rf,v_mean,v_median])
        print(A1A2Q[ii])
    A1A2Q_Retention = A1A2Q
    return A1A2Q_Retention
if __name__ == '__main__':
    args= parser.parse_args()
    
    tag = '_'.join(args.random_locations_file.split('_')[-4:])
    outdir = args.out_directory+'/'+args.label+'_'+tag
    if not os.path.isdir(outdir):
        os.system('mkdir '+outdir)
    radius_str = tag.split('_')[1]
    mass_str = tag.split('_')[3]
    v_escs = pd.read_csv(args.random_locations_file).v_esc.values
    print('Running cluster model  with Plummer radius {0} and  mass {1} \n{2} samples per grid-node and maxkick = {3}'.format(radius_str,mass_str,args.Nsamps,args.maxkick))
    
    fracs = run_retention_grid(args.Na,args.Nq,v_escs,args.Nsamps,args.Nbatch,args.batch,args.maxkick)
    np.savetxt(outdir+'/retention_fractions_'+str(args.batch),fracs)



