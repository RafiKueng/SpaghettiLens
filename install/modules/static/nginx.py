import os, StringIO
from install.utils import _r, _s, _p, _l, _fe
import install.utils as utils

from install.package import package_install

from fabric.api import *
from fabric.colors import *

conf = env.conf

#################################################################################  


def about():
  return "fast production nginx http static file server"


def neededVars():
  return (
    ("PUBLIC_URL", "url to reach the server from the internet", "http://localhost"),
    ("PUBLIC_PORT", "port to the internet for the webserver", "80"),
    ("INSTALL_DIR", "root directory of install", os.getcwd()),
    ("HTML_DIR", "directory of static html files (relative to install)", "/static_html"),
    ("DJANGO_STATIC", "directory of static django files (relative)", "/backend/static"),
    ("DJANGO_STATIC_URL", "virtual static django files url, url prefix for static fiels (relative)", "/static_django/"),
    ("MEDIA_FILES", "direcory of generrated images (relative)", "/tmp_media"),
    ("DJANGO_SERVER_HOST", "(internal?) url for redirects to django server", "http://localhost"),
    ("DJANGO_SERVER_PORT", "(internal?) port to django server", "8000"),
    ("RESULTPATH", "(virtual) path where the client gets the results from", "/results")
  )


#################################################################################  


def beforeInstallCmds():
  pass

  


def installPackages():
  package_install('nginx')





def testInstall():
  # enable the default site and check if it answers
  _s("ln -s -f /etc/nginx/sites-available/default /etc/nginx/sites-enabled")
  _s("/etc/init.d/nginx restart")
  _r("wget %(PUBLIC_URL)s:%(PUBLIC_PORT)s" % conf)
  test = _fe("index.html")
  with settings(warn_only=True):
    resp = _r("grep 'Welcome to nginx' index.html")
    test = test and resp.return_code
  if not test: warn(yellow('nginx is not running properly'))
  _r("rm index.html")
  _s("rm /etc/nginx/sites-enabled/default")
  _s("/etc/init.d/nginx restart")




def setup():
  file = _generateConfigFile()
  puts("--- nginx temp config file: ")
  print file.getvalue()
  
  _p(file, "/etc/nginx/sites-available/lmt.conf", use_sudo=True)  #local
  _s("ln -f -s /etc/nginx/sites-available/lmt.conf /etc/nginx/sites-enabled") #remote
  _s("/etc/init.d/nginx reload") #remote
  


  # copy html files
  _s("cp -f -R %(REPRO_DIR)s/static_html %(INSTALL_DIR)s%(HTML_DIR)s" % conf)
  file = _generateHTMLSettings()
  _p(file, "%(INSTALL_DIR)s%(HTML_DIR)s/js/lmt.settings.js" % conf, use_sudo=True)  #local
  _s("chown -R %(SYS_USER)s:%(SYS_GROUP)s %(INSTALL_DIR)s/*" % conf)
  _s("chmod -R 644 %(INSTALL_DIR)s%(HTML_DIR)s/*" % conf)  








#################################################################################  


  
def _generateConfigFile():
  print "in _gen"
  env["PATH_FULL_HTML"] = env.INSTALL_DIR + env.HTML_DIR
  env["PATH_FULL_DJANGOSTATIC"] = env.INSTALL_DIR + env.DJANGO_STATIC
  env["URL_DJANGO_SERVER"] = env.DJANGO_SERVER_HOST + ':' + env.DJANGO_SERVER_PORT
  
  
  cfg = """
server {
  listen %(PUBLIC_PORT)s; ## listen for ipv4; this line is default and implied
  listen   [::]:%(PUBLIC_PORT)s default ipv6only=on; ## listen for ipv6

  root %(PATH_FULL_HTML)s;
  index index.php index.html index.htm;

  # Make site accessible from http://localhost/
  server_name _;

  #proxy settings
  proxy_pass_header Server;
  proxy_set_header Host $http_host;
  proxy_redirect off;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Scheme $scheme;
  proxy_connect_timeout 10;
  proxy_read_timeout 10;

  access_log %(INSTALL_DIR)s%(LOG_DIR)s/nginx_access.log;
  error_log %(INSTALL_DIR)s%(LOG_DIR)s/nginx_error.log;

  # django static files
  location %(DJANGO_STATIC_URL)s {
    autoindex on;
    alias %(PATH_FULL_DJANGOSTATIC)s/;
  }
  
  location ^~ /admin/ {proxy_pass %(URL_DJANGO_SERVER)s;}
  location ^~ /get_initdata/ {proxy_pass %(URL_DJANGO_SERVER)s;}
  location ^~ /get_modeldata/ {proxy_pass %(URL_DJANGO_SERVER)s;}
  location ^~ /save_model/ {proxy_pass %(URL_DJANGO_SERVER)s;}
  location ^~ /load_model/ {proxy_pass %(URL_DJANGO_SERVER)s;}

  #check if this mediafile already exists, then serve it directly, otherwise let django create it
  location ~ ^%(RESULTPATH)s/(?<id>\d+)/(?<file>.+\..+)$ {
    try_files %(MEDIA_FILES)s/$id/$file @tmpmedia;
  }

  location @tmpmedia {
    proxy_pass %(URL_DJANGO_SERVER)s;
  }
}
""" % env
  
  return StringIO.StringIO(cfg)





def _generateHTMLSettings():
  #create the js/lmt.settings.js file
  set = '''
  LMT.com.serverUrl = "";
  '''
  
  return StringIO.StringIO(set)









