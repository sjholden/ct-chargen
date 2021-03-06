# ct-chargen
Classic Traveller Chargen

A character roller for classic traveller, designed to run on Google's AppEngine and use their cloud storage for the data.

All the rolling is performed server side, other than generating over and over it shouldn't be possible for the player to "cheat" - there's no undo or reloading to retry a roll.

## Current Deployment

A running instance is available at https://ct-chargen.appspot.com/

Note that rolled characters are all stored on the associated cloud storage - I have access to them though there's no way to enter private data anyway. They may also be deleted at any time which would break any /sheet/ urls.

## Known Issues

* The various tables are tested, plus an example char.
* Mustering out benefit roll DMs are "may add" in the rules, they are always used here which is bad if a Low Psg is worth more than Social (say your Social is already F).
* Doesn't provide any information on how many skill rolls or mustering out rolls are left to roll (it is derivable from the Roll History and a rule book though).
* Doesn't provide feedback on what changes have been made, for example there's no indication that Strength was increased or that a skill was gained aside from the numbers/text actually changing (again it is derivable from the Roll History and a rule book).

## AppEngine Notes

* Requires cloudstorage to be installed in lib in the deploy per https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/setting-up-cloud-storage
* Drop a favicon.ico in static too.

