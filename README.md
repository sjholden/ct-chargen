# ct-chargen
Classic Traveller Chargen

A character roller for classic traveller, designed to run on Google's AppEngine and use their cloud storage for the data.

All the rolling is performed server side, other than generating over and over it shouldn't be possible for the player to "cheat" - there's no undo or reloading to retry a roll.

## AppEngine Notes

Requires cloudstorage to be installed in lib in the deploy per https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/setting-up-cloud-storage

