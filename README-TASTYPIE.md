Tastypie!

The Tastypie stuff is mostly in the file 'api.py'.  I'll go through some more detail here:

- The primary resources are TwitterUserResource and Tweet Resource. The others are just leftover from Django and Tastypie.
  - Both methods only allow for 'get' operations since the actual data is pulled from twitter.
  - Most of this is pretty simple and out of the Tastypie docs, but one main difference: The TwitterUserResource is an example
    of using a non-standard URL construction to filter against the Resource/Object type.
    <code>
        detail_uri_name = 'screen_name'

        def prepend_urls(self):
            return [
                url(r"^(?P<resource_name>%s)/(?P<screen_name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            ]
    </code>
    The code above basically uses the 'django.conf/urls' to construct a searchable REST api using the following construction:
      <code>http://192.168.33.10/api/v1/twitteruser/<twitter-screen-name></code>  This is important so you can construct URLs specifically
      for certain types of functions.
  - Authorization:  Right now gets are allowed on all of the methods, and that's it (Except for entry).  So you can play with
    the various API's directly.  I've got the EntryResource allowing everything so we can show how to test the APIs later.
    This app doesn't cover auth stuff specifically since we've already got a page for that here: https://socialcode.atlassian.net/wiki/display/ENG/Service+Authentication
    if you want to play with 'PUT', 'POST', 'DELETE' then just add <code>authorization = Authorization()</code> to the resource.
    DO NOT DO THIS IN REAL LIFE as you're basically letting anyone interact with the API through all methods.
  - Here are some APIs you can play with if you've got the app running
      - http://192.168.33.10/api/v1/tweet/
      - http://192.168.33.10/api/v1/tweet/238746430288838656
      - http://192.168.33.10/api/v1/tweet/schema
      - http://192.168.33.10/api/v1/twitteruser/
      - http://192.168.33.10/api/v1/twitteruser/newtMcKerr
      - http://192.168.33.10/api/v1/twitteruser/schema

    - Schema is of interest as it shows the outline of the API and how to interact.