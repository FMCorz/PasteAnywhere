Paste Anywhere
==============

A Sublime Text plugin to paste multiple selections to your favourite paste site.

Usage
-----

Commands accessible via the command palette:

- Paste Anywhere: to Pastie
- Paste Anywhere: Privately
- Paste Anywhere: For a day
- ...

Add your own commands to paste to other sites, define your own settings like the privacy, the time to live, the password, or other depending on the site you are using.

Settings
--------

Each of these settings can be overwritten per command call.

### to

The paster to paste to. The possible values are the name of the Paster (see the directory PyPasteLib/pasters) without the .py.

The following settings are the ones offered by the library [PyPasteLib](https://github.com/FMCorz/PyPasteLib), not all the sites support all of them.

### ttl

The time to live, in seconds.

### private

True if the paste should be private.

### poster

The name of the person pasting.

### description

The description of the paste.

### password

The password to access the paste.

### result_sent_to

Where you want the URL to be set. The possible values are: clipboard, newfile, outputpanel.

### set_identifiers

If you do not want the identifiers of each blob you are pasting to be defined, set this to false. For instance, on Gist, the identifier is the name of the file.

### settings

The settings key must contain a key/value array for specific settings of the Paste. For instance, pasting to Pastebin requires an API key which must be set here.

Sites supported
---------------

- [Code Vault](http://cdv.lt)
- [gist](https://gist.github.com/)
- [Hey! Paste it](http://www.heypasteit.com/)
- [KDE](http://paste.kde.org)
- [Mozilla](http://pastebin.mozilla.org)
- [Paste2.org](http://paste2.org)
- [PasteBay](http://pastebay.net)
- [pastebin](http://pastebin.com)
- [Pastee](https://pastee.org)
- [Pastie](https://pastie.org)
- [Slexy](https://slexy.org)
- [SnipSource](http://snipsource.com)
- [Ubuntu](http://paste.ubuntu.com)

Or any other ones supported by [PyPasteLib](https://github.com/FMCorz/PyPasteLib#pasters-supported).

License
-------

Licensed under the [MIT License](http://www.opensource.org/licenses/mit-license.php)