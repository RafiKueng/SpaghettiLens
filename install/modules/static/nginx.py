import os, StringIO
from fabric.operations import put

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
    ("URL_DJANGO_SERVER", "(internal?) url for redirects to django server", "localhost:8000"),
  )



def beforePackageInstall():
  return (
    # add rabbitmq to sources
    ("echo deb http://www.rabbitmq.com/debian/ testing main >> /etc/apt/sources.list"),
    ("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc"),
    ("apt-key add rabbitmq-signing-key-public.asc"),
    ("rm rabbitmq-signing-key-public.asc"),
    ("apt-get update"),
  )


def getPackagesToInstall():
  return ('nginx',)

def setup():
  put(StringIO(_generateConfigFile() %
               ("")),
      "/etc/nginx/sites-available/name")
  puts("ln -s /etc/nginx/sites-available/name /etc/nginx/sites-enabled")
  




  
def _generateConfigFile():
  cfg = """
server {
  listen   8080; ## listen for ipv4; this line is default and implied
  listen   [::]:8080 default ipv6only=on; ## listen for ipv6

  root /srv/lmt;
  index index.php index.html index.htm;

  # Make site accessible from http://localhost/
  server_name _; #rk-dev.no-ip.org *.rk-dev.no-ip.org localhost;

  location /favicon.ico { alias /srv/lmt/static_html/favicon.ico; }

  # ressource folders for the static content
  location /js { autoindex on; alias /srv/lmt/static_html/js/; }
  location /css { alias /srv/lmt/static_html/css/; }
  location /img { alias /srv/lmt/static_html/img/; }
  location /font { alias /srv/lmt/static_html/font/; }
  location /i18n { alias /srv/lmt/static_html/i18n/; }

  # django static files
  location /static_django {
    autoindex on;
    alias /srv/lmt/backend/static/;
  }
  
  #check if this mediafile already exists, then serve it directly, otherwise let django create it
  location ~ ^/result/(?<id>\d+)/(?<file>.+\..+)$ {
    try_files /tmp_media/$id/$file @tmpmedia;
  }

  location @tmpmedia {
    proxy_pass_header Server;
    proxy_set_header Host $http_host;
    proxy_redirect off;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Scheme $scheme;
    proxy_connect_timeout 10;
    proxy_read_timeout 10;
    proxy_pass http://localhost:8001;
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
    proxy_pass http://localhost:8001/;
  }
}
"""
  return cfg