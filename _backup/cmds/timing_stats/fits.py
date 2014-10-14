import matplotlib.pylab as pl
import numpy as np

from numpy import array, exp
from scipy.optimize import leastsq


execfile('new_calc.py')
_=h

# 'pixrad','npix','burninlen','nmodels','t_init','t_ev',
# 't_burnin','t_model','t_thread','t_wallclock','dt_burnin','dt_model'

def f(params, t, p, n):
  a1, a2, a3 = params
  return a1*p**5 + a2*n + a3 - t

# t_burn(p,n)
def f1(params, t, p, n):
  a1, a2 = params
  return a1*p**7 + a2 - t

#t_thread(p,n)
def f2(params, t, p, n):
  a1, a2, a3 = params
  return a1*p**7 + a2*n*3 + a3 - t

  
p = data.anker[:,h.pixrad]
n = data.anker[:,h.nmodels]

t1 = data.anker[:,h.t_burnin]
t2 = data.anker[:,h.t_thread]

a1 = 0.00001
a2 = 0.1

b1 = 0.001
b2 = 0.01
b3 = 1


print '%i datapoints fitted' % len(t1)
p_t_burn, _   = leastsq(f1,  array([a1, a2]), args=(t1, p, n))
p_t_thread, _ = leastsq(f2,  array([b1, b2, b3]), args=(t2, p, n))



# parameters from manual fit of actuall messured time on anker, 2.8 ghz, see timings.hand.odt
aa1 = 34.104
bb1 = -28.033
def at_burn(p, n):
  return aa1*f1(p_t_burn, 0, p, n)+bb1
  
# parameters from manual fit of actuall messured time on anker, 2.8 ghz
aa2 = 0.9857
bb2 = 2.3436
def at_thread(p, n):
  return aa2*f2(p_t_thread, 0, p, n)+bb2
  
cc1 = 0#p/4.*3. # arb. offset
def tottime(p, n):
  return at_burn(p, n) + at_thread(p,n) + cc1
  
  
# testing
act_pn  = np.array([[10,500],
                    [10,1000],
                    [10,2000],
                    [ 8,500],
                    [ 8,1000],
                    [ 8,2000],
                    [12,500],
                    [12,1000],
                    [12,2000],
                    [ 6,1000],
                    [ 7,1000],
                    [ 8,1000],
                    [ 9,1000],
                    [10,1000],
                    [11,1000],
                    [12,1000]])
                    
act_time = np.array([84, 99, 129, 25, 30, 41, 278, 329, 395, 18, 22, 30, 56, 99, 222, 329], dtype=np.float32)

dt = act_time * 0
dtp = act_time * 0
for i, (p, n) in enumerate(act_pn):
  t = tottime(p, n)
  dt[i] = np.abs(t-act_time[i])
  dtp[i] = 100.0*(1.0-act_time[i] / t)
  print '%2i / %4i | calc: %6.2f | actual: %6.2f | delta: %6.2f / %5.1f%%' % (p, n, t, act_time[i], dt[i], dtp[i])

print 'average error: %6.3f / %5.1f' % (np.average(dt), np.sqrt(np.average(dtp**2)))


a = np.arange(6,13)
r = np.array([3+6,3+6,4+7,5+7,7+8,9+9,12+9])


print "\n--- FINAL RESULT ---"
print 'tottime(p,n) = at_burn(p, n) + at_thread(p,n) + cc1'
print 'at_burn(p, n) = aa1*f1(p_t_burn, 0, p, n)+bb1'
print 'at_thread(p,n) = aa2*f2(p_t_thread, 0, p, n)+bb2'
print 'with:'
for t, v in [('aa1',aa1), ('bb1',bb1), ('aa2',aa2), ('bb2',bb2), ('cc1',cc1)]:
  print '  ', t, '%7.3f' % v
print 'and:'
print 'p_t_burn(p,n) = a1*p**7 + a2'
print ' with a1=',p_t_burn[0],' a2=',p_t_burn[1]
print 'p_t_thread(p,n) = a1*p**7 + a2*n*3 + a3'
print ' with a1=',p_t_thread[0],' a2=',p_t_thread[1],' a3=',p_t_thread[2]
print ''
print 'function tottime(p,n) {'
print '  //parameters from variious fits'
print '  //machine: how much slower is the worker than anker (@2.8Ghz): 2.21 for mite'
for t, v in [ ('aa1',aa1), ('bb1',bb1),
              ('aa2',aa2), ('bb2',bb2), ('cc1',cc1),
              ('a11', p_t_burn[0]), ('a12', p_t_burn[1]),
              ('a21', p_t_thread[0]), ('a22', p_t_thread[1]), ('a23', p_t_thread[2]),
              ('machine', 2.21)]:
  print '  var %s=%14.10f;' % (t,v)
print '  return machine*(aa1*(a11*Math.pow(p,7) + a12)+bb1 + aa2*(a21*Math.pow(p,7) + a22*n*3 + a23)+bb2 + cc1);};'
