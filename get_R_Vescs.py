import numpy as np
import plummer_model
import h5py
import pickle
import argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('--mass', type=float,required=True)
parser.add_argument('--radius', type=float,required=True)
parser.add_argument('--Nsamps', type=int,default=1000)

args=parser.parse_args()

cluster = plummer_model.Plummer_pdf(args.radius,args.mass)
rs = cluster.rvs(size=args.Nsamps)
vescs = cluster.vesc(rs)
df = pd.DataFrame(dict(zip(['R_merge','v_esc'],[rs,vescs])))
df.to_csv('plummer_samples/'+str(int(np.log10(args.Nsamps)))+'_A_'+str(args.radius)+'_M_{:.0E}'.format(args.mass))
print(df)
