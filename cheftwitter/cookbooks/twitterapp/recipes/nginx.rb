execute "install-nginx" do
  command "apt-get install nginx -y"  
  action :run
end

#execute "link-twitter-to-nginx" do
  #not_if {  ::File.exists?( "/home/vagrant/twitter/twitter_nginx.conf") } 
#  command "ln -s /home/vagrant/twitter/twitter_nginx.conf /etc/nginx/sites-enabled/"
#  action :run
#end

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



#execute "start-nginx" do
#  command "nginx"
#  action :run
#end

