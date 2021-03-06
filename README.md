The Void Extractor
==================

Simple command line extractor for the data files of the game
[The Void](http://www.tension-game.com/).


Usage
-----

Datafiles come in the form of `.vfs` files in The Void, each of those
bundles a directory in uncompressed form. Modding should be possible
by simply having a plain directory with the same name next to the .vfs
file.

You can extract everything (`--extract-all`), name files to extract
explicitly or extract by glob pattern (`--glob "*.ogg"`). Example usage
would look like this:

    ./thevoid-extractor.py \
        -v "/win/Program Files/The Void/data/Sounds.vfs" \
        --extract --targetdir data/ -g "*.ogg"

If `--targetdir` is not given files will be extracted to the current
working directory.
