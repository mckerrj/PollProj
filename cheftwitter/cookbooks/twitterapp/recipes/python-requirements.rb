virtualenv_path = "/home/vagrant/twitter_ve"
# Since it's a clean environment, skipping virtual environment for now.


python_pip "django" do
  version "1.6.2"
  action :install
  virtualenv virtualenv_path 
end

python_pip "celery" do
  action :install
 virtualenv virtualenv_path
end

python_pip "django-celery" do
  action :install
  virtualenv virtualenv_path
end

python_pip "django-tastypie" do
  action :install
  virtualenv virtualenv_path
end

python_pip "oauth2" do
  action :install
  virtualenv virtualenv_path
end

python_pip "oauth" do
  action :install
  virtualenv virtualenv_path
end

python_pip "django-oauth2-provider" do
  action :install
  virtualenv virtualenv_path
end

python_pip "mysql-python" do
  action :install
  virtualenv virtualenv_path
end

python_pip "requests" do
  version "2.2.1"
  action :install
  virtualenv virtualenv_path
end

python_pip "requests-oauthlib" do
  action :install
  virtualenv virtualenv_path
end

#python_pip "oauthlib" do
#  action :install
#  version "0.6.1"
#  virtualenv virtualenv_path
#end

python_pip "oauthlib" do
  action :upgrade
  version "0.6.1"
  virtualenv virtualenv_path
end

python_pip "mock" do
  action :install
  virtualenv virtualenv_path
end

python_pip "redis" do
  action :install
  virtualenv virtualenv_path
end

python_pip "uwsgi" do
  action :install
  virtualenv virtualenv_path
end

python_pip "south" do
  action :install
  virtualenv virtualenv_path
end
