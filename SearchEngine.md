#Specs of the Tucan search engine.

# Introduction #

This article will describe the specifications of the Tucan search engine.

# UI #

The search dialog window will have a search box, a treeview to display the results of a query, a treeview to display the available services, with the number of free slots for each service.

# Fetcher #

The fetcher class will launch all the query threads, check the links and return the results to the program.

**Use case**

  * Type a string to search
  * Type "Enter"
  * Creation of a Fetcher.search thread
    * Creation of SearchEngine instances
    * Creation of SearchEngine.search threads
    * Each thread perfoms the search, check if the main thread is still alive, if so return a batch of urls to be checked, if not stops.
  * Main thread checks the links
  * If it is still the current thread (no other search has been launched), the package is sent to the program


# Search engine plugins #

# Work in progress #

![http://i.imgur.com/O0MxK.png](http://i.imgur.com/O0MxK.png)