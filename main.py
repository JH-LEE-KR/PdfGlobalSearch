# ------------------------------------------
# Copyright 2023, Jaeho Lee, dlwogh9344@khu.ac.kr,
# All rights reserved.
# ------------------------------------------

from concurrent.futures import ProcessPoolExecutor
import argparse
import glob
from pypdf import PdfReader

def get_args_parsers():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='./', help='Path to the directory')
    parser.add_argument('--keyword', type=str, default='Jaeho Lee', help='Keyword to search')
    parser.add_argument('--copy', action='store_true', default=False, help='Copy the file to the destination directory')
    parser.add_argument('--dst', type=str, default='./', help='Destination directory to copy the file')
    parser.add_argument('--proc', type=int, default=2, help='Number of processes to use')

    return parser

def search(path, keyword):
    reader = PdfReader(path)
    for page in reader.pages:
        text = page.extract_text()
        if keyword in text:
            print(f'Found keyword "{keyword}" in {path}')
            return path

def main():
    parser = get_args_parsers()
    args = parser.parse_args()

    files = glob.glob(args.path + '/**/*.pdf', recursive=True)

    with ProcessPoolExecutor(max_workers=args.proc) as executor:
        results = [executor.submit(search, path, args.keyword) for path in files]

        paths = []
        for r in results:
            if r.result() is not None:
                paths.append(r.result())
    
    if len(paths) == 0:
        print('No file found')
        exit(0)

    if args.copy and args.dst:
        import shutil
        for path in paths:
            shutil.copy(path, args.dst)
            print('Copied {} to {}'.format(path, args.dst))
    
    exit(0)

if __name__=='__main__':
    main()