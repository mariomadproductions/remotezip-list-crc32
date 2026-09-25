import argparse
import json

import remotezip

import fsspec
import py7zr

DEFAULT_BUFFER_SIZE = 64 * 1024  # 64 KiB
ARCHIVE_TYPES = ['zip', '7z']
DEFAULT_ARCHIVE_TYPE = 'zip'

def _yield_file_dicts_from_obj(obj, archive_type):
    mappings = {'zip': {'name':  'filename',
                        'size':  'file_size',
                        'crc32': 'CRC'},
                '7z':  {'name':  'filename',
                        'size':  'uncompressed',
                        'crc32': 'crc32'}
                }

    for info in obj:
        file_dict = {}
        for out_name, attr_name in mappings[archive_type].items():
            item = getattr(info, attr_name, None)
            if item is not None and out_name == 'crc32':
                item = f"{item:08x}"
            file_dict[out_name] = item
        yield file_dict

def _yield_file_dicts_from_zip(url, buffer_size):
    with remotezip.RemoteZip(url, initial_buffer_size=buffer_size) as remote_zip_obj:
        file_info_obj = remote_zip_obj.infolist()
        yield from _yield_file_dicts_from_obj(file_info_obj, 'zip')

def _yield_file_dicts_from_7z(url, buffer_size):
    if buffer_size is None:
        fs = fsspec.filesystem('http')
    else:
        fs = fsspec.filesystem('http', block_size=buffer_size)

    with fs.open(url, 'rb') as f:
        with py7zr.SevenZipFile(f, mode='r') as archive:
            file_info_obj = archive.list()
            yield from _yield_file_dicts_from_obj(file_info_obj, '7z')

def yield_file_dicts(url, archive_type=DEFAULT_ARCHIVE_TYPE, buffer_size=DEFAULT_BUFFER_SIZE):
    if archive_type == 'zip':
        yield from _yield_file_dicts_from_zip(url, buffer_size)
    elif archive_type == '7z':
        yield from _yield_file_dicts_from_7z(url, buffer_size)
    else:
        raise ValueError('Invalid archive type')

def get_args():
    parser = argparse.ArgumentParser(prog='remotezip-list-crc32', description='Lists name, uncompressed size, and CRC32 for all items in a HTTP(S)-hosted ZIP or 7-Zip archive. It outputs JSONL.')
    parser.add_argument('URL')
    parser.add_argument('-t', '--archive-type', choices=ARCHIVE_TYPES, default=DEFAULT_ARCHIVE_TYPE, help=f'(default: {DEFAULT_ARCHIVE_TYPE})')
    parser.add_argument('--buffer-size', type=int, default=DEFAULT_BUFFER_SIZE, help=f'For ZIP, this is used for initial buffer size, for 7-Zip, it is simply for the buffer size. (default: {DEFAULT_BUFFER_SIZE})')
    return parser.parse_args()

def main():
    args = get_args()
    for file_dict in yield_file_dicts(args.URL, args.archive_type, args.buffer_size):
        print(json.dumps(file_dict))
