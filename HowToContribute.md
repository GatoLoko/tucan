# Introduction #

The main goal of this article is to present the various ways to contribute to the Tucan project.

Here are the main topics in which we need your help :

**Development help:**
  * Core Design.
  * GUI development.
  * Bug hunting.
  * Plugin Maintenance. (See [HowToWriteAServicePlugin](HowToWriteAServicePlugin.md))

**Documentation Help:**
  * HowToDocStrings

**Localization Help:**
  * HowToLocalize

Feel free to come on IRC if you are motivated and in the meantime try to get familiarized with the codestyle.

# Development #

## How to get started ##
You think you have an idea worth sharing ? You want to see a particular service in Tucan and are motivated to do it by yourself ? We would be happy to review and integrate your code.

There are a few steps to follow to start working on Tucan code, but it is really simple.

Tucan uses Mercurial as its revision control tool.

You can easily get the source code :

```
hg clone https://tucan.googlecode.com/hg/ tucan 
```

If you want to submit some code for us to review, you should create a clone of the main repository by going on the **Source** tab, and then **Clones**, and finally **Create a clone**.

That way you will have your own repo to push into and you can **open a ticket in the main repo** when you think your code is ready, with the name of your clone and the ID of the last commit to be reviewed.

If you have pulled the code from the main repo, then you should push it using

```
hg push https://your-repo.googlecode.com/hg/  
```

Otherwise, if you have pulled your code from your own repo, you can simply do :

```
hg push 
```

Now, a good start if you want to contribute is to write a new plugin or maintain an existing one (repair it or add premium support for instance). For more input on that matter, you should take a look at [HowToWriteAServicePlugin](HowToWriteAServicePlugin.md).

## How to get your code reviewed and integrated into the main repo ##

In order to reduce the time we spend on reviewing your code, you will have to follow these steps to see your code integrated into Tucan.

  * Clone the main repo in your own server side clone
  * Create a clone **for each bugfix or new feature**, **no branches** (only the default one)
  * Commit the changes to that clone, **only the changes regarding that bugfix/new feature**
  * Open a ticket in the tracker or answer to an open ticket with :
    * A link to your clone
    * The name of the revision to be reviewed

You can close the clone if your work on the feature is done and your code has been integrated in the main repo.