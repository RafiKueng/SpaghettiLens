from fabric.operations import local
from fabric.api import local, settings, abort
from fabric.context_managers import lcd
from fabric.contrib.console import confirm

from datetime import datetime as dt
import os
import hashlib
import gzip

import install.install as i

# makes a fresh install, remote or locally
def install():
  i.install()


# updates an existing install
def update_html(install_dir="./build", htmldir = 'static_html'):
  '''
  combine all vendor js sand css files, (TODO: minimize them) and tag with a file hash
  so they stay the same as long as nothing changed
  
  all lmt files will be tagged with version number and time.
  '''
  install_dir=os.path.realpath(install_dir)
  
  # make sure to have the latest tags
  if confirm("update git tags?"):
    local('git fetch --tags')
  version = local("git describe --abbrev=1 --tags", capture=True)
  time_str = dt.now().strftime("%Y%m%d%H%M")
  v_str = version + "-" + time_str

  if confirm("delete old files?"):
    with settings(warn_only=True):
      local("rm "+os.path.join(install_dir,htmldir,'js','lmt.v*'))
      local("rm "+os.path.join(install_dir,htmldir,'css','lmt.v*'))
  
  print "version string:", v_str
  
  js = {
    'name': 'lmt.'+v_str+'.min.js',
    'root': os.path.join(install_dir,htmldir,'js'),
    }
  js['full'] = os.path.join(js['root'], js['name'])

  css = {
    'name': 'lmt.'+v_str+'.min.css',
    'root': os.path.join(install_dir,htmldir,'css'),
    }
  css['full'] = os.path.join(css['root'], css['name'])

  src = {
    'js': os.path.abspath('./static_html/js'),
    'css': os.path.abspath('./static_html/css'),
    'html': os.path.abspath('./static_html/')
  }



  print 'generating js file:', js['full']
  js_files = [f for f in os.listdir(src['js']) if f.startswith("lmt")
                                                and f.endswith(".js")
                                                and not f=='lmt.js'
                                                and not f=='lmt.settings.js']
  
  if not os.path.isdir(js['root']):
    os.makedirs(js['root'])
  with open(js['full'], 'w') as outfile:
    with open(os.path.join(src['js'], 'lmt.js')) as infile:
      print '  > lmt.js'
      for line in infile:
          outfile.write(line)
    for fname in js_files:
      print '  >',fname
      with open(os.path.join(src['js'], fname)) as infile:
        for line in infile:
          outfile.write(line)
    # write settings
    set = [
      'debug = true;',
      'local = false;',
      'doLog = true;',
      'logToConsole = true;',
      'LMT.com.serverUrl = \'\';',
      'LMT.version = \'%s\'' % version,
      'LMT.build_time = \'%s\'' % time_str,
      'LMT.build = \'%s\'' % v_str,
    ]
    print 'using lmt.settings.js config: (hardcoded)'
    for _ in set: print '  >', _
    outfile.write('\n'+'\n'.join(set))



  vendor_js_files = [f for f in os.listdir(src['js']) if f.startswith("jquery")]
  vendor_js_files.append('canvg.js')
  
  vjshash = "".join([hashlib.sha256(open(os.path.join(src['js'], fname), 'rb').read()).hexdigest()[:4] for fname in vendor_js_files])

  vjs = {
    'name': 'vendor.'+vjshash+'.min.js',
    'root': os.path.join(install_dir,htmldir,'js'),
    }
  vjs['full'] = os.path.join(vjs['root'], vjs['name'])

  if os.path.isfile(vjs['full']):
    print "skipping regeneration of vendor js", vjs['full']
  else:
    print 'generating vendor js file:', vjs['full']
    with open(vjs['full'], 'w') as outfile:
      for fname in vendor_js_files:
        with open(os.path.join(src['js'], fname)) as infile:
          for line in infile:
            outfile.write(line)



  
  print 'generating css file:', css['full']
  css_files = [f for f in os.listdir(src['css']) if f.startswith("lmt") and f.endswith(".css") and not f=='lmt.css']
  
  if not os.path.isdir(css['root']):
    os.makedirs(css['root'])
  with open(css['full'], 'w') as outfile:
    with open(os.path.join(src['css'], 'lmt.css')) as infile:
      for line in infile:
          outfile.write(line)
    for fname in css_files:
      with open(os.path.join(src['css'], fname)) as infile:
        for line in infile:
          outfile.write(line)
  
  



  
  vendor_css_files = [f for f in os.listdir(src['css']) if f.startswith("jquery")]
  vendor_css_files.append('font-awesome.css')

  vcsshash = "".join([hashlib.sha256(open(os.path.join(src['css'], fname), 'rb').read()).hexdigest()[:4] for fname in vendor_css_files])

  vcss = {
    'name': 'vendor.'+vcsshash+'.min.css',
    'root': os.path.join(install_dir,htmldir,'css'),
    }
  vcss['full'] = os.path.join(vcss['root'], vcss['name'])
  
  if os.path.isfile(vcss['full']):
    print "skipping regeneration of vendor css"
  else:
    print 'generating vendor css file:', vcss['full']
    with open(vcss['full'], 'w') as outfile:
      for fname in vendor_css_files:
        with open(os.path.join(src['css'], fname)) as infile:
          for line in infile:
            outfile.write(line)



  bigfiles = [js['full'], vjs['full'], css['full'], vcss['full']]
  for filen in bigfiles:
    if os.path.isfile(filen+'.gz'):
      print "skipping gzip of", filen
    else:
      print "gzip of", filen
      with open(filen, 'r') as inp, gzip.open(filen+'.gz', 'w') as gz:
        gz.write(inp.read())
    

          
  
  csslist = [
    'http://ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/themes/ui-darkness/jquery-ui.css',
    'css/'+vcss['name'],
    'css/'+css['name']
  ]
  
  jslist = [
    'http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.js',
    'http://ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.js',
    'http://canvg.googlecode.com/svn/trunk/rgbcolor.js',
    'http://canvg.googlecode.com/svn/trunk/StackBlur.js',
    'js/'+vjs['name'],
    'js/'+js['name']
  ]
  
  csstags = ''
  for url in csslist:
    csstags += '  <link rel="stylesheet" href="%s" />\n' % url

  jstags = ''
  for url in jslist:
    jstags += '  <script src="%s"></script>\n' % url
  
  lmtdir = os.path.join(install_dir,htmldir,'lmt.html')
  
  print 'wrinting lmt.html', lmtdir
  with open(lmtdir, 'w') as out:
    with open(os.path.join(src['html'],'html.tmpl'), 'r') as head:
      with open(os.path.join(src['html'],'body.php'), 'r') as body:
        str = head.read()
        str = str.format(css=csstags,
                         js=jstags,
                         body=body.read())
        out.write(str)
  






# restarts any server
def restart():
  pass




def test():
  from fabric.contrib.files import exists as fe
  from fabric.contrib.files import cd

  from fabric.api import env as e
  from install.utils import _cd, _fe, _s
  
  conf = {}
  conf['INSTALL_DIR'] =  '/srv/lmt'
  conf['WORKER_DIR'] = '/worker'
  
  with _cd(conf['INSTALL_DIR']):
    print conf['INSTALL_DIR']
    print conf['WORKER_DIR']+"/run_glass"
    print _fe(conf['INSTALL_DIR']+conf['WORKER_DIR']+"/run_glass")
