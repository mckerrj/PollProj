directory "/root/.ssh" do
  owner "root"
  group "root"
  mode 0600
  action :create
end

file "/home/vagrant/.ssh/id_rsa_twitterapp" do
  owner 'vagrant'
  group 'vagrant'
  mode 0600
  content ::File.open("/vagrant/.chef/id_rsa_twitterapp").read
  action :create
end

file "/home/vagrant/.ssh/config" do
  owner 'vagrant'
  group 'vagrant'
  mode 0600
  content ::File.open("/vagrant/.chef/config").read
  action :create
end

file "/root/.ssh/config" do
  owner 'root'
  group 'root'
  mode 0600
  content ::File.open("/vagrant/.chef/config").read
  action :create
end

file "/root/.ssh/id_rsa_twitterapp" do
  owner 'root'
  group 'root'
  mode 0600
  content ::File.open("/vagrant/.chef/id_rsa_twitterapp").read
  action :create
end

git "/home/vagrant/twitter/" do
  repository "git@github.com:mckerrj/TwitterApp.git"
  reference "master"
  action :checkout
end
