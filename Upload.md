#Specs for the future upload system

# Introduction #

This document describes the implementation of the upload system in Tucan.


# Details #

## UI ##

This is how the UI could look like.

![http://i.imgur.com/QGzjT.png](http://i.imgur.com/QGzjT.png)

## Implementation ##

Urllib doesn't manage natively multipart/data. So we should use [Poster](http://atlee.ca/software/poster/) which is a 2 files library, very useful. It handles all we need and offers to use a callback function to be aware of the upload progress.

A working proof of concept has been done for Megaupload Anonymous using Poster.

## Todo ##

  * Manage the description field
  * Implement a function that generate strings of random numbers