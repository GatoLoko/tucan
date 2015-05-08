# Introduction #

This article will describe the specifications for the future addon API.

An addon in Tucan is every feature that is not part of the core or the services plugins mechanism. For instance, it could be auto-extract, search engines, restart router...

These addons will be added to the Update Manager system so they can be updated separately from Tucan core.


# Specs #

Here are the different parts of Tucan core that need to be exposed through the addon API.

  * Menu
  * Toolbar
  * Download/Upload API
  * Events (start/end of a download, a captcha pop-up appears...)