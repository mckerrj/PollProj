execute "install-nginx" do
  command "apt-get install nginx -y"  
  action :run
end

link "/etc/nginx/sites-enabled/twitter_nginx.conf" do
  to "/home/vagrant/twitter/twitter_nginx.conf"
  action :create
end

if ::File.exists?("/var/run/nginx.pid") 
  execute "nginx-reload" do
    command "nginx -s reload"
    #action :run
  end
else
  execute "nginx-start" do
    command "nginx"
    #action :run
  end
end


