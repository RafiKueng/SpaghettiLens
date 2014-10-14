import csv
import numpy as np
#from scipy.optimize import curve_fit


def filt(data, cond, column):
  f = data[:,column]==cond
  return data[f]


def read_csv():
  # 0: mite (8/3)
  # 1: anker (4/2)
  # 2: siamese (2/2)
  machine=[[], [], [], []]


  with open('ext_time.csv', 'r') as csvfile:
    csvf = csv.reader(csvfile)
    csvf.next()
    for line in csvf:
      
      if int(line[1])==0: continue
      
      if   int(line[4]) == 8 and int(line[5]) == 3: _m = 0
      elif int(line[4]) == 4 and int(line[5]) == 2: _m = 1
      elif int(line[4]) == 2 and int(line[5]) == 2: _m = 2
      else: _m=3

      pixrad = np.int(line[2])
      npix = np.int(line[3])
      burninlen = np.int(line[6])
      nmodels = np.int(line[7])
      t_init = np.float(line[8])
      t_ev = np.float(line[9])
      t_burnin = np.float(line[10])
      t_model = np.float(line[11])
      t_thread = np.float(line[12])
      t_wallclock = np.float(line[13])
      
      dt_burnin = np.float(line[14])
      dt_model = np.float(line[15])
     
      machine[_m].append([pixrad,npix,burninlen,nmodels,t_init,t_ev,t_burnin,t_model,t_thread,t_wallclock,dt_burnin,dt_model])
      
  return machine

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
  
  
data = AttrDict()

data.m = read_csv()

data.mite = np.array(data.m[0])
data.anker = np.array(data.m[1])
data.siamese = np.array(data.m[2])

data.header = ['pixrad','npix','burninlen','nmodels','t_init','t_ev',
  't_burnin','t_model','t_thread','t_wallclock','dt_burnin','dt_model']
h = AttrDict()
for i,j in enumerate(data.header):
  h[j]=i
  h[i]=j
