# remotezip-list-crc32

Lists name, uncompressed size, and CRC32 for all items in an HTTP(S)-hosted ZIP or 7-Zip archive. It outputs JSONL. Library (one function: `yield_file_dicts`) and command-line interface.

## Technical details
This is a simple wrapper, using the following Python libraries for each format:
 - ZIP: [`remotezip`](https://github.com/gtsystem/python-remotezip) for ZIP
 - 7-Zip: [`fsspec`](https://github.com/fsspec/filesystem_spec) (using its http filesystem) and [`py7zr`](https://github.com/miurahr/py7zr)