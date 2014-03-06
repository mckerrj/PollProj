# Cookbook Name:: twitterapp
# Recipe:: mysql-server-setup

mysql_connection_info = {
  :host     => 'localhost',
  :username => 'root',
  :password => node['mysql']['server_root_password']
}

mysql_database 'twitter' do
  connection mysql_connection_info
  action :create
end

mysql_database 'test_twitter' do
  connection mysql_connection_info
  action :create
end

#Commented since following grant command will create and grant.  Kept for now as comment
#database_user 'twitter' do
#  connection mysql_connection_info
#  password   'twitter314'
#  provider   Chef::Provider::Database::MysqlUser
#  action     :create
#end

# Command will both create the user AND grant.
mysql_database_user 'twitter' do
  connection    mysql_connection_info
  password      'twitter314'
  database_name 'twitter'
  host          '%'
  privileges    [:'select',:'update',:'insert',:'delete',:'execute',:'create',:'alter',:'references',:'index',:'create view',:'create routine',:'alter routine',:'drop',:'trigger',:'create temporary tables',:'lock tables']
  action        :grant
end

mysql_database_user 'twitter' do
  connection    mysql_connection_info
  password      'twitter314'
  database_name 'test_twitter'
  host          '%'
  privileges    [:'select',:'update',:'insert',:'delete',:'execute',:'create',:'alter',:'references',:'index',:'create view',:'create routine',:'alter routine',:'drop',:'trigger',:'create temporary tables',:'lock tables']
  action        :grant
end


template "/etc/mysql/my.cnf" do
  owner "root"
  group "root"
  mode "0600"
  notifies :restart, 'service[mysql]'
end

service "mysql" do
  provider Chef::Provider::Service::Upstart
  supports :status => true, :restart => true
  action [:start]
end

