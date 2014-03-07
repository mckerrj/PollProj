Tastypie Tutorial App for Django, basic Python, Celery, Tastypie, and Chef.

What the TwitterApp does
1) Setup a simple Django project
2) Shows how to set up a simple Django Model
2) Setup a simple Tastypie API
3) Run tests against your model and your API.  Simple tests and some mock tests
4) Have a python object that Authenticates with Twitter and gets data about your Tweets and Twitter Handle associated with those Tweets. and stores them
   using your DJango model.
5) Have a simple Celery app that runs the python-twitter sync-up every five minutes (if you let it).
6) Have a simple web app that uses HTML and Javascript (no Django views) to call the Tastypie API's to get your Tweet and Twitter user data and display them
in a VERY simple app.
7) Deploy the entire app and stack using Chef and Vagrant which includes:
  - Redis to handle messaging for Celery
  - Mysql install, setup databases and users
  - Django and uwsgi
  - A Simple Nginx config
  - Setup a Virtual Environment
  - Get the code and MOST dependencies from GitHub
8) deploy your app using Jenkins

Assumptions:
- You can use some unix-like environment.  I've only tested this on OSX and a Vagrant Precise64 environment.
- You can do some basic stuff with Git.
- You know a little bit about software development.  Databases. Stuff like that.
- You can do some basic stuff with virtual machines.

So let's do all that.  We're going to go out of order from above and get it up and running, then walk through all of the app bits.


1) Get the code and stuff.
  a) Create a directory where you want your stuff.
    - run <code>git clone ???repository????'</code>
  b) Now you've got some code! Yay.  Unfortunately, you're not quite done.
2) Now 'cd' into the TwitterApp directory.
  - Sidenote: I've got the Chef repository and the App Repository all together.  This isn't the cleanest way to go, but for a training app, it's ok.
  a) You can now see various bits of the app that I've all put in the root directory more for simplicity than for cleanliness. Things to note:
    1) README!
    2) The 'cheftwitter' directory.  This contains all of the chef recipes, roles, environments, cookbooks that you'll need.  It also contains the Vagrantfile.
       I'm not going to go into Chef in detail until later, but the Vagrantfile should be all you need to get the whole kit running.
    3) Before you run off and run the vagrant file though, you may need a pre-requisite, particularly on OSX.  We're going to be using chef-solo for the this exercise.
       Chef Solo has some weirdness compared with enterprise, so make sure you get the latest.  Assuming you've got Vagrant installed, you'll need the omnibus package.
       So run: <code>vagrant plugin install vagrant-omnibus</code>.  Otherwise you're likely to get all sorts of versioning errors.
    4) The run <code>vagrant up</code>
    5) I've found that sometimes this will provision the VM with chef-solo, and sometimes not.  If you don't see any chef stuff happening, run <code>vagrant provision</code>
       after <code>vagrant up</code> has completed.
    6) ssh into the VM using <code>vagrant ssh</code>
    7) You'll need to run some stuff to finish it all.
       - Activate the virtual eng <code>source twitter_ve/bin/activate</code>
       - Switch directories into the twitter directory
       - run <code>python manage.py syncdb</code>  When the terminal asks you if you want to create a superuser, say, 'no'
       - run <code>python manage.py loaddata twitter/tests/fixtures/data.json</code>  Here we're just loading some data for giggles so you can play around with the API's
       - Now we want to runs some tests, make sure everything works, so run <code>python manage.py test</code> It may ask you if you want to delete the test_twitter db,
         say, 'yes'.  Should be ok now.
    8) Now you need to run the process that goes to Twitter and sucks up Jason's info.  Yes, this currently has my Twitter Auth info in the app.  Don't abuse it.
       run the command: <code>celery --app=twitterapp worker --loglevel=info -B</code>



