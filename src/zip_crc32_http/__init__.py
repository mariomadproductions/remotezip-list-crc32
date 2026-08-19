import argparse
import zipfile

def get_args():
    parser = argparse.ArgumentParser(prog='zip-crc32-http')
    parser.add_argument('URL')
    return parser.parse_args()

def main():
    args = get_args()
    
    if args.URL:
        import remotezip # slow import only done when needed - not just when viewing help
        remote_zip_obj = remotezip.RemoteZip(args.URL)
        for item in remote_zip_obj.infolist():
            print(f'{item.CRC:0{8}x} {item.filename}')
