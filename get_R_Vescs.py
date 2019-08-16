import numpy as np
import plummer_model
import h5py
import pickle
import argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('--mass', type=float,
                    help = 'Cluster mass in units of solar mass.'
                    required=True)
parser.add_argument('--radius', type=float,
                    help = 'Plummer radius a_p in parsecs.\
                            Half-mass radius ~1.3 a_p.\
                            Virial radius ~1.7 a_p.'
                           required=True)
parser.add_arguemnt('-out','--out-directory', type = str)

parser.add_argument('--Nsamps', type=int,default=1000)
parser.add_argument('
args=parser.parse_args()

cluster = plummer_model.Plummer_pdf(args.radius,args.mass)
rs = cluster.rvs(size=args.Nsamps)
vescs = cluster.vesc(rs)
df = pd.DataFrame(dict(zip(['R_merge','v_esc'],[rs,vescs])))
df.to_csv('plummer_samples/'+str(int(np.log10(args.Nsamps)))+'_A_'+str(args.radius)+'_M_{:.0E}'.format(args.mass))
print(df)
