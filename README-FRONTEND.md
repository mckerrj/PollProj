## The simple front end to this app.

- The front end of the Twitter APP is a very simple JavaScript app with just two pages.
  - The [twitter_main.html](https://github.com/mckerrj/TwitterApp/blob/master/templates/twitter_main.html) page
    loads the Tweet data from the TastyPie API and displays it using Knockout.js.  It makes a simple AJAX call to
    the API, converts it to a KO Observable Array and displays it.  It reloads every 30 seconds.
  - The [twitter_user.html](https://github.com/mckerrj/TwitterApp/blob/master/templates/twitter_user.html) is just linked
    from the main page and just shows the user info associated with a tweet.  Same type of ajax call and loading.

  - I'm pretty aware that my front end skills aren't very good. :) Talk to the UX team if we want this part of the tutorial to be better.
