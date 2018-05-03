
#Server Install Process (on OpenSUSE)


the particular software packaes presented here are not really in order..


the real order should be:

1. databases
2. broker
3. python stuff (virtualenv with np, sp, mpl; django; celery)
4. nginx
    
and test in this order..

##preparing:

* upgrade: `sudo zypper up`
* install nano: `sudo zypper install nano`
* open firewall for ssh:

    SuSEfirewall2 open EXT TCP ssh
    SuSEfirewall2
    
* no need for gui: `ln -sf /usr/lib/systemd/system/runlevel3.target /etc/systemd/system/default.target`

##Install the message broker: RabbitMQ

    sudo zypper install rabbitmq-server

* enable systemd service: `systemctl enable rabbitmq-server`
* make sure the hostname is set and assigned correctly: /etc/hosts   127.0.0.1   localhost hostname
* start the server: `systemctl start rabbitmq-server`
* check if running `systemctl | grep rabbit`
* see if the ctl bin works: `rabbitmqctl stop'
 
By default, the server is run as user `rabbitmq`. Its config file is in `/etc/rabbitmq/rabbitmq.config`. but doesn't exist by default (and usually no further configs are needed. otherwise check http://www.rabbitmq.com/configure.html#configuration-file)

### management plugin
* `sudo zypper install rabbitmq-server-plugins`
* `rabbitmq-plugins enable rabbitmq_management`
* `systemctl start rabbitmq-server.service`

then check the interface (http://localhost:15672)
If it failes, check firewall `systemctl restart SuSEfirewall2`

* maybe fix  it: `echo 'FW_SERVICES_EXT_TCP="15672"' > /etc/sysconfig/SuSEfirewall2`

### Setup Users and vHosts

    rabbitmqctl add_user lmt password
    rabbitmqctl add_vhost lmt_vhost
    rabbitmqctl set_permissions -p lmt_vhost lmt ".*" ".*" ".*"
    rabbitmqctl set_user_tags lmt monitoring

change psw on the default guest account (will not be used):

    # rabbitmqctl clear_password guest
    rabbitmqctl change_password guest password


### Config file

It could look something like this: (not tested nor used atm...)

    [
      {rabbit,                    [ {tcp_listeners,               [5672]},
                                    {collect_statistics_interval, 10000} ] },
      {rabbitmq_management,       [
                                    {http_log_dir,          "/tmp/rabbit-mgmt"}
                                    {listener,              [{port, 15672]}
                                  ]
      },
    ].




## Install NoSQL database: CouchDB

> OLD STUFF
>    sudo zypper in couchdb # the default repro version is broken!
>    
>    http://software.opensuse.org/download.html?project=home%3AZaWertun%3Adb&package=couchdb
>    
>    zypper addrepo http://download.opensuse.org/repositories/home:ZaWertun:db/openSUSE_13.1/home:ZaWertun:db.repo
>    zypper refresh
>    zypper install couchdb erlang
 
The versions in the repro of couchdb (1.3) and erlang (16) are NOT compatible! Thats why you should use:

    rpm -i http://download.opensuse.org/repositories/server:/database/openSUSE_13.1/x86_64/erlang-17.3-3.1.x86_64.rpm http://download.opensuse.org/repositories/server:/database/openSUSE_13.1/x86_64/erlang-epmd-17.3-3.1.x86_64.rpm
    rpm -i http://download.opensuse.org/repositories/server:/database/openSUSE_13.1/x86_64/couchdb-1.6.1-45.1.x86_64.rpm 
    
DONT start the command line version as root: `couchdb`. This will mess up all the rights.. After install, directly start:
    
    systemctl enable couchdb
    systemctl start couchdb
    
make sure to install the erlang version from the repro, not from opensuse.


* create database: `curl -X PUT http://127.0.0.1:5984/spaghettilens`
* check the result: `curl -X GET http://127.0.0.1:5984/_all_dbs`
* use the webui: http://127.0.0.1:5984/_utils/

* after you installed all the python stuff, we need the py bindings: `pip install couchdbkit`. see below

edit config `/etc/couchdb/local.ini`:
* allow access from lan: `bind_address = 0.0.0.0`
* create an admin under `[admin]` : `admin = password`
* create an user under `[admin]` : `spaghetti_user = password` #

enable ssl so the psw will not be transmitted in plain text! http://wiki.apache.org/couchdb/How_to_enable_SSL

ALTERNATIVE:
bind to 127.0.0.1 only and let clients use ssh. easier and more secure..



## Install SQL Database: MariaDB

* install: `sudo zypper install mariadb`
* start to test: `systemctl start mysql`
* enable at boot `chkconfig mysql on` or newer / better i guess: `systemctl enable mysql.service`
* create directory layout: (is this really useful or needed?? I don't think so) `mysql_install_db`
* secure the install: `mysql_secure_installation`

###Create user, DB and allow lan access:

* `mysql -u root -p`
* `CREATE DATABASE new_database;` 
* `USE spaghettilens;`
* `GRANT ALL PRIVILEGES ON spaghettilens.* TO 'lmt'@'192.168.100.%' IDENTIFIED BY 'password' WITH GRANT OPTION;`
* `exit`


> other commands to create user... (not used)
> 
> * `CREATE USER 'lmt'@'localhost' IDENTIFIED BY 'virt_psw';`
> * `grant CREATE, ALTER, DELETE, INSERT, SELECT, UPDATE, LOCK TABLES on spaghettilens.* to 'lmt'@'localhost';`
> * `GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.100.%' IDENTIFIED BY 'my-new-password' WITH GRANT OPTION;`
    

## Install webserver: nginx

### Basic install

* install: `zypper install nginx`
* start: `systemctl start nginx.service`
* make autostart on reboot: `systemctl enable nginx.service`

### Configuration

increase nr of processses according to cpu count:

    nano /etc/nginx/nginx.conf
    ...
    worker_processes 4;
    


since I like the debian way of handling vhosts, implement the same here (are there any draw backs?):

    cd /etc/nginx
    mkdir sites-available
    mkdir sites-enabled
    
* remove all `server {...}` sections from `nginx.conf`.
* change the line `include vhosts.d/*.conf;` to `include sites-enabled/*.conf;` (or add it, maybe software automatically installs into `vhosts.d` ???)
* `cd sites-available`
* create a default page: `nano default.conf`

    server {
        listen       80;
        server_name  localhost;
    
        #charset koi8-r;
    
        #access_log  /var/log/nginx/host.access.log  main;
    
        location / {
            root   /srv/www/default/;
            index  index.html index.htm;
        }
    
        #error_page  404              /404.html;
    
        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /srv/www/htdocs/;
        }
    
        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        location ~ \.php$ {
            root           /srv/www/htdocs/;
            fastcgi_pass   127.0.0.1:9000; 
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


* enable the deault page: `cd ../sites-enabled` and `ln -s ../sites-available/default.conf`
* create a page `echo '<html><body><h1>Welcome to my website!</h1></body></html>' >> /srv/www/htdocs/index.html`
* restart 'systemctl restart nginx.service'

* adjust firewall (maybe its already enabled): `echo 'FW_CONFIGURATIONS_EXT="apache2"' >> /etc/sysconfig/SuSEfirewall2`
* restart to take effect: `systemctl restart SuSEfirewall2.service`

* test locally: `lynx localhost` and remote: `firefox 192.168.100.2`

### get php

    zypper in php5-fpm
    cp /etc/php5/fpm/php-fpm.conf.default /etc/php5/fpm/php-fpm.conf
    nano /etc/php5/fpm/php-fpm.conf

#### changes to the config:

    ; Unix user/group of processes
    ; Note: The user is mandatory. If the group is not set, the default user's group
    ;       will be used.
    user = nginx
    group = nginx
    ...
    error_log = /var/log/php-fpm.log
    ...
    listen.allowed_clients = 127.0.0.1
    

then there is no php.ini config. copy one `cp /etc/php5/cli/php.ini /etc/php5/fpm/`. 
You can edit it: `nano /etc/php5/fpm/php.ini` but it seems to be ok with default values.
(maybe need to fix `cgi.fix_pathinfo=0` or change scripts..)

enable and start up:

    systemctl start php-fpm.service
    systemctl enable php-fpm.service

#### and test php setup:

edit the default / testing page () and add / uncomment:

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    location ~ \.php$ {
        root           /srv/www/htdocs/;
        fastcgi_pass   127.0.0.1:9000; 
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include        fastcgi_params;
    }

then do:

    `echo '<?php phpinfo(); ?>' >> /srv/www/htdocs/phptest.php`
    systemctl restart nginx.service
    lynx localhost/phptest.php



### get phpmyadmin (might be handy at some point)

no, learn the cli mysql thinggy.. more secure and stuff..






## Get all the Python stuff

### Create the VirtualEnv

install virtualenv:

    sudo zypper install python-virtualenv
    
and dependencies:
    
    sudo zypper install libmysqlclient-devel
    
create a virtualenv and install all required python modules locally:

    sudo mkdir -p /srv/www/webapps
    sudo chown rafik webapps
    mkdir -p /srv/www/webapps/spaghettilens
    cd /srv/www/webapps/spaghettilens
    virtualenv .
    source bin/activate
    pip install ipython MySQL-python couchdbkit
    pip install numpy scipy matplotlib
    pip install django Celery django-celery django-lazysignup flower
    
    
    




### Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX



> OLD: I prefer a local install now because of simplicity..

> since this is a critical part, use the system package manager (auto updates.. logfile location.. secure defaults.. different users..)

>    zypper install libevent libevent-devel python-greenlet python-gevent python-gunicorn
    
> depending on the start up method, use supervisord or systemd. see here for scripts: http://gunicorn-docs.readthedocs.org/en/latest/deploy.html I need to be able to reastart this process with my local user rights!

get requirements:

    sudo zypper install libevent libevent-devel python-devel
    
install in virtualenv:

    pip install greenlet gevent gunicorn setproctitle
    # setproctitle used for --name arguemnt to have any effect


either start gunicorn with supervisor (DONT):


http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/

* /etc/supervisor/conf.d/hello.conf

    [program:spaghettilens]
    command = /webapps/hello_django/bin/gunicorn_start                    ; Command to start app
    user = hello                                                          ; User to run as
    stdout_logfile = /webapps/hello_django/logs/gunicorn_supervisor.log   ; Where to write log messages
    redirect_stderr = true  

* /webapps/hello_django/bin/gunicorn_start 

    #!/bin/bash
     
    NAME="hello_app" # Name of the application
    DJANGODIR=/webapps/hello_django/hello # Django project directory
    SOCKFILE=/webapps/hello_django/run/gunicorn.sock # we will communicte using this unix socket
    USER=hello # the user to run as
    GROUP=webapps # the group to run as
    NUM_WORKERS=3 # how many worker processes should Gunicorn spawn
    DJANGO_SETTINGS_MODULE=hello.settings # which settings file should Django use
    DJANGO_WSGI_MODULE=hello.wsgi # WSGI module name
     
    echo "Starting $NAME as `whoami`"
     
    # Activate the virtual environment
    cd $DJANGODIR
    source ../bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH
     
    # Create the run directory if it doesn't exist
    RUNDIR=$(dirname $SOCKFILE)
    test -d $RUNDIR || mkdir -p $RUNDIR
     
    # Start your Django Unicorn
    # Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
    exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --bind=unix:$SOCKFILE \
    --log-level=debug \
    --log-file=-


or use systemd: (WE WANT THIS)

http://gunicorn-docs.readthedocs.org/en/latest/deploy.html

* gunicorn.service

    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target
    
    [Service]
    PIDFile=/run/gunicorn/pid
    User=someuser
    Group=someuser
    WorkingDirectory=/home/someuser
    ExecStart=/home/someuser/gunicorn/bin/gunicorn --pid /run/gunicorn/pid test:app
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s TERM $MAINPID
    PrivateTmp=true
    
    [Install]
    WantedBy=multi-user.target
    
* gunicorn.socket:

    [Unit]
    Description=gunicorn socket
    
    [Socket]
    ListenStream=/run/gunicorn/socket
    ListenStream=0.0.0.0:9000
    ListenStream=[::]:8000
    
    [Install]
    WantedBy=sockets.target

OFC this needs to be modified first...
Don't forget to give the user the right to `sudo systemctl [start|stop|stauts|restart|] gunicorn.service
maybe rename the file to something more clear: `spaghettilens-gunicorn.service`


## get the webapp itself

`git clone from_bla into_bla`


## END

the basic dir structre should look like this at the end:

    /webapps/
    ├── spaghettilens               <= virtualenv for the application 
    │   ├── bin
    │   │   ├── activate
    │   │   ├── gunicorn            <= app's gunicorn
    │   │   ├── gunicorn_start      <= app's gunicorn start script
    │   │   ├── python      
    │   │   ├── celery      
    │   │   ├── flower
    │   │   └── ...
    │   ├── lmt                     <= app's Django project directory
    │   │   ├── api
    │   │   │   ├── __init__.py
    │   │   │   ├── settings.py     <= .settings - settings module Gunicorn will use
    │   │   │   ├── urls.py
    │   │   │   └── wsgi.py         <= hello.wsgi - WSGI module Gunicorn will use
    │   │   └ manage.py
    │   ├── logs                    <= app's logs will be saved here
    │   ├── media
    │   ├── run                     <= Gunicorn's socket file will be placed here
    │   ├── static
    │   ├── include
    │   │   └── python2.7           -> /usr/include/python2.7
    │   ├── lib
    │   │   └── python2.7
    │   ├── lib64                   -> /webapps/hello_django/lib
    │   ├── logs                    <= Application logs directory
    │   │   ├── gunicorn_supervisor.log
    │   │   ├── nginx-access.log
    │   │   └── nginx-error.log
    │   ├── media                   <= User uploaded files folder
    │   ├── run
    │   │   └── gunicorn.sock 
    │   └── static                  <= Collect and serve static files from here
    └── some_other_app              <= analogous virtualenv for the another app
        ├── ...




# Notes
## Firewall / open ports

    Local / machine access (for security reason use ssh tunneling?)
        8001    http    flower (monitoring celery, use 8090)
        9000    cgi     php5-fpm
        8001            gunicorn
        15672   http    rabbitmq management (change to 8091)
                        CouchDB
    
    Lan access:
        ?       ?       some way to store binary files in the system (ssh?)
        3306    mysql   MariaDB
        5672    amqp    RabbitMQ
        5984    http    CouchDB API

    Internet Access:
        22      ssh
        80      http    nginx



## Logrotate

Dont forget about logrotate!












