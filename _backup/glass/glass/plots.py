from __future__ import division
import pylab as pl
import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.lines as mpll
from matplotlib import rc
from matplotlib.ticker import LogLocator
from matplotlib.patches import Circle, Ellipse
from matplotlib.lines import Line2D
from collections import defaultdict
from itertools import count, izip, product

from glass.environment import env
from glass.command import command
from glass.log import log as Log
from glass.scales import convert
from glass.shear import Shear
from glass.utils import dist_range

from scipy.ndimage.filters import correlate1d
from scipy.misc import central_diff_weights

# added by rafik
import scipy.interpolate as interp
import scipy.optimize as optimize
from matplotlib import colors as mplcolors

import glass.exmass

rc('text', usetex=True)
#rc('text', dvipnghack=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})

_styles = [{'label':r'rejected', 'c':'r', 'ls':'-', 'z':-1, 'line':Line2D([],[],c='r',ls='-')},
           {'label':r'accepted', 'c':'b', 'ls':'-', 'z': 0, 'line':Line2D([],[],c='b',ls='-')},
           {'label':r'unknown',  'c':'k', 'ls':'-', 'z':+1, 'line':Line2D([],[],c='k',ls='-')}]

_system_colors = 'gbmykw'
_source_colors = 'c'

def system_color(i): return _system_colors[i%len(_system_colors)]
def source_color(i): return _source_colors[i%len(_source_colors)]

def _style_iterator(colors='gbrcm'):
    _linestyles = [k for k,v, in mpll.lineStyles.iteritems() if not v.endswith('nothing')]
    _linestyles.sort()
    for lw in count(1):
        for ls in _linestyles:
            for clr in colors:
                yield lw,ls,clr

def style_iterator():
    if env().bw_styles:
        return _style_iterator('k')
    else:
        return _style_iterator()

def default_kw(R, kw={}):
    kw.setdefault('extent', [-R,R,-R,R])
    kw.setdefault('interpolation', 'nearest')
    kw.setdefault('aspect', 'equal')
    kw.setdefault('origin', 'upper')
    kw.setdefault('fignum', False)
    kw.setdefault('cmap', cm.bone)
    #if vmin is not None: kw['vmin'] = vmin
    #if vmax is not None: kw['vmax'] = vmax
    return kw

def index_to_slice(i):
    if i is None: 
        return slice(None)
    else:
        return slice(i,i+1)

def glscolorbar():
    rows,cols,_ = pl.gca().get_geometry()
    x,y = pl.gcf().get_size_inches()
    pars = pl.gcf().subplotpars
    left = pars.left
    right = pars.right
    bottom = pars.bottom
    top = pars.top
    wspace = x*pars.wspace
    hspace = y*pars.hspace
    totWidth = x*(right-left)
    totHeight = y*(top-bottom)

    figH = (totHeight-(hspace*(rows>1))) / rows
    figW = (totWidth-(wspace*(cols>1))) / cols

    pl.colorbar(shrink=figW/figH)

@command
def show_plots(env):
    pl.show()

@command
def img_plot(env, **kwargs): #src_index=None, with_maximum=True, color=None, with_guide=False, tight=False):

    obj_index = kwargs.pop('obj_index', 0)
    src_index = kwargs.pop('src_index', None)
    tight     = kwargs.pop('tight', False)
    with_guide = kwargs.pop('with_guide', False)
    color = kwargs.pop('color', None)
    with_maximum = kwargs.pop('with_maximum', True)

    if src_index is not None and not isinstance(src_index, (list,tuple)):
        src_index = [src_index]

    #obj,_ = model['obj,data'][obj_index]
    obj = env.objects[obj_index]

#   if isinstance(model, (list, tuple)):
#       obj,_ = model
#   else:
#       obj = model

    oxlim, oylim = pl.xlim(), pl.ylim()

    rmax = 0
    si = style_iterator()
    for i,src in enumerate(obj.sources):
        lw,ls,c = si.next()

        if src_index is not None and i not in src_index: continue
        xs,ys,cs = [], [], []

        for img in src.images:
            #print img.pos
            if not with_maximum and img.parity_name == 'max': continue

            xs.append(img.pos.real)
            ys.append(img.pos.imag)
            if not color:
                if img.parity_name == 'unk':
                    cs.append('red')
                else:
                    cs.append(c)
            else:
                cs.append(color)

        if xs and ys:
            pl.over(pl.scatter,xs, ys, s=80, c=cs, zorder=1000, alpha=1.0)
            if with_guide or tight:
                a = pl.gca()
                for x,y in zip(xs,ys):
                    r = np.sqrt(x**2 + y**2)
                    rmax = np.amax([r,rmax])
                    if with_guide:
                        a.add_artist(Circle((0,0),r, fill=False,color='lightgrey'))

    pl.xlim(oxlim); pl.ylim(oylim)

    if tight and rmax > 0:
        pl.gca().set_xlim(-rmax, rmax)
        pl.gca().set_ylim(-rmax, rmax)

@command
def external_mass_plot(env, obj_index=0, with_maximum=True, color=None, with_guide=False, tight=False):

    #obj,_ = model['obj,data'][obj_index]
    #obj,_ = model['obj,data'][obj_index]
    si = style_iterator()
    for i in xrange(obj_index+1):
        lw,ls,c = si.next()
    obj = env.objects[obj_index]

    #print obj.external_masses

#   if isinstance(model, (list, tuple)):
#       obj,_ = model
#   else:
#       obj = model

    oxlim, oylim = pl.xlim(), pl.ylim()

    rmax = 0
    xs,ys,cs = [], [], []
    for i,m in enumerate(obj.extra_potentials):
        if isinstance(m, Shear): continue

        xs.append(m.r.real)
        ys.append(m.r.imag)
        if not color:
            cs.append(c)
        else:
            cs.append(color)

        rmax = np.amax([np.abs(m.r),rmax])

    if xs and ys:
        pl.over(pl.scatter,xs, ys, s=160, c=cs, zorder=1000, alpha=1.0, marker='s')

    pl.xlim(oxlim); pl.ylim(oylim)

    if tight and rmax > 0:
        pl.pl.gca().set_pl.xlim(-rmax, rmax)
        pl.pl.gca().set_pl.ylim(-rmax, rmax)

@command
def Re_plot(env, models=None, obj_index=0, color=None):

    if models is None:
        models = env.models
    elif not hasattr(models, '__getslice__'):
        models = [models]

    if not color: color = 'k'

    for m in models:
        obj,data = m['obj,data'][obj_index]
        print data.keys()
        if not data['Re']: continue
        Re, a,b, theta = data['Re']
        #pl.gca().add_artist(Circle((rl.real,rl.imag), 0.1, fill=False, lw=2, color='r'))
        #pl.gca().add_artist(Circle((rs.real,rs.imag), 0.1, fill=False, lw=2, color='r'))
        #pl.gca().add_artist(Line2D([0,A[0]], [0,A[1]], lw=2, color=color))
        #pl.gca().add_artist(Line2D([0,B[0]], [0,B[1]], lw=2, color=color))
        #pl.gca().add_artist(Circle((0,0), a, fill=False, lw=2, color=color))
        #pl.gca().add_artist(Circle((0,0), b, fill=False, lw=2, color=color))
        pl.gca().add_artist(Ellipse((0,0), 2*a,2*b, theta, fill=False, lw=2, color=color))
        #pl.gca().add_artist(Circle((0,0), a, fill=False, lw=2, color=color))

@command
def src_plot(env, models=None, **kwargs):

    obj_index = kwargs.pop('obj_index', 0)
    src_index = kwargs.pop('src_index', None)
    hilite_model = kwargs.pop('hilite_model', None)
    hilite_color = kwargs.pop('hilite_color', 'g')

    if models is None: models = env.models

    oxlim, oylim = pl.xlim(), pl.ylim()

    def plot(model, si, hilite=False):
        obj, data = model
        xs = []
        ys = []
        cs = []
        for i,sys in enumerate(obj.sources):
            if src_index is not None and i != src_index: continue
            xs.append(data['src'][i].real)
            ys.append(data['src'][i].imag)
            lw,ls,c = si.next()
            cs.append(c) #system_color(i))
        if hilite:
            pl.over(scatter,xs, ys, s=80, c=hilite_color, zorder=2000, marker='x', alpha=1.0, **kwargs)
        else:
            pl.scatter(xs, ys, s=80, c=cs, zorder=1000, marker='d', alpha=0.5, facecolor='none', linewidths=1, **kwargs)
            #pl.over(scatter,xs, ys, s=80, c=cs, zorder=1000, marker='d', alpha=0.5, facecolor='none', linewidths=1)

    if isinstance(models, dict):
        si = style_iterator()
        plot(models['obj,data'][obj_index], si)
    else:
        for mi,model in enumerate(models):
            for m in model['obj,data']:
                si = style_iterator()
                plot(m, si, mi==hilite_model)

    pl.xlim(oxlim); pl.ylim(oylim)

    #if isinstance(models, (list,tuple)) and len(models)>0 and isinstance(models[0], (list,tuple)):
    #else:

def src_hist(**kwargs):
    xlabel = kwargs.get('xlabel', r'$r$ $(\mathrm{arcsec})$')
    ylabel = kwargs.get('ylabel', r'$\mathrm{Count}$')
    models = kwargs.get('models', None)
    hilite_model = kwargs.get('hilite_model', None)
    if models is None: models = env.models

    d = []
    hilite=[]
    for mi,model in enumerate(models):
        for [_,data] in model['obj,data']:
            r = list(np.abs(data['src']))
            d += r
            if mi == hilite_model: hilite += r
    pl.hist(d, histtype='step', log=False)
    for i,r in enumerate(hilite):
        print r
        pl.axvline(r, c=system_color(i), ls='-', zorder=-2, alpha=0.5)

    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

@command
def image_plot(env, im, radius, center, format=None):
    dx, dy = center
    if  isinstance(radius, (list,tuple)):
        Rx,Ry = radius
    else:
        Rx = Ry = radius
    kw = {}
    kw['extent'] = [-Rx-dx,Rx-dx,-Ry-dy,Ry-dy]
    if format:
        kw['format'] = format
    pl.imshow(pl.imread(im), **kw)

#def kappa_avg_plot(models):
#    objs = {} 
#    for m in models:
#        for [obj, data] in m['obj,data']:
#            a = 
#
#    grid

def mass_plot(model, obj_index, with_contours=True, only_contours=False, clevels=30):
    print "WARNING: use of mass_plot is deprecated. Use kappa_plot instead."
    return kappa_plot(model, obj_index, with_contours, only_contours, clevels)

@command
def kappa_plot(env, model, obj_index, **kwargs):
    obj, data = model['obj,data'][obj_index]
    if not data: return

    with_contours   = kwargs.pop('with_contours', False)
    only_contours   = kwargs.pop('only_contours', False)
    label_contours  = kwargs.pop('label_contours', False)
    clevels         = kwargs.pop('clevels', 30)
    with_colorbar   = kwargs.pop('with_colorbar', True)
    vmin            = kwargs.pop('vmin', None)
    vmax            = kwargs.pop('vmax', None)
    subtract        = kwargs.pop('subtract', 0)
    xlabel          = kwargs.pop('xlabel', r'arcsec')
    ylabel          = kwargs.pop('ylabel', r'arcsec')

#   print pl.gca()
#   print pl.gca().get_frame()
#   print pl.gca().get_frame().get_bbox()
#   print pl.gca().get_geometry()
#   print pl.gca().get_position()
#   print pl.gca().get_window_extent()
#   l= pl.gca().get_axes_locator()
#   print l
#   help(l)
#   #help(pl.gca())
#   assert 0

    R = obj.basis.mapextent
    kw = default_kw(R, kwargs)

    #grid = obj.basis.kappa_grid(data)
    #print data['kappa'].shape
    #print subtract
    grid = obj.basis._to_grid(data['kappa']-subtract,1)
    if vmin is None:
        w = data['kappa'] != 0
        if not np.any(w):
            vmin = -15
            grid += 10**vmin
        else:
            vmin = np.log10(np.amin(data['kappa'][w]))
        #print 'min?', np.amin(data['kappa'] != 0)
        kw.setdefault('vmin', vmin)

    if vmax is not None:
        kw.setdefault('vmax', vmax)

    grid = np.log10(grid.copy()) # + 1e-15)
#   grid2 = grid.copy() 
#   for i in xrange(grid.shape[0]):
#       for j in xrange(grid.shape[1]):
#           grid[i,j] = abs(grid2[grid.shape[0]-i-1, grid.shape[1]-j-1] - grid[i,j]) / grid[i,j]
#   grid = grid.copy() + 1e-4

    #grid[grid >= 1] = 0


    if not only_contours:
        #pl.matshow(np.log10(grid), **kw)
        pl.matshow(grid, **kw)
        #imshow(grid, fignum=False, **kw)
        #pl.matshow(grid, fignum=False, **kw)
        if with_colorbar: 
            glscolorbar()

    if only_contours or with_contours:
        #if 'colors' in kw and 'cmap' in kw:
            #kw.pop('cmap')

        kw.setdefault('colors', 'w')
        kw.setdefault('extend', 'both')
        kw.setdefault('alpha', 0.7)
        kw.pop('cmap')
        #kw.pop('colors')
        C = pl.contour(grid, clevels, **kw)
        if label_contours:
            pl.clabel(C, inline=1, fontsize=10)
        pl.gca().set_aspect('equal')

    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

@command
def grad_kappa_plot(env, model, obj_index, which='x', with_contours=False, only_contours=False, clevels=30, with_colorbar=True):
    obj, data = model['obj,data'][obj_index]

    R = obj.basis.mapextent

    grid = obj.basis.kappa_grid(data)
    grid = grid.copy()

    kw = default_kw(R)
    kw['vmin'] = -1
    kw['vmax'] =  2

    if not only_contours:
        print '!!!!!!', grid.shape
        if which == 'x': grid = np.diff(grid, axis=1)
        if which == 'y': grid = np.diff(grid, axis=0)
        print '!!!!!!', grid.shape
        pl.matshow(grid, **kw)
        if with_colorbar: 
            glspl.colorbar()

    if with_contours:
        kw.pop('cmap')
        pl.over(contour, grid, clevels, extend='both', colors='k', alpha=0.7, **kw)

    pl.xlabel('arcsec')
    pl.ylabel('arcsec')

@command
def potential_plot(env, model, obj_index, src_index, with_colorbar=True, with_contours=False):
    obj, data = model['obj,data'][obj_index]
    R = obj.basis.mapextent
    grid = obj.basis.potential_grid(data)
    levs = obj.basis.potential_contour_levels(data)
#   pl.matshow(grid, fignum=False, extent=[-R,R,-R,R], interpolation='nearest')
    pl.matshow(grid, fignum=False, cmap=cm.bone, extent=[-R,R,-R,R], interpolation='nearest')
    if with_colorbar: glspl.colorbar()
#   pl.contour(grid, extent=[-R,R,-R,R], origin='upper')
    #print levs
    if with_contours:
        for i,lev in enumerate(levs):
            pl.over(contour, grid, lev, colors = system_color(i), 
                 extent=[-R,R,-R,R], origin='upper', extend='both')


    pl.xlabel('arcsec')
    pl.ylabel('arcsec')
#   figure();
#   xs = linspace(-R, R, grid.shape[0])
#   plot(xs, grid[grid.shape[1]//2, :], 'k-')
#   plot(xs, 5*xs, 'r-')

    #pl.suptitle('Potential')

@command
def critical_curve_plot(env, model, obj_index, src_index):
    obj, data = model['obj,data'][obj_index]
    R = obj.basis.mapextent
    g = obj.basis.maginv_grid(data)[src_index]
    pl.matshow(g, fignum=False, cmap=cm.bone, extent=[-R,R,-R,R], interpolation='nearest')
    pl.over(contour, g, [0], colors='g', linewidths=1, extent=[-R,R,-R,R], origin='upper')

@command
def arrival_plot(env, model, **kwargs):

    obj_index       = kwargs.pop('obj_index', None)
    src_index       = kwargs.pop('src_index', None)
    only_contours   = kwargs.pop('only_contours', None)
    clevels         = kwargs.pop('clevels', None)
    with_colorbar   = kwargs.pop('with_colorbar', False)
    xlabel          = kwargs.pop('xlabel', r'arcsec')
    ylabel          = kwargs.pop('ylabel', r'arcsec')

    obj_slice = slice(None) if obj_index is None else obj_index

    obj_slice = index_to_slice(obj_index)
    src_slice = index_to_slice(src_index)
    #if src_index is not None:
        #assert 0, 'arrival_plot: src_index not yet supported'


    def plot_one(obj,data,src_index,g,lev,kw):
        matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
        #loglev = logspace(1, log(amax(g)-amin(g)), 20, base=math.e) + amin(g)
        if not only_contours:
            kw.update({'zorder':-100})
            pl.matshow(np.log10(g), **kw)
            if with_colorbar: glspl.colorbar()

        if 'cmap' in kw: kw.pop('cmap')
        if clevels:
            loglev=clevels
            #loglev = logspace(1, log(g.ptp()), clevels, base=math.e) + amin(g)
            #loglev = 1 / logspace(1/ log(amax(g)-amin(g)), 1, clevels, base=math.e) + amin(g)
            #loglev = 1 / logspace(1/ log10(amax(g)-amin(g)), 1, clevels) + amin(g)
            kw.update({'zorder':-1000})
            pl.contour(g, loglev, **kw)
        if lev:
            kw.update({'zorder':1000})
            kw.update({'colors': 'k', 'linewidths':2, 'cmap':None})
            #kw.update({'colors':system_color(src_index), 'linewidths':3, 'cmap':None})
            pl.contour(g, lev, **kw)

    for obj,data in model['obj,data'][obj_slice]:
        if not data: continue

        print len(obj.sources[src_slice])
        lev = obj.basis.arrival_contour_levels(data)
        print len(lev)
        arrival_grid = obj.basis.arrival_grid(data)
        for i,src in enumerate(obj.sources[src_slice]):

            #print src.index, len(lev)
            if lev: levels = lev[src.index]
            g = arrival_grid[src.index]

            S = obj.basis.subdivision
            R = obj.basis.mapextent
            kw = default_kw(R, kwargs)
            kw.update(kwargs)
            kw.setdefault('colors', 'grey')
            kw.setdefault('linewidths', 1)
            kw.setdefault('cmap', None)

            plot_one(obj,data,src.index,g,levels,kw)
            pl.xlim(-obj.basis.mapextent, obj.basis.mapextent)
            pl.ylim(-obj.basis.mapextent, obj.basis.mapextent)

    pl.gca().set_aspect('equal')
    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

@command
def srcdiff_plot(env, model, **kwargs):
    obj_index       = kwargs.pop('obj_index', 0)
    src_index       = kwargs.pop('src_index', 0)
    with_colorbar   = kwargs.pop('with_colorbar', False)
    xlabel          = kwargs.pop('xlabel', r'arcsec')
    ylabel          = kwargs.pop('ylabel', r'arcsec')

    obj, data = model['obj,data'][obj_index]
    S = obj.basis.subdivision
    R = obj.basis.mapextent

    g = obj.basis.srcdiff_grid(data)[src_index]
    vmin = np.log10(np.amin(g[g>0]))
    g = g.copy() + 1e-10
    kw = default_kw(R, kwargs) #, vmin=vmin, vmax=vmin+2)

    #loglev = logspace(1, log(amax(g)-amin(g)), 20, base=math.e) + amin(g)
    pl.matshow(np.log10(g), **kw)
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    if with_colorbar: glspl.colorbar()
#   pl.over(contour, g, 50,  colors='w',               linewidths=1, 
#        extent=[-R,R,-R,R], origin='upper', extend='both')
    #pl.grid()

    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

@command
def srcdiff_plot_adv(env, model, **kwargs):
    obj_index       = kwargs.pop('obj_index', 0)
    src_index       = kwargs.pop('src_index', 0)
    xlabel          = kwargs.pop('xlabel', r'')
    ylabel          = kwargs.pop('ylabel', r'')
    nightMode       = kwargs.pop('night', False) # colormode for use with black background (use with savefig(.. facecolor='black'))
    upsample        = kwargs.pop('upsample', False) # upsample this
    ppp             = kwargs.pop('range', 0.5) # map values [vmin, vmin + ppp*(vmax-vmin)] to colormap grayscale [white ... black]; aka dynamic range;


    obj, data = model['obj,data'][obj_index]
      
    S = obj.basis.subdivision
    R = obj.basis.mapextent

    g = obj.basis.srcdiff_grid(data)[src_index]

    #set outside to max value    
    gmax = np.amax(g)
    g += np.array(g==0, dtype=float)*gmax
    
    if upsample:
      xdim, ydim = np.shape(g)
      R = obj.basis.mapextent
      #print xdim, ydim
      xvec = np.linspace(-R, R, xdim)
      yvec = np.linspace(-R, R, ydim)
      from scipy.interpolate import RectBivariateSpline
      interpol = RectBivariateSpline(xvec, yvec, g)
      
      xnew = np.linspace(-R, R, xdim*upsample)
      ynew = np.linspace(-R, R, ydim*upsample)
      
      g = interpol(xnew, ynew)            

    
    vmin = np.log10(np.amin(g[g>0]))
    vmax = np.log10(np.amax(g[g>0]))
    

    gdat = np.log10(g + 1e-10)
    gave = np.average(gdat)
    kw = default_kw(R, kwargs) #, vmin=vmin, vmax=vmin+2)
    kw['vmin'] = vmin
    kw['vmax'] = vmin + ppp*(vmax-vmin)    # remember: arraival time: small -> brigt -> inner parts
    kw['cmap'] = 'Greys'
    print vmin, vmax, gave

    #loglev = logspace(1, log(amax(g)-amin(g)), 20, base=math.e) + amin(g)

    ax = pl.gca()
    fig = pl.gcf()
    
    if nightMode:
      fig.set_facecolor('black')
      fig.patch.set_facecolor('black')
    else:
      pass
    
    pl.matshow(gdat, **kw)
    fig.set_facecolor('black')
      
    if nightMode:
      pl.xlabel('')
      pl.ylabel('')
      pl.axis('off')
      pl.tight_layout() #if this doesn't work update matplotlib
    else:
      pl.xlabel(xlabel)
      pl.ylabel(ylabel)


@command
def kappa_enclosed_plot(env, model, **kwargs):
    obj_index       = kwargs.pop('obj_index', 0)
    src_index       = kwargs.pop('src_index', 0)
    err_margin      = kwargs.pop('err_margin', 1) #err_margin = 0.9 -> 90% -> values within from 5% .. 95%
    xlabel          = kwargs.pop('xlabel', r'image radius [SpaceWarps pixels]')
    ylabel          = kwargs.pop('ylabel', r'mean convergance [1]')
    plot_rE         = kwargs.pop('plot_rE', True)
    plot_rE_box     = kwargs.pop('plot_rE_box', True)
    rscale           = kwargs.pop('rscale', 440./500*100) #default Spacewarps -> SL -> glass scaling of radius

    obj, data = model['obj,data'][obj_index]

    ### HELPER FUNCTION ########################################
    def getEinsteinR(x, y):
      poly = interp.PiecewisePolynomial(x,y[:,np.newaxis])
      
      def one(x):
        return poly(x)-1
      
      x_min = np.min(x)
      x_max = np.max(x)
      x_mid = poly(x[len(x)/2])
      
      rE,infodict,ier,mesg = optimize.fsolve(one, x_mid, full_output=True)
      
      #print rE,infodict,ier,mesg
      
      if (ier==1 or ier==5) and x_min<rE<x_max and len(rE)==1:
        return rE[0]
      elif len(rE)>1:
        for r in rE:
          if x_min<r<x_max:
            return r
      else:
        return -1


    
    ### DO THE CALCULATIONS ####################################
    # maybe you want to put this stuff to another file..
    
    # def constants
    n_rings = len(obj.basis.rings) # number of rings with center (=pixrad+1)
    distance_factor = 0.428 #TODO don't hardcode this one..

    # init vars
    kappaRenc_median = np.zeros(n_rings)
    kappaRenc_xsigmaplus = np.zeros(n_rings)
    kappaRenc_xsigmaminus = np.zeros(n_rings)
    
    pixPerRing = np.zeros(n_rings)
    pixEnc = np.zeros(n_rings)

    # get pixels per ring and encolsed pixels per ring
    #TODO this data is probably already around??
    for i in range(n_rings):
      pixEnc[i] = len(obj.basis.rings[i])
      pixPerRing[i] = len(obj.basis.rings[i])
      for j in range(i):
        pixEnc[i] += len(obj.basis.rings[j])

    # collect data
    
    kappaRenc_median


    if 1:
      for k in range(n_rings):
        kappaRenc_k_all = np.zeros(0)
        for m in env.models:
          obj,ps = m['obj,data'][0]
    
          kappaRenc_model = ps['kappa(R)'][k]*pixPerRing[k]
          for kk in range(k):
            kappaRenc_model += ps['kappa(R)'][kk] * pixPerRing[kk]
          kappaRenc_k_all = np.append(kappaRenc_k_all,kappaRenc_model)
    
        kappaRenc_k_all /= pixEnc[k]
        kappaRenc_k_all *= distance_factor
        kappaRenc_k_all = np.sort(kappaRenc_k_all)
        
        kappaRenc_median[k] = kappaRenc_k_all[len(kappaRenc_k_all)/2]
        
        if 0 < err_margin < 1:
          p = err_margin / 2.
          kappaRenc_xsigmaplus[k] = kappaRenc_k_all[int((0.5+p)*len(kappaRenc_k_all))]
          kappaRenc_xsigmaminus[k] = kappaRenc_k_all[int((0.5-p)*len(kappaRenc_k_all))]
        elif err_margin == 1:
          kappaRenc_xsigmaplus[k] = kappaRenc_k_all[-1]
          kappaRenc_xsigmaminus[k] = kappaRenc_k_all[0]
        else:
          #TODO crash gracefully
          kappaRenc_xsigmaplus[k] = 0
          kappaRenc_xsigmaminus[k] = 0
    
    else:
      for mod in env.models:
        for rng in range(n_rings):
          kappaR[mod, rng]
    
    
    
    x_vals = (np.arange(n_rings)+0.5) * rscale * obj.basis.cell_size[0]  
    
    # calulate einstein radii
    if plot_rE:
      rE_mean = getEinsteinR(x_vals, kappaRenc_median)
      rE_max = getEinsteinR(x_vals, kappaRenc_xsigmaplus)
      rE_min = getEinsteinR(x_vals, kappaRenc_xsigmaminus)
      if rE_mean<0 or rE_max<0 or rE_min<0:
        plot_rE = False

    
    ### DO THE PLOTTING ########################################
    
    if plot_rE:
      a_re_min = np.array([rE_min, rE_min])
      a_re_max = np.array([rE_max, rE_max])
      a_re_mean = np.array([rE_mean, rE_mean])
      
      # define some text properties      
      mmax = np.amax(kappaRenc_xsigmaplus)
      rE_pos = max(round(mmax*0.75), 3) # there to draw the einsteinradius text
      t_dx = 0.0 # text offset position
      t_dy = 0.1
      t_props = {'ha':'left', 'va':'bottom'}       
      

      pl.plot(a_re_mean, [0,rE_pos], '--', color=(0,0.5,0))
      pl.text(rE_mean+t_dx, rE_pos+t_dy, 'r_E = %4.2f [%4.2f .. %4.2f]'%(rE_mean, rE_min, rE_max), **t_props)

      if plot_rE_box:
        # this would allow for a colored box with gradient, see the cdict
        cy = np.ones(rE_pos*4) # spaced in 1/4 steps, rE_pos is int!
        cy[0]=0
        cy[1]=0.5
        cy[-1]=0
        cy[-2]=0.5
        cy = np.array([cy,cy]).transpose()
        cdict = { 'red':   ((0,0,0),(1,0,0)),
                  'green': ((0,0.5,0.5),(1,0.5,0.5)),
                  'blue':  ((0,0,0),(1,0,0)),
                  'alpha': ((0,1,1),(1,1,1))}
        cmblue = mplcolors.LinearSegmentedColormap('DarkGreen', cdict)
        pl.imshow(cy, interpolation='bilinear', cmap=cmblue, extent=(rE_min, rE_max, 0.0, rE_pos), alpha=0.7, aspect='auto')
      else:
        pl.plot(a_re_min, [0,rE_pos-0.25], ':b')
        pl.plot(a_re_max, [0,rE_pos-0.25], ':b')

    pl.plot(x_vals, kappaRenc_xsigmaplus, 'b')
    pl.plot(x_vals, kappaRenc_xsigmaminus, 'b')
    pl.fill_between(x_vals, kappaRenc_xsigmaplus, kappaRenc_xsigmaminus, facecolor='blue', alpha=0.5)
    pl.plot([0,np.amax(x_vals)], [1,1], ':m')         
    
    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

 
    
    
@command
def deflect_plot(env, model, obj_index, which, src_index):
    obj, data = model['obj,data'][obj_index]
    S = obj.basis.subdivision
    R = obj.basis.mapextent

    g = obj.basis.deflect_grid(data, which, src_index)

    #vmin = np.log10(amin(g[g>0]))
    g = g.copy() + 1e-10
    kw = default_kw(R, vmin=None, vmax=None)

    pl.matshow(g, **kw)
    #matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

@command
def grad_tau(env, model, obj_index, which, src_index):

    assert which in ['x','y'], "grad_tau: 'which' must be one of 'x' or 'y'"

    #print "grad_tau"
    obj,ps = model['obj,data'][obj_index]
    R = obj.basis.mapextent

    #---------------------------------------------------------------------------
    # Find the derivative of the arrival time surface.
    #---------------------------------------------------------------------------
    arrival = obj.basis.arrival_grid(ps)[src_index]

    w = central_diff_weights(3)

    which = 1 if which == 'x' else 0
    d = correlate1d(arrival, w, axis=which, mode='constant')

    d = d[1:-1,1:-1]
    d[np.abs(d) < 1e-3] = 0
    d[d>0] = 1
    d[d<0] = -1
    pl.matshow(d, fignum=False, extent=[-R,R,-R,R], alpha=0.5)

@command
def deriv(env, model, obj_index, src_index, m, axis, R):
    w = central_diff_weights(5)
    #d = correlate1d(m, w, axis=axis, mode='constant')
    d = (correlate1d(m, -w, axis=0, mode='constant')) \
      + (correlate1d(m,  w, axis=1, mode='constant'))
    d = (correlate1d(d, -w, axis=0, mode='constant')) \
      + (correlate1d(d,  w, axis=1, mode='constant'))
    d = d[2:-2,2:-2]
    d[d>.8] = .8
    d[d<-.8] = -.8
    #d = correlate1d(d, w, axis=axis, mode='constant')
    #d = diff(d, axis=axis)
    #d /= abs(d)
    #d = correlate1d(d, w, axis=axis, mode='constant')
    #d = diff(d, axis=axis)

    R -= model[0].basis.top_level_cell_size * 2
    #R -= model[0].basis.top_level_cell_size * 2
    pl.matshow(d, extent=[-R,R,-R,R])
    glspl.colorbar()
    arrival_plot(model, obj_index, src_index, only_contours=True, clevels=200)
    #img_plot(model, src_index=src_index)
    #pl.matshow(d)

#   d = d[1:-1,1:-1]
#   d[d>0] = 1
#   d[d<0] = -1
#   pl.matshow(d, extent=[-R,R,-R,R])
#   img_plot(model, src_index=src_index)

@command
def inout_plot(env, model, obj_index, src_index):
    print "inout"
    obj,ps = model['obj,data'][obj_index]
    R = obj.basis.mapextent
    arrival = obj.basis.arrival_grid(ps)[src_index]

    deriv(model, obj_index, src_index, arrival, 0, R)
    deriv(model, obj_index, src_index, arrival, 1, R)

def _find_key(xs, key):
    if hasattr(key, '__iter__'):
        for k in key[:-1]:
            xs = xs[k]
        key = key[-1]
    return xs[key]

def _data_plot(models, X,Y, **kwargs):
    with_legend = False
    use = [0,0,0]

    if isinstance(X, basestring): X = [X,None]
    if isinstance(Y, basestring): Y = [Y,None]

    x_prop, x_units = X
    y_prop, y_units = Y

    ret_list = []

    every           = kwargs.pop('every', 1)
    upto            = kwargs.pop('upto', len(models))
    mark_images     = kwargs.pop('mark_images', True)
    hilite_model    = kwargs.pop('hilite_model', None)
    hilite_color    = kwargs.pop('hilite_color', 'm')
    yscale          = kwargs.pop('yscale', 'log')
    xscale          = kwargs.pop('xscale', 'linear')
    xlabel          = kwargs.pop('xlabel', None)
    ylabel          = kwargs.pop('ylabel', None)

    kwargs.setdefault('color', 'k')
    kwargs.setdefault('marker', '.')
    kwargs.setdefault('ls', '-')

    normal_kw   = {'zorder':0,    'drawstyle':'steps', 'alpha':1.0}
    hilite_kw   = {'zorder':1000, 'drawstyle':'steps', 'alpha':1.0, 'lw':4, 'ls':'--'}
    accepted_kw = {'zorder':500,  'drawstyle':'steps', 'alpha':0.5}

    normal = []
    hilite = []
    accepted = []
    #imgs = set()
    imgs = defaultdict(set)
    xmin, xmax = np.inf, -np.inf
    ymin, ymax = np.inf, -np.inf

    objplot = defaultdict(dict)
    for mi in xrange(0,upto,every):
        m = models[mi]

        si = m.get('accepted', 2)
        tag = ''
        if si==False: tag = 'rejected'
        if si==True: tag = 'accepted'

        for [obj, data] in m['obj,data']:

            try:
                xs = data[x_prop][x_units]
                ys = data[y_prop][y_units]

                xlabel = _axis_label(xs, x_units) if not xlabel else None
                ylabel = _axis_label(ys, y_units) if not ylabel else None

                objplot[obj].setdefault(tag, {'ys':[], 'xs':None})
                objplot[obj][tag]['ys'].append(ys)
                objplot[obj][tag]['xs'] = xs

                #objplot[obj].setdefault('%s:xs'%tag, xs)
                #objplot[obj].setdefault('%s:ymax'%tag, ys)
                #objplot[obj].setdefault('%s:ymin'%tag, ys)
                #objplot[obj].setdefault('%s:ysum'%tag, np.zeros_like(ys))
                #objplot[obj].setdefault('%s:count'%tag, 0)

                #objplot[obj]['%s:ymax'%tag]  = np.amax((objplot[obj]['%s:ymax'%tag], ys), axis=0)
                #objplot[obj]['%s:ymin'%tag]  = np.amin((objplot[obj]['%s:ymin'%tag], ys), axis=0)
                #objplot[obj]['%s:ysum'%tag] += ys
                #objplot[obj]['%s:count'%tag] += 1

                if mark_images:
                    for i,src in enumerate(obj.sources):
                        for img in src.images:
                            imgs[i].add(convert('arcsec to %s' % x_units, np.abs(img.pos), obj.dL, data['nu']))

            except KeyError as bad_key:
                print "Missing information for object %s with key %s. Skipping plot." % (obj.name,bad_key)
                continue

            use[si] = 1

            s = _styles[si]

            #xmin, xmax = min(xmin, amin(data[X])), max(xmax, amax(data[X]))
            #ymin, ymax = min(ymin, amin(data[Y])), max(ymax, amax(data[Y]))

    for i,tag in enumerate(['rejected', 'accepted', '']):
        for k,v in objplot.iteritems():
            if tag not in v: break

            ys = np.array(v[tag]['ys'])
            xs = np.repeat(np.atleast_2d(v[tag]['xs']), len(ys), axis=0)

            ret_list.append([xs,ys])
            if tag == 'rejected':
                pl.plot(xs, ys, c=_styles[0]['c'], zorder=_styles[0]['z'])
            else:
                pl.plot(xs.T, ys.T, **kwargs)

#   return

    pl.yscale(yscale)
    pl.xscale(xscale)

    si = style_iterator()
    for k,v in imgs.iteritems():
        lw,ls,c = si.next()
        for img_pos in v:
            pl.axvline(img_pos, c=c, ls=ls, lw=lw, zorder=-2, alpha=0.5)

#   if use[0] or use[1]:
#       lines  = [s['line']  for s,u in zip(_styles, use) if u]
#       labels = [s['label'] for s,u in zip(_styles, use) if u]
#       pl.legend(lines, labels)

    if use[0]:
        lines  = [ _styles[0]['line'] ]
        labels = [ _styles[0]['label'] ]
        pl.legend(lines, labels)

    #axis('scaled')
    if xlabel: pl.xlabel(xlabel)
    if ylabel: pl.ylabel(ylabel)
    pl.xlim(xmin=pl.xlim()[0] - 0.01*(pl.xlim()[1] - pl.xlim()[0]))
    #pl.ylim(0, ymax)

    return ret_list

def _axis_label(data, units):
    label = '%s' % data.symbol
    if units is not None: label += ' (%s)' % data.label(units)
    return label

def _data_error_plot(models, X,Y, **kwargs):
    with_legend = False
    use = [0,0,0]

    if isinstance(X, basestring): X = [X,None]
    if isinstance(Y, basestring): Y = [Y,None]

    x_prop, x_units = X
    y_prop, y_units = Y

    ret_list = []

    every           = kwargs.pop('every', 1)
    upto            = kwargs.pop('upto', len(models))
    mark_images     = kwargs.pop('mark_images', True)
    hilite_model    = kwargs.pop('hilite_model', None)
    hilite_color    = kwargs.pop('hilite_color', 'm')
    yscale          = kwargs.pop('yscale', 'log')
    xscale          = kwargs.pop('xscale', 'linear')
    xlabel          = kwargs.pop('xlabel', None)
    ylabel          = kwargs.pop('ylabel', None)
    sigma           = kwargs.pop('sigma', '1sigma')

    kwargs.setdefault('color', 'k')
    kwargs.setdefault('marker', '.')
    kwargs.setdefault('ls', '-')

    normal_kw   = {'zorder':0,    'drawstyle':'steps', 'alpha':1.0}
    hilite_kw   = {'zorder':1000, 'drawstyle':'steps', 'alpha':1.0, 'lw':4, 'ls':'--'}
    accepted_kw = {'zorder':500,  'drawstyle':'steps', 'alpha':0.5}

    normal = []
    hilite = []
    accepted = []
    #imgs = set()
    imgs = defaultdict(set)
    xmin, xmax = np.inf, -np.inf
    ymin, ymax = np.inf, -np.inf

    objplot = defaultdict(dict)
    for mi in xrange(0,upto,every):
        m = models[mi]

        si = m.get('accepted', 2)
        #print si
        tag = ''
        if si==False: tag = 'rejected'
        if si==True: tag = 'accepted'

        for [obj, data] in m['obj,data']:

            try:
                xs = data[x_prop][x_units]
                ys = data[y_prop][y_units]

                xlabel = _axis_label(xs, x_units) if not xlabel else xlabel
                ylabel = _axis_label(ys, y_units) if not ylabel else ylabel

                objplot[obj].setdefault(tag, {'ys':[], 'xs':None})
                objplot[obj][tag]['ys'].append(ys)
                objplot[obj][tag]['xs'] = xs

                #objplot[obj].setdefault('%s:xs'%tag, xs)
                #objplot[obj].setdefault('%s:ymax'%tag, ys)
                #objplot[obj].setdefault('%s:ymin'%tag, ys)
                #objplot[obj].setdefault('%s:ysum'%tag, np.zeros_like(ys))
                #objplot[obj].setdefault('%s:count'%tag, 0)

                #objplot[obj]['%s:ymax'%tag]  = np.amax((objplot[obj]['%s:ymax'%tag], ys), axis=0)
                #objplot[obj]['%s:ymin'%tag]  = np.amin((objplot[obj]['%s:ymin'%tag], ys), axis=0)
                #objplot[obj]['%s:ysum'%tag] += ys
                #objplot[obj]['%s:count'%tag] += 1

                if mark_images:
                    for i,src in enumerate(obj.sources):
                        for img in src.images:
                            imgs[i].add(convert('arcsec to %s' % x_units, np.abs(img.pos), obj.dL, data['nu']))

            except KeyError as bad_key:
                print "Missing information for object %s with key %s. Skipping plot." % (obj.name,bad_key)
                continue

            use[si] = 1

            s = _styles[si]

            #xmin, xmax = min(xmin, amin(data[X])), max(xmax, amax(data[X]))
            #ymin, ymax = min(ymin, amin(data[Y])), max(ymax, amax(data[Y]))

    for i,tag in enumerate(['rejected', 'accepted', '']):
        for k,v in objplot.iteritems():
            if tag not in v: break
            #if not v.has_key('%s:count'%tag): break

            avg, errp, errm = dist_range(v[tag]['ys'], sigma=sigma)
            errp = errp - avg
            errm = avg - errm
            #s = np.sort(v[tag]['ys'], axis=0)
            #avg = s[len(s)//2] if len(s)%2==1 else (s[len(s)//2] + s[len(s)//2+1])/2
            #print s
            #avg = np.median(v[tag]['ys'], axis=0)
            #print avg
            #print np.median(v[tag]['ys'], axis=1)
            #errp = s[len(s) * .841] - avg
            #errm = avg - s[len(s) * .159]

            #errp = np.amax(v[tag]['ys'], axis=0) - avg
            #errm = avg - np.amin(v[tag]['ys'], axis=0)
            #errp = errm = np.std(v[tag]['ys'], axis=0, dtype=np.float64)
            xs = v[tag]['xs']

#           print [x[1] for x in v[tag]['ys']]
#           pl.hist([x[1] for x in v[tag]['ys']])
#           break

            #avg = v['%s:ysum'%tag] / v['%s:count'%tag]
            #errp = v['%s:ymax'%tag]-avg
            #errm = avg-v['%s:ymin'%tag]
            #errm = errp = np.std(

            #print len(v['xs'])
            #print len(avg)
            #assert 0
            #print len(xs)
            #print len(avg)

            ret_list.append([xs,avg,errm,errp])
            yerr = (errm,errp) if not np.all(errm == errp) else None
            if tag == 'rejected':
                pl.errorbar(xs, avg, yerr=yerr, c=_styles[0]['c'], zorder=_styles[0]['z'])
            else:
                pl.errorbar(xs, avg, yerr=yerr, **kwargs)

#   return

    pl.xscale(xscale)
    pl.yscale(yscale)

    si = style_iterator()
    for k,v in imgs.iteritems():
        lw,ls,c = si.next()
        for img_pos in v:
            pl.axvline(img_pos, c=c, ls=ls, lw=lw, zorder=-2, alpha=0.5)

#   if use[0] or use[1]:
#       lines  = [s['line']  for s,u in zip(_styles, use) if u]
#       labels = [s['label'] for s,u in zip(_styles, use) if u]
#       pl.legend(lines, labels)

    if use[0]:
        lines  = [ _styles[0]['line'] ]
        labels = [ _styles[0]['label'] ]
        pl.legend(lines, labels)

    #axis('scaled')
    if xlabel: pl.xlabel(xlabel)
    if ylabel: pl.ylabel(ylabel)
    pl.xlim(xmin=pl.xlim()[0] - 0.01*(pl.xlim()[1] - pl.xlim()[0]))
    #pl.ylim(0, ymax)

    return ret_list

@command
def glplot(env, ptype, xkeys, ykeys=[], **kwargs):
    if not ykeys: ykeys = ptype
    models = kwargs.pop('models', env.models)
    _data_plot(models, xkeys, ykeys, **kwargs)

@command
def glerrorplot(env, ptype, xkeys, ykeys=[], **kwargs):
    if not ykeys: ykeys = ptype
    models = kwargs.pop('models', env.models)
    return _data_error_plot(models, xkeys, ykeys, **kwargs)

@command
def H0inv_plot(env, **kwargs):
    _hist(env, '1/H0', xlabel=r'$H_0^{-1}$ (Gyr)')
    return

    models      = kwargs.pop('models', env.models)
    obj_index   = kwargs.pop('obj_index', 0)
    key         = kwargs.pop('key', 'accepted')
    xlabel      = kwargs.pop('xlabel', r'$H_0^{-1}$ (Gyr)')
    ylabel      = kwargs.pop('ylabel', r'Count')

    # select a list to append to based on the 'accepted' property.
    l = [[], [], []]
    for m in models:
        obj, data = m['obj,data'][0] # For H0inv we only have to look at one model because the others are the same
        l[m.get(key,2)].append(data['1/H0'])
        #l[2].append(data['kappa'][1])

    #print amin(l[2]), amax(l[2])

    not_accepted, accepted, notag = l

    #print 'H0inv_plot',H0s

    for d,s in zip(l, _styles):
        if d:
            #print len(d), d
            #pl.hist(d, bins=20, histtype='step', edgecolor=s['c'], zorder=s['z'], label=s['label'])
            pl.hist(d, bins=np.ptp(d)//1+1, histtype='step', edgecolor=s['c'], zorder=s['z'], label=s['label'], **kwargs)

    #if not_accepted or accepted:
        #pl.legend()

    pl.axvline(13.7, c='k', ls=':', zorder = 2)

    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

    if accepted or not not_accepted:
        if accepted:
            h = np.array(accepted)
        else:
            h = np.array(accepted + notag)

        hs = np.sort(h)
        l = len(hs)

        m = hs[l * 0.50]
        u = hs[l * (0.50 + 0.341)]
        l = hs[l * (0.50 - 0.341)]
        #u = hs[l * 0.68]
        #l = hs[l * 0.32]

        pl.axvline(m, c='r', ls='-', zorder = 2)
        pl.axvline(u, c='g', ls='-', zorder = 2)
        pl.axvline(l, c='g', ls='-', zorder = 2)

        print 'H0inv_plot: ', m, u, l
        print 'H0inv_plot: ', m, (u-m), (m-l)
    else:
        print "H0inv_plot: No H0inv values accepted"

_H0_xlabel = r'$H_0$ (km/s/Mpc)'
@command
def H0_plot(env, **kwargs):
    _hist(env, 'H0', xlabel=r'$H_0$ (km/s/Mpc)')
    return

    models = kwargs.pop('models', env.models)
    obj_index = kwargs.pop('obj_index', 0)
    key = kwargs.pop('key', 'accepted')

    # select a list to append to based on the 'accepted' property.
    l = [[], [], []]
    for m in models:
        obj, data = m['obj,data'][obj_index] # For H0 we only have to look at one model because the others are the same
        l[m.get(key,2)].append(data['H0'])
        #print 'nu', data['nu']
        #l[2].append(data['kappa'][1])

    #print amin(l[2]), amax(l[2])

    not_accepted, accepted, notag = l

    #print 'H0_plot',H0s

    for d,s in zip(l, _styles):
        if d:
            #print len(d), d
            #pl.hist(d, bins=20, histtype='step', edgecolor=s['c'], zorder=s['z'], label=s['label'])
            pl.hist(d, bins=np.ptp(d)//1+1, histtype='step', edgecolor=s['c'], zorder=s['z'], label=s['label'], **kwargs)

    if not_accepted or accepted:
        pl.legend()

    #pl.axvline(72, c='k', ls=':', zorder = 2)

    pl.xlabel(_H0_xlabel)
    pl.ylabel(r'Count')

    if accepted or not not_accepted:
        if accepted:
            h = np.array(accepted)
        else:
            h = np.array(accepted + notag)

        hs = np.sort(h)
        l = len(hs)

        m = hs[l * 0.50]
        u = hs[l * (0.50 + 0.341)]
        l = hs[l * (0.50 - 0.341)]

        pl.axvline(m, c='r', ls='-', zorder = 2)
        pl.axvline(u, c='g', ls='-', zorder = 2)
        pl.axvline(l, c='g', ls='-', zorder = 2)

        Log( 'H0_plot: %f %f %f' % (m, u, l) )
        Log( 'H0_plot: %f %f %f' % (m, (u-m), (m-l)) )
    else:
        Log( "H0_plot: No H0 values accepted" )

    pl.xlim(xmin=0)
    pl.xlim(xmax=pl.xlim()[1] + 0.01*(pl.xlim()[1] - pl.xlim()[0]))
    pl.ylim(ymax=pl.ylim()[1] + 0.01*(pl.ylim()[1] - pl.ylim()[0]))

_time_delays_xlabel = r'Time delay (days)'
@command
def time_delays_plot(env, **kwargs):

    models = kwargs.pop('models', env.models)
    obj_index = kwargs.pop('obj_index', 0)
    src_index = kwargs.pop('src_index', 0)
    key = kwargs.pop('key', 'accepted')

    d = defaultdict(list)
    for m in models:
        obj,data = m['obj,data'][obj_index]
        t0 = data['arrival times'][src_index][0]
        for i,t in enumerate(data['arrival times'][src_index][1:]):
            d[i].append( float('%0.6f'%convert('arcsec^2 to days', t-t0, obj.dL, obj.z, data['nu'])) )
            t0 = t

    s = product(range(1,1+len(d)), ['solid', 'dashed', 'dashdot', 'dotted'])
    for k,v in d.iteritems():
        #print 'td plot', k, len(v)
        #print v
        lw,ls = s.next()
        pl.hist(v, bins=25, histtype='step', color='k', ls=ls, lw=lw, label='%s - %s' % (str(k+1),str(k+2)), **kwargs)

    #pl.xlim(xmin=0)
    pl.ylim(ymin=0)
    pl.xlim(xmin=pl.xlim()[0] - 0.01*(pl.xlim()[1] - pl.xlim()[0]))
    pl.legend()

    pl.xlabel(_time_delays_xlabel)
    pl.ylabel(r'Count')


_scale_factor_xlabel = r'Scale factor'
@command
def scale_factor_plot(env, **kwargs):
    _hist(env, 'sigp:scale-factor', xlabel=r'Scale factor')
    return

    models  = kwargs.pop('models', env.models)
    objects = kwargs.pop('objects', None)
    key     = kwargs.pop('key', 'accepted')

    # select a list to append to based on the 'accepted' property.
    l = [[], [], []]
    for m in models:
        # For H0 we only have to look at one model because the others are the same
        obj, data = m['obj,data'][0] 
        l[m.get(key,2)].append(data['sigp:scale-factor'])

    not_accepted, accepted, notag = l

    for d,s in zip(l, _styles):
        if d:
            pl.hist(d, bins=np.ptp(d)//1+1, histtype='step', edgecolor=s['c'], zorder=s['z'], label=s['label'], log=False, **kwargs)

    if not_accepted or accepted:
        pl.legend()

    pl.xlabel(_scale_factor_xlabel)
    pl.ylabel(r'Count')


_chisq_xlabel = r'$\chi^2$'
@command
def chisq_plot(env, **kwargs):
    _hist(env, 'sigp:chisq', xlabel=r'$\chi^2$')
    return

    models = kwargs.pop('models', env.models)
    objects = kwargs.pop('objects', None)
    key = kwargs.pop('key', 'accepted')

    # select a list to append to based on the 'accepted' property.
    l = [[], [], []]
    for m in models:
        # For H0 we only have to look at one model because the others are the same
        obj, data = m['obj,data'][0] 
        l[m.get(key,2)].append(data['sigp:chisq'])

    not_accepted, accepted, notag = l

    for d,s in zip(l, _styles):
        if d:
            pl.hist(d, histtype='step', edgecolor=s['c'], zorder=s['z'], label=s['label'], log=False, **kwargs)

    if not_accepted or accepted:
        pl.legend()

    pl.xlabel(_chisq_xlabel)
    pl.ylabel(r'Count')

@command
def shear_plot(env, **kwargs):

    models = kwargs.pop('models', env.models)
    obj_index = kwargs.pop('obj_index', None)
    src_index = kwargs.pop('src_index', None)
    key = kwargs.pop('key', 'accepted')

    obj_slice = index_to_slice(obj_index)
    src_slice = index_to_slice(src_index)

    s0 = [ [] for o in env.objects ]
    s1 = [ [] for o in env.objects ]
    for mi,m in enumerate(models):
        # For H0 we only have to look at one model because the others are the same
        for oi, [obj,data] in enumerate(m['obj,data'][obj_slice]):
            if not data.has_key('shear'): continue
            #s0[oi].append(90-np.degrees(np.arctan2(*data['shear'])))
            s0[oi].append(data['shear'][0])
            s1[oi].append(data['shear'][1])

            #s0,s1 = data['shear']
            #Log( 'Model %i  Object %i  Shear %.4f %.4f' % (mi, oi, s0,s1) )

    if s0[0]: pl.hist(s0[0], histtype='step', **kwargs)
    if s1[0]: pl.hist(s1[0], histtype='step', **kwargs)

_chi2_xlabel = r'$\ln \chi^2$'
@command
def chi2_plot(env, models, model0, **kwargs):
    v = []
    n_chi2 = 0
    d_chi2 = 0
    for m in models:
        total_chi2 = 0
        for m1,m2 in izip(m['obj,data'], model0['obj,data']):
            obj,data = m1
            obj0,data0 = m2
            mass0 = data0['kappa'] * convert('kappa to Msun/arcsec^2', 1, obj0.dL, data0['nu'])
            mass1 = data['kappa'] * convert('kappa to Msun/arcsec^2', 1, obj.dL, data['nu'])
            n_chi2 += np.sum((mass1 - mass0)**2)
            d_chi2 += np.sum(mass0**2)
        v.append(np.log(n_chi2/d_chi2))
    pl.hist(v, histtype='step', log=False, **kwargs)
    pl.xlabel(_chi2_xlabel)
    pl.ylabel(r'Count')

@command
def glhist(env, data_key, **kwargs):
    _hist(env, data_key, **kwargs)

def _hist(env, data_key, **kwargs):

    models      = kwargs.pop('models', env.models)
    obj_index   = kwargs.pop('obj_index', 0)
    key         = kwargs.pop('key', 'accepted')
    label       = kwargs.pop('label', None)
    color       = kwargs.pop('color', None)
    xlabel      = kwargs.pop('xlabel', data_key)
    ylabel      = kwargs.pop('ylabel', r'Count')
    sigma       = kwargs.pop('sigma', '1sigma')

    # select a list to append to based on the 'accepted' property.
    l = [[], [], []]
    for m in models:
        obj, data = m['obj,data'][obj_index] # For H0 we only have to look at one model because the others are the same
        if data.has_key(data_key):
            l[m.get(key,2)].append(data[data_key])
        #print 'nu', data['nu']
        #l[2].append(data['kappa'][1])

    #print amin(l[2]), amax(l[2])

    not_accepted, accepted, notag = l

    #print 'H0_plot',H0s

    for d,s in zip(l, _styles):
        kw = kwargs.copy()
        if d:
            kw.setdefault('bins', np.ptp(d)//1+1)
            kw.setdefault('histtype', 'step')
            #print len(d), d
            #pl.hist(d, bins=20, histtype='step', edgecolor=s['c'], zorder=s['z'], label=s['label'])
            pl.hist(d, 
                    edgecolor=s['c'] if color is None else color, 
                    zorder=s['z'], 
                    label=s['label'] if label is None else label, 
                    **kwargs)

    if not_accepted or label:
        pl.legend()

    if mark_sigma and (accepted or not not_accepted):
        if accepted:
            h = np.array(accepted)
        else:
            h = np.array(accepted + notag)

        m,u,l = dist_range(h, sigma=sigma)

        pl.axvline(m, c='r', ls='-', zorder = 2)
        pl.axvline(u, c='g', ls='-', zorder = 2)
        pl.axvline(l, c='g', ls='-', zorder = 2)

        Log( '%s: %f %f %f' % (data_key, m, u, l) )
        Log( '%s: %f %f %f' % (data_key, m, (u-m), (m-l)) )
    else:
        Log( "%s: No H0 values accepted" % data_key )

    #pl.axvline(72, c='k', ls=':', zorder = 2)

    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

    pl.xlim(xmax=pl.xlim()[1] + 0.01*(pl.xlim()[1] - pl.xlim()[0]))
    pl.ylim(ymax=pl.ylim()[1] + 0.01*(pl.ylim()[1] - pl.ylim()[0]))
    
    

def iterPrint(val, key='', maxrec=10, d=0, maxlistitems=5):
  '''recusivly prints the attributes of any type 'val' '''

  import types
  if d>=maxrec:
    #print ' |'*d, ' (MAX RECURSION)'
    return
  if d==0: print '---------------------'
  s = ' |'*d + '--> '
  tp = type(val).__name__
  try:
    tp += ' [%i]'%len(val)
  except (TypeError, AttributeError):
    pass
  try:
    tp1 = val.__class__.__name__
    if not type(val).__name__==tp1:
      tp += ' (%s)' % tp1
  except AttributeError:
    pass
  tp = tp if len(tp)<47 else tp[0:47]+'...'
  
  vl = str(val)
  vl = vl if len(vl)<67 else vl[0:67]+'...'
  
  print '%-40s: %-50s %-70s' % (s + key, tp, vl)
  
  if d>maxrec:
    print ' |'*(d+1) + '--> ... (reached max recursion depth)'
  
  elif isinstance(val, (list, tuple)) and len(vl)>67:
    for i in range(len(val) if len(val)<maxlistitems else maxlistitems): #only print the first 20
      iterPrint(val[i], '%s_%03i' % (key,i),maxrec, d+1, maxlistitems)
    if len(val)>=maxlistitems:
      print ' |'*(d+1) + '--> ... (cut of rest of items)'
    
  elif isinstance(val, (type, types.ClassType, types.InstanceType)):
    for nkey, nval in vars(val).items():
      iterPrint(nval, nkey, maxrec, d+1, maxlistitems)

  elif isinstance(val, (dict)):
    for nkey, nval in val.items():
      try:
        iterPrint(nval, nkey, maxrec, d+1, maxlistitems)
      except TypeError: #if key is not a string
        iterPrint(nval, str(nkey), maxrec, d+1, maxlistitems)
        
        
@command
def overlay_input_points(env, model, **kwargs):
  '''adds the input points (min, max, sad, pmass) ontop of existing plot'''
  
  obj_index       = kwargs.pop('obj_index', 0)
  src_index       = kwargs.pop('src_index', 0)
  overlay_ext_pot = kwargs.pop('overlay_ext_pot', True)

  obj, data = model['obj,data'][obj_index]

  if overlay_ext_pot:
    for epot in obj.extra_potentials:
      if isinstance(epot, glass.exmass.PointMass):
        #epot.r #coordinatess as complex
        #epot.name
        #pms.append(epot)
        pl.plot([epot.r.real], [epot.r.imag], 'sy')
  
  for img in obj.sources[0].images:
    #print img, img.parity
    
    #['min', 'sad', 'max', 'unk'].index(parity)
    tp = ['c', 'g', 'r', 'm'][img.parity]
    pl.plot([img.pos.real], [img.pos.imag], 'o'+tp)
  #mark origin
  pl.plot([0], [0], 'or')
  
    

