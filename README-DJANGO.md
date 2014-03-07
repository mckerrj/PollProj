The Django portion of this thing:

- Let's do a quick review of what is in this app for Django.
  - go to https://github.com/mckerrj/TwitterApp/blob/master/twitter/models.py
  - Models: The two primary objects are the TwitterUser and Tweet Objects.  They are fairly simple Django models.  I've mapped them from some of the fields that
    are returned when the <code>https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=newtMcKerr</code> is called.  To view a complete
    sample of what that call returns check this file (it's just a formatted JSON return so you can see some of the mappings):
    https://github.com/mckerrj/TwitterApp/blob/master/twitter/tests/fixtures/tweetstuff.json
  - Views: There are no django views in this project.  I am using straight javascript calls to the APIs.
  - Admin: The Admin app is enabled, and you can log in and do stuff.  go to: Hit http://192.168.33.10/admin.  Username is 'admin' password is 'admin314'
  - The other model objects are just left over from the Django and Tastypie tutorials.  I left them there
    pretty much just for testing purposes.