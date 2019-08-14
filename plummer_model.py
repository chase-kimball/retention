import numpy as np
from scipy.integrate import trapz
from scipy.stats import rv_continuous
import astropy.constants as c
import astropy.units as u
class Plummer_pdf(rv_continuous):
    '''
    density pdf from Hernquist potential
    '''
    def __init__(self, a_plum, Mcluster, momtype=1, a=0, b=None, xtol=1e-14,
                 badvalue=None, name=None, longname=None,
                 shapes=None, extradoc=None, seed=None):
        rv_continuous.__init__(self, momtype, a, b, xtol,
                 badvalue, name, longname,
                 shapes, extradoc, seed)
        self.a_plum = a_plum
        self.Mcluster = Mcluster

    def _pdf(self, r):
        # r, abulge in parsecs
        #Mcluster in Msun
        # plummer density model * 4pi*r**2 divided by Mcluster
        # Turns mass density function to probability density function.
        
        # rvs() requires _pdf normalized to 1 on domain, which in this case is [0,inf]
        # Leaving Mcluster in there normalizes to Mcluster. Check normalization by printing Plummer_pdf.cdf(big number)
        # WARNING: Cluster_pdf.cdf(np.inf) will always return 1 because it assumes we normalized correctly
        

        return 3.*(r**2)*(self.a_plum**-3)*(1.+(r/self.a_plum)**2)**(-5./2.)
    def potential(self, r):
        #a, a_plum in parsecs
        #Mcluster in Msun
        
        r = r*u.pc.to(u.m)
        a_plum = self.a_plum*u.pc.to(u.m)
        Mcluster = self.Mcluster*u.M_sun.to(u.kg)
        
        return -c.G.value*Mcluster/np.sqrt(r**2+a_plum**2)
    def vesc(self,r):
        #r in parsecs
        #returns in km/s
        return np.sqrt(-2*self.potential(r))*u.m.to(u.km)
