The challenge states that the login functionality is unimplemented.

By looking at the source we find the file `http://shell2017.picoctf.com:35895/static/client.js` which hold the javascript functionality.
We can see that the `make_ajax_request()` function seems to be already implemented just not the `validate` function.

Using the console, we can execute the function with a dummy password to see what happens.

Surely enough, by doing so the flag pops up on the page.

Flag: `client_side_is_the_dark_sidebde1f567656f8c9b654a1ec24e1ff889`
