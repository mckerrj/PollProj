## Nginx and UWSGI config for the vagrant box

- Here is a quick lowdown on seting up a simple NGinx proxy and UWSGI for this app.  This is by no means comprehensive, but a good starter for understanding it.
- We use NGinx for Proxying and UWSGI for production DJango.
- Since it's pretty straighforward, I'll post the whole thing as code here.
  - NGinx gets installed by chef.
  - UWSGI also gets installed by chef.
  - the <code>python manage.py collectstatic</code> puts any static files (including the admin app) where we want them as set in 'settings.py'
  - And then we have an [nginx.conf](https://github.com/mckerrj/TwitterApp/blob/master/twitter_nginx.conf) type file to connect it up
  ```
    # twitter_nginx.conf

    # the upstream component nginx needs to connect to
    upstream django {
         server unix:///var/run/twitter.sock; # for a file socket
        #server 192.168.33.10:8001 ; # for a web port socket (we'll use this first)
    }

    # configuration of the server
    server {
        # the port your site will be served on
        listen      80;
        # the domain name it will serve for
        server_name 192.168.33.10; # substitute your machine's IP address or FQDN
        charset     utf-8;

        # Finally, send all non-media requests to the Django server.
        location / {
            uwsgi_pass  django;
            include     /home/vagrant/twitter/uwsgi_params; # the uwsgi_params file you installed
        }

        location /static/ { # STATIC_URL
            alias /static/; # STATIC_ROOT
            expires 30d;
       }
    }
  ```

  - This sets up unix sockets to handle the connection to Django.
  - The <code>server</code> block sets
    - The port
    - IP
    - Character encoding
    - Stuff for uwsgi
    - and maps the location of the static files.