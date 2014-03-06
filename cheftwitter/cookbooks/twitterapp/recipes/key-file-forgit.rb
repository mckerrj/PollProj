unless Chef::Config[:solo]
    secret = Chef::EncryptedDataBagItem.load_secret("/vagrant/.chef/encrypted_data_bag_secret")
    keys = Chef::EncryptedDataBagItem.load('twitter_deploy_key', 'mykeys', secret)
end

directory ::File.join('/home/vagrant/', '.ssh' ) do
  mode 0700
end

file ::File.join('/home/vagrant/', '.ssh', 'id_rsa' ) do
  #content "#{keys['private']}"
  owner "vagrant"
  group "vagrant"
  mode 0600
  action :create
end
