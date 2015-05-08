#Design specs of the implementation of the Web UI

# Introduction #

The goal of the Web UI is to provide a distant access to a machine where Tucan is running. This can be useful in a local network to centralize all the downloads on a computer, for instance the one plugged on the TV, but also to launch downloads from a remote computer and keep an eye on them when you are not at home.


# Specs #

## UI elements ##

The idea is to implement all the elements of the GUI :

  * The main list of downloads/uploads
  * The ability to add downloads/uploads
  * A box to add/check links and configure packages
  * A box to upload a text file containing some links
  * A box to perform the Recaptcha challenges

## Security ##

The user can specify some login/password (using Digest Authentication) or not. The ability to limit the IP address authorized should also be implemented.

The security is important due to the ability for the user to have access to Tucan over the Internet.

## Implementation ##

### Client ###

The Web UI should use some static HTML/CSS to display a nice, clean and light UI. The requests to the server should be done using Ajax and doing POST requests.

### Server ###

Python offers a native way to implement a simple HTTP server which would be enough for this purpose.