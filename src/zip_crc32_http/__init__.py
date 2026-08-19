import argparse
import remotezip

def get_args():
    parser = argparse.ArgumentParser(prog='zip-crc32-http')
    parser.add_argument('URL')
    return parser.parse_args()

def main():
    args = get_args()

    remote_zip_obj = remotezip.RemoteZip(args.URL)
    for item in remote_zip_obj.infolist():
        print(f'{item.CRC:0{8}x} {item.filename}')