The Void Extractor
==================

Simple command line extractor for the data files of the game
[The Void](http://www.tension-game.com/).

Datafiles come in the form of `.vfs` files in The Void, each of those
bundles a directory in uncompressed form. Modding should be possible
by simply having a plain directory with the same name next to the .vfs
file.

You can extract everything (`-x`), name files to extract explicitly or
extract by glob pattern (`--glob "*.ogg"`). Example usage would look
like this:

    ./thevoid_extractor.py \
        -v ~/games/SteamLibrary/steamapps/common/The\ Void/data/Sounds.vfs \
        --targetdir data/ -x

If `--targetdir` is not given files will be extracted to the current
working directory.


Usage
-----

    usage: thevoid_extractor.py [-h] [-l] [-x] [-t DIR] [-a] [-s] [-g PATTERN] [-v VFS] [FILE ...]
    
    'The Void' datafile extraction tool
    
    positional arguments:
      FILE
    
    optional arguments:
      -h, --help            show this help message and exit
      -l, --list            List all resource files
      -x, --extract         Extract resource files
      -t DIR, --targetdir DIR
                            The directory where files will be extracted
      -a, --extract-all     Extract all resource files
      -s, --stdout          Extract data to stdout
      -g PATTERN, --glob PATTERN
                            Extract files by glob pattern
      -v VFS, --vfs VFS     Prefix of the resource files, can be 'resources' or 'german'
    
