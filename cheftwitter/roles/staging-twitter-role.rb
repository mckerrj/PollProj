name "staging-twitter-role"

description "Role for my sample twitter app"
override_attributes()

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

default_attributes({})

