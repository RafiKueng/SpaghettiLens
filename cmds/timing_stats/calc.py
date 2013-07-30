from numpy import array, exp
from scipy.optimize import leastsq




def res(params, t, p, n):
    a1, a2, b1, b2, c = params
    #return a1*n*exp(a2*p)+b1*exp(b2*p)+c - t
    #return a1*n*p**3 + a2*p**3 + c - t
    
    #for t2
    #return a1*n + a2*p**b1 + c - t

    #for t3
    return a1*n + a2*p**b1 + c - t
    
    
# load a, b, c

p = array([ 6, 7,10,10, 10, 8, 8, 8, 12, 12, 12])
n = array([10,10, 5,10, 20, 5,10,20,  5, 10, 20])*100
t1= array([18,22,84,99,129,25,30,41,278,329,395])
t2= array([4,  4,55,55, 55,10,10,10,220,220,220])
t3= array([5,  9,14,29, 59, 5, 9,20, 43, 87,156])

t=t3

a1 = 0
a2 = 1
b1 = 7
b2 = 1
c = 20

p_opt, _ = leastsq(res,  array([a1, a2, b1, b2, c]), args=(t, p, n))

for _ in p_opt:
  print '%3.3f' % _

print p_opt

for i in range(len(p)):
  r=res(p_opt, 0, p[i], n[i])
  print  '%2i: %2i %4i | %4i | %6.1f || %6.1f'%(i, p[i], n[i], t[i], r, r-t[i])


  
  
  