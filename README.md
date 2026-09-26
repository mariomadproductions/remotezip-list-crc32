# remotezip-list-crc32

Simple wrapper script that lists name, uncompressed size, and CRC32 for all items in a HTTP(S)-hosted ZIP or 7-Zip archive. It outputs JSONL. It is a library (with one public function: `yield_file_dicts`) and has a command-line interface.

## Technical details
This uses the following Python libraries for each format:
 - ZIP: [`remotezip`](https://github.com/gtsystem/python-remotezip) for ZIP
 - 7-Zip: [`fsspec`](https://github.com/fsspec/filesystem_spec) (using its http filesystem) and [`py7zr`](https://github.com/miurahr/py7zr)