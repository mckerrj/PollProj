## Simple Tutorial App for Django, basic Python, Celery, Tastypie, and Chef.
This app is for onboarding new employees at SocialCode to familiarize yourself with some basics around our technical stack notably Django, Python, TastyPie,
Celery, UWSGI, Nginx, and Chef/Vagrant.

### What the TwitterApp does
- Setup a simple Django project
- Shows how to set up a simple Django Model
- Setup a simple Tastypie API
- Run tests against your model and your API.  Simple tests, mock tests, and API tests.
- Have a python object that Authenticates with Twitter and gets data about your Tweets and Twitter Handle associated with those Tweets. It then stores them
   using your Django model.
- Have a simple Celery app that runs the python-twitter sync-up every five minutes (if you let it).
- Have a simple web app that uses HTML and Javascript (no Django views) to call the Tastypie API's to get your Tweet and Twitter user data and display them
in a VERY simple app.  It's knockout.js and ajax.  Very simple.
- Deploy the entire app and stack using Chef and Vagrant which includes:
  - Redis to handle messaging for Celery
  - Mysql install, setup databases and users
  - Django and uwsgi
  - A Simple Nginx config for passing through requests, reverse proxy, and mapping requests to static files.
  - Setup a Python Virtual Environment
  - Get the code and dependencies from GitHub

### Assumptions:
- You can use some unix-like environment.  I've only tested this on OSX and a Vagrant Precise64 environment.
- You can do some basic stuff with Git.
- You know a little bit about software development.  Databases. Stuff like that.
- You can do some basic stuff with virtual machines.

###So let's do all that.  
We're going to go out of order from above and get it up and running, then walk through all of the app bits.


- Get the code and stuff.
  - Create a directory where you want your stuff.
    - run <code>git clone git@github.com:mckerrj/TwitterApp.git</code>
  - Now you've got some code! Yay.  Unfortunately, you're not quite done.
- Now 'cd' into the TwitterApp directory.
  - Sidenote: I've got the Chef repository and the App Repository all together.  This isn't the cleanest way to go, but for a training app, it's ok.
  - You can now see various bits of the app that I've all put in the root directory more for simplicity than for cleanliness. Things to note
    - README
    - The 'cheftwitter' directory.  This contains all of the chef recipes, roles, environments, cookbooks that you'll need.  It also contains the Vagrantfile.
       I'm not going to go into Chef in detail until later, but the Vagrantfile should be all you need to get the whole kit running.
    - Before you run off and run the vagrant file though, you may need a pre-requisite, particularly on OSX.  We're going to be using chef-solo for the this exercise.
       Chef Solo has some weirdness compared with enterprise, so make sure you get the latest.  Assuming you've got Vagrant installed, you'll need the omnibus package.
       So run: <code>vagrant plugin install vagrant-omnibus</code>.  Otherwise you're likely to get all sorts of versioning errors.
    - Then run <code>vagrant up</code>
    - I've found that sometimes this will provision the VM with chef-solo, and sometimes not.  If you don't see any chef stuff happening, run <code>vagrant provision</code>
       after <code>vagrant up</code> has completed.
    - ssh into the VM using <code>vagrant ssh</code>
    - If you get an error from Chef about being unpable to interact with Github (access denied or something like that) you need to setup keys for github ON YOUR HOST MACHINE.  I have vagrant setup to passthrough ssh from the host.  If you want something else, then edit the Vagrantfile to do what you want.
    - **Note** You'll see OATH stuff in the 'settings.py' file but I've revoked access for those.  You'll need to add your own OAUTH stuff for Twitter.
      want your own stuff, please change the following parameters in the project's 'settings.py' file.
      - OAUTH_TOKEN
      - OAUTH_TOKEN_SECRET
      - CONSUMER_KEY
      - CONSUMER_SECRET
      - TWITTER_SCREENNAME
      - To Change them, you'll need a Twitter account then
        - Then you'll need to login to Twitter's developer site at 'apps.twitter.com' and click the 'create new app' button
        - Once you've created the app you need to create access tokens.  Click on the API keys tab and create them.
        - Then copy the right keys into 'settings.py' file.

    - You'll need to run some stuff to finish it all.
       - Activate the virtual environment <code>source twitter_ve/bin/activate</code>
       - Switch directories into the twitter directory
       - run <code>python manage.py syncdb</code>  When the terminal asks you if you want to create a superuser, say, 'no'
       - run <code>python manage.py loaddata twitter/tests/fixtures/data.json</code>  Here we're just loading some data for giggles so you can play around with the API's
       - run <code>sudo python manage.py collectstatic</code> (need sudo, because of where I'm putting the static files).
       - Now we want to runs some tests, make sure everything works, so run <code>python manage.py test</code> It may ask you if you want to delete the test_twitter db,
         say, 'yes'.  Should be ok now.
    - Now you need to run the process that goes to Twitter and sucks up your twitter info. 
      Run the command: <code>sudo celery --app=twitterapp worker --loglevel=info -B</code> (make sure you're in the 'twitter' directory when you run this).
      The task that gets the Twitter stuff runs once every 5 minutes.  Probably don't want to leave it running.  Run it until you see it suck up the goods and then
      <code>ctrl-c</code> that process.  Celery will print out a bunch of stuff related to the task, so you'll see it happen.  If you're impatent, go to
      settings.py and shorten the time for the task.
    - Last step: Start django and uwsgi: <code>sudo uwsgi --socket /var/run/twitter.sock --module twitterapp.wsgi --chmod-socket=666</code>
       (make sure you're in the 'twitter' directory when you run this).
    - Open a browser and hit http://192.168.33.10 and BAM.  You should see a list of Tweets.  You can click on the Twitter User in any row to
      go to a simple detail page for the user.
    - You can also play with most of the API's through an API tool or the URL
      - http://192.168.33.10/api/v1/tweet/
      - http://192.168.33.10/api/v1/tweet/<tweetid>
      - http://192.168.33.10/api/v1/tweet/schema
      - http://192.168.33.10/api/v1/twitteruser/
      - http://192.168.33.10/api/v1/twitteruser/<twitter-handle>
      - http://192.168.33.10/api/v1/twitteruser/schema
    - I've also enabled the admin app so you can play around with data.  Hit http://192.168.33.10/admin.  Username is 'admin' password is 'admin314'

  ### Now onto the project itself.
  I'll create a different README for each major chunk of the project.
  - [README-DJANGO](README-DJANGO.md)
  - [README-TASTYPIE](README-TASTYPIE.md)
  - [README-CELERY](README-CELERY.md)
  - [README-TESTS](README-TESTS.md)
  - [README-CHEF](README-CHEF.md)
  - [README-WEBSETUP](README-WEBSETUP.md)
  - [README-FRONTEND](README-FRONTEND.md)




