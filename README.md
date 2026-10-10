# remotezip-list-crc32

Simple wrapper script that lists name, uncompressed size, and CRC32 for all items in a HTTP(S)-hosted ZIP or 7-Zip archive. It outputs JSONL. It is a library (with one public function: `yield_file_dicts`) and has a command-line interface.

## Technical details
This uses the following Python libraries for each format:
 - ZIP: [`remotezip`](https://github.com/gtsystem/python-remotezip) for ZIP
 - 7-Zip: [`smart_open`](https://github.com/piskvorky/smart_open) (using its http filesystem) and [`py7zr`](https://github.com/miurahr/py7zr)

Both use a [`requests`](https://github.com/psf/requests) session.

Note about past versions:
[Previously](https://github.com/mariomadproductions/remotezip-list-crc32/commit/da1f949f2b87a54e83011401284cb05f655b44db) this used [`fsspec`](https://github.com/fsspec/filesystem_spec)'s http filesystem, but I moved to smart_open because it uses requests, so we can share a requests session for both ZIP and 7-Zip, and requests seems to have better support for importing from a standard Python FileCookieJar, and therefore from a cookies.txt file.