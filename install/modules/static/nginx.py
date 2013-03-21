import os, StringIO
from install.utils import path

from fabric.api import env
from fabric.operations import put
from fabric.utils import puts


def about():
  return "fast production nginx http static file server"


def neededVars():
  return (
    ("PUBLIC_URL", "url to reach the server from the internet", "http://localhost"),
    ("PUBLIC_PORT", "port to the internet for the webserver", "80"),
    ("ROOT_DIR", "root directory of install", os.getcwd()),
    ("HTML_DIR", "directory of static html files (sub of root dir)", "/static_html"),
    ("DJANGO_STATIC", "directory of static django files (sub of root dir)", "/backend/static"),
    ("MEDIA_FILES", "direcory of generrated images", "/tmp_media"),
    ("URL_DJANGO_SERVER", "(internal?) url for redirects to django server, WITH port", "http://localhost:8000"),
    ("RESULTPATH", "(virtual) path where the client gets the results from", "/results")
  )



def beforeInstallCmds():
  def fnc():
    # add rabbitmq to sources
    puts("echo deb http://www.rabbitmq.com/debian/ testing main >> /etc/apt/sources.list")
    puts("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
    puts("apt-key add rabbitmq-signing-key-public.asc")
    puts("rm rabbitmq-signing-key-public.asc")
    puts("apt-get update")
    
  return (fnc,)


def getPackagesToInstall():
  return ('nginx',)


def setup():
  filename = _generateConfigFile()
  puts("--- nginx temp config file: " + filename)
  
  puts('put(filename, "/etc/nginx/sites-available/lmt.conf")') #local
  puts("ln -s /etc/nginx/sites-available/lmt.conf /etc/nginx/sites-enabled") #remote
  puts("/etc/init.d/nginx reload") #remote
  
  puts("os.remove(filename)") #local


def test():
  # enable the default site and check if it answers
  puts("ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled")
  puts("/etc/init.d/nginx restart")
  puts("wget %(PUBLIC_URL)s:%(PUBLIC_PORT)")
  puts("check if index.html exists and has the right contens")
  puts("del index.html")
  puts("rm /etc/nginx/sites-enabled/default")
  puts("/etc/init.d/nginx restart")


  
def _generateConfigFile():
  env["PATH_FULL_HTML"] = path(env.ROOT_DIR, env.HTML_DIR)
  env["PATH_FULL_DJANGOSTATIC"] = path(env.ROOT_DIR, env.DJANGO_STATIC)
  
  tempfilestr = path(env.TEMP, "nginx.conf")
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