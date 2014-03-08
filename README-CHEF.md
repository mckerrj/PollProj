## Chef setup

- I'm using Chef to manage the deployment of the app and all of it's dependencies.  It's setup to work either with Chef Enterprise or Chef Solo.
  I assume your using Chef-solo and not an enterprise account, so that's the default setup.
- All of the Chef and Vagrant configs are here: [Chef Directory](https://github.com/mckerrj/TwitterApp/tree/master/cheftwitter)
- Since we're using chef-solo with Vagrant, the [VagrantFile](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/Vagrantfile) the
  various chef artifacts are setup in the VagrantFile.
  ```
    config.omnibus.chef_version = :latest

    config.vm.provision :chef_solo do |chef|
     chef.cookbooks_path = "cookbooks"
     chef.roles_path = "roles"
     chef.environments_path = "environments"
     chef.data_bags_path = "databags"
     #chef.add_role("dev-twitter-role")
     chef.add_role("staging-twitter-role")
     #chef.environment = "development"
     chef.environment = "staging"
     #chef.node_name = 'twitterapp-dev'
     chef.node_name = 'twitterapp-staging'

     chef.json = {
        :mysql => {
            :bind_address => '192.168.33.10',
            :allow_remote_root => 'true',
            :remove_test_database => 'true',
            :remove_anonymous_users => 'true',
            :server_root_password => 'root314',
            :server_debian_password => 'root314',
            :server_repl_password => 'root314'
        }
     }
    end
  ```

  - You can see there are a couple of roles, development and staging.  Development I use just to setup a mysql and redis instance.  Staging does everything
  - I'm only going to talk about the staging role here.

- The [staging role](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/roles/staging-twitter-role.rb) basically loads the runlist that I want.
  ```
  run_list(
    "recipe[apt]",
    "recipe[mysql::client]",
    "recipe[mysql::server]",
    "recipe[database::mysql]",
    "recipe[redisio::install]",
    "recipe[redisio::enable]",
    "recipe[python]",
    "recipe[twitterapp]",
    "recipe[twitterapp::virtualenv]",
    "recipe[twitterapp::mysql-server-setup]",
    "recipe[twitterapp::python-requirements]",
    "recipe[twitterapp::key-file-forgit]",
    "recipe[git]",
    "recipe[twitterapp::git-twitter]",
    "recipe[twitterapp::nginx]",
    "recipe[twitterapp::vim]"
)
  ```
  - Yeah, I know I'm installing vim using a runlist. :)

- The [staging environment](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/environments/staging.json) would normally be all of the
  standard settings that I want, but chef-solo does some weird stuff with the MySQL cookbook.  Sor for Solo it'll use the <code>chef.json</code>
  stuff in the VagrantFile and for Enterprise it'll use the settings in the environment file:
  ```
    {
      "chef_type": "environment",
      "cookbook_versions": {},
      "default_attributes": {
      "mysql": {
            "bind_address": "192.168.33.10",
      "allow_remote_root": "true",
      "remove_test_database": "true",
      "remove_anonymous_users": "true"
          },
      "redisio": {
                    "default_settings": {
           "address":"192.168.33.10"
        }
             }
      },
      "description": "Jason's Staging Environment",
      "json_class": "Chef::Environment",
      "name": "staging",
      "override_attributes": {
        "mysql": {
        "server_root_password": "root314"
        }
    }
  ```
- Finally, there are a bunch of fairly simple recipes for setting things up. They are in
  [this directory](https://github.com/mckerrj/TwitterApp/tree/master/cheftwitter/cookbooks/twitterapp/recipes)
  - The [git-twitter.rb](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/cookbooks/twitterapp/recipes/git-twitter.rb) file is setting
    up the Deploy Keys for pulling the git repo.
    - copy the "id_rsa_twitterapp" file to the .ssh directory.  That's the deploy key
    - copy the "config" file to the .ssh directory (sets the name of the file, adds the host, turns off strict checking).
    - checkout the code from gihub
  - The [key-file-forgit.rb](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/cookbooks/twitterapp/recipes/key-file-forgit.rb) you can ignore for now.
  - The [mysql-server-setup.rb](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/cookbooks/twitterapp/recipes/mysql-server-setup.rb) file
    sets up the database stuff.
      - Creates databases
      - Creates users
      - Grants privileges
      - Restarts the mysql service.
  - The [nginx.rb](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/cookbooks/twitterapp/recipes/nginx.rb) is NGinx
    - Install NGinx
    - Link to the NGinx config file for this project (explained elsewhere)
    - Check for pid file, if not start the service, otherwise reload the service.
  - The [virtualenv.rb](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/cookbooks/twitterapp/recipes/virtualenv.rb) file just creates
    a python virtual environment.
  - The [python-requirements.rb](https://github.com/mckerrj/TwitterApp/blob/master/cheftwitter/cookbooks/twitterapp/recipes/python-requirements.rb)
    installs the necessary python stuff for the project.

- That should really cover all of the chef config for this project.

