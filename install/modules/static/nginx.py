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
    ("MEDIA_FILES", "direcory of generrated images (relative)", "/tmp_media"),
    ("URL_DJANGO_SERVER", "(internal?) url for redirects to django server, WITH port", "http://localhost:8000"),
    ("RESULTPATH", "(virtual) path where the client gets the results from", "/results")
  )


#################################################################################  


def beforeInstallCmds():
  pass

  


def installPackages():
  package_install('nginx')



def setup():
  filename = _generateConfigFile()
  puts("--- nginx temp config file: " + filename)
  
  _p(filename, "/etc/nginx/sites-available/lmt.conf", use_sudo=True)  #local
  _s("ln -f -s /etc/nginx/sites-available/lmt.conf /etc/nginx/sites-enabled") #remote
  _s("/etc/init.d/nginx reload") #remote
  
  _l("os.remove(filename)") #local







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




#################################################################################  


  
def _generateConfigFile():
  env["PATH_FULL_HTML"] = path(env.ROOT_DIR, env.HTML_DIR)
  env["PATH_FULL_DJANGOSTATIC"] = path(env.ROOT_DIR, env.DJANGO_STATIC)
  
  
  tempfilestr = utils.path(env.TEMP, "nginx.conf")
  tempfile = open(tempfilestr, 'wb')
  
  cfg = """
server {
  listen %(PUBLIC_PORT)s; ## listen for ipv4; this line is default and implied
  listen   [::]:%(PUBLIC_PORT)s default ipv6only=on; ## listen for ipv6

  root %(ROOT_DIR)s;
  index index.php index.html index.htm;

  # Make site accessible from http://localhost/
  server_name _;

  location /favicon.ico { alias %(PATH_FULL_HTML)s/favicon.ico; }

  # ressource folders for the static content
  location /js { autoindex on; alias %(PATH_FULL_HTML)s/js/; }
  location /css { alias %(PATH_FULL_HTML)s/css/; }
  location /img { alias %(PATH_FULL_HTML)s/img/; }
  location /font { alias %(PATH_FULL_HTML)s/font/; }
  location /i18n { alias %(PATH_FULL_HTML)s/i18n/; }

  # django static files
  location %(DJANGO_STATIC)s {
    autoindex on;
    alias %(PATH_FULL_DJANGOSTATIC)s/;
  }
  
  #check if this mediafile already exists, then serve it directly, otherwise let django create it
  location ~ ^%(RESULTPATH)s/(?<id>\d+)/(?<file>.+\..+)$ {
    try_files %(MEDIA_FILES)s/$id/$file @tmpmedia;
  }

  location @tmpmedia {
    proxy_pass_header Server;
    proxy_set_header Host $http_host;
    proxy_redirect off;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Scheme $scheme;
    proxy_connect_timeout 10;
    proxy_read_timeout 10;
    proxy_pass %(URL_DJANGO_SERVER)s;
  }
  

  # all the dynamic rest goes to gunicorn server - django
  location / {
    proxy_pass_header Server;
    proxy_set_header Host $http_host;
    proxy_redirect off;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Scheme $scheme;
    proxy_connect_timeout 10;
    proxy_read_timeout 10;
    proxy_pass %(URL_DJANGO_SERVER)s;
  }
}
""" % env

  tempfile.write(cfg)
  tempfile.close()
  return tempfilestr