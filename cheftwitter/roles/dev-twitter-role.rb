name "dev-twitter-role"

description "Role for my sample twitter app"
override_attributes()

run_list(
	"recipe[apt]",
	"recipe[mysql::client]",
	"recipe[mysql::server]",
	"recipe[database::mysql]",
	"recipe[redisio::install]",
	"recipe[redisio::enable]",
	"recipe[twitterapp::mysql-server-setup]"
)

default_attributes({})

