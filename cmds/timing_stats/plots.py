import matplotlib.pylab as pl
import numpy as np

execfile('new_calc.py')
_=h

# 'pixrad','npix','burninlen','nmodels','t_init','t_ev',
# 't_burnin','t_model','t_thread','t_wallclock','dt_burnin','dt_model'


x = _.pixrad
y = _.t_burnin

fdata = filt(data.siamese,200,_.nmodels)
dat = fdata[:,x]
wei = fdata[:,y]

s = int(min(dat))
e = int(max(dat)) 
ds = 1
#s = 100
#e = 2000

bins = np.arange(s-0.5,e+ds+.5,ds)
ebin = np.arange(s,e+1,ds)

binned = np.histogram(dat, bins, weights=wei)[0]
npbin = np.histogram(dat, bins)[0]

bin_means = binned / npbin

c = np.isnan(bin_means)
ebin2 = ebin[~c]
bm2 = bin_means[~c]

def plot():
  pl.plot(ebin2, bm2)
  pl.plot(dat, wei, '.')
  pl.xlabel(_[x])
  pl.ylabel(_[y])
  pl.show()