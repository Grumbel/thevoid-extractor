# The Void Extractor

A simple command-line tool to extract resource files from **[The Void](https://store.steampowered.com/app/37000/The_Void/)** game `.vfs`
bundles (the uncompressed resource-packed files used by the game).

This repository contains `thevoid_extractor.py` — a small Python 3 script that
reads `.vfs` files (file magic `LP2C`) and can list or extract embedded files.

## Requirements

* Python 3.8+
* No further external dependencies

## Quick start

```sh
python3 thevoid_extractor.py <VFSFILE> [FILES...]
```

## Usage

```txt
thevoid-extractor [-h] (-l | -x) [-o DIR] [-s] [-g PATTERN] VFSFILE [ENTRYTOEXTRACT ...]

'The Void' datafile extraction tool

positional arguments:
  VFSFILE              .vfs file to process (e.g. ".../The Void/data/Sound.vfs")
  ENTRYTOEXTRACT       individual entry to extract, extract all by default

options:
  -h, --help           show this help message and exit

actions:
  -l, --list           List all resource files
  -x, --extract        Extract resource files

options:
  -o, --outputdir DIR  The directory where files will be extracted
  -s, --stdout         Extract data to stdout
  -g, --glob PATTERN   Extract entries by glob pattern

```

## Examples

List the VFS content:

```sh
python3 thevoid_extractor.py --list "The Void/data/Sound.vfs"
```

Extract the complete VFS content:

```sh
python3 thevoid_extractor.py --extract "The Void/data/Sound.vfs" --outputdir extracted/
```

Extract only `.ogg` files using a glob:

```sh
python3 thevoid_extractor.py --extract "The Void/data/Sound.vfs" --glob "*.ogg" --outputdir extracted/
```
