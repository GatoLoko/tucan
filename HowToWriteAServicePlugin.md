# Introduction #

This how-to will present the way to implement a service plugin in Tucan.

# Folders and files #

First of all, here are the differents files used in a service plugin.

## Files and folder located in /default\_plugins/ ##

**servicename/** : Directory containing all the files of a plugin. It shouldn't contain any dot in its name. (required)

**`__`init`__`.py** : To be recognized as a module by Python (required)

**service.conf** : File containing all the informations regarding the service (required)

**servicename.ico** : Icon (48x48) of the service, you can use the favicon (optional)

**anonymous\_download.py** : Do the job for anonymous download (optional)

**premium\_download.py** : Do the job for premium download (optional)

**premium\_cookie.py** : Get the cookie for premium download (optional)

## File located in `/tests/_default_plugins/` ##

**test\_servicename.py** : Test suite for automated testing (required)

# Building the test file #

We recommend that you start writing your plugin by defining a test file. The file should be saved under **`/tests/_default_plugins/test_servicename.py`**.

It contains some informations about the file : name, size, unit and some about the links, a valid one and an invalid one (so the program know when a link provided is valid or not). To get these links, you should upload the file called **`/tests/_default_plugins/prueba.bin`**, get the link, the name of the file and the size and units returned by the service. To get an invalid link, just modify the valid link until you get an error like "Error : the file doesn't exist." (but try not to have a 404 error).

To run the test suite, go to **/tests/** and run :
```
python suite.py _default_plugins/test_servicename.py
```