
#Server Install Process (on OpenSUSE)


the particular software packaes presented here are not really in order..

##preparing:

* upgrade: `sudo zypper up`
* install nano: `sudo zypper install nano`
* open firewall for ssh:

    SuSEfirewall2 open EXT TCP ssh
    SuSEfirewall2
    

##Install the message broker: RabbitMQ

    sudo zypper install rabbitmq-server

* enable systemd service: `sudo chkconfig rabbitmq-server on`
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
    rabbitmqctl set_usSuSEfirewall2 open EXT TCP ssh
SuSEfirewall2er_tags lmt monitoring

change psw on the default guest account:

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



## Install Database: MariaDB

* install: `sudo zypper install mariadb`
* start to test: `systemctl start mysql`
* enable at boot `chkconfig mysql on` or newer / better i guess: `systemctl enable mysql.service`
* create directory layout: (is this really useful or needed??) `mysql_install_db`
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

### Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX

since this is a critical part, use the system package manager (auto updates.. logfile location.. secure defaults.. different users..)

    zypper install libevent libevent-devel python-greenlet python-gevent python-gunicorn
    











python-mysql

















