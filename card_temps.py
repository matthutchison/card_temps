import argparse
import csv
import re
import sys
from glob import glob
from pathlib import Path
from pprint import pprint
from zipfile import is_zipfile, BadZipFile, ZipFile, ZipExtFile

DEFAULT_PATH = r'C:\ProgramFiles\Gatan\Logs\*DM.log'
DM_LOG_TEMPERATURE_PATTERN = re.compile(r'((:?\d?\d?\d[.]\d\d\s){10})')

def get_zip_temps(file):
    temps = {}
    with ZipFile(file) as z:
        for name in z.namelist():
            f = z.open(name)
            temps[name] = get_temps(f)
    return temps

def get_temps(file):
    if isinstance(file, ZipExtFile):
        try:
            data = file.readlines()
            data = (l.decode(errors='ignore') for l in data)
        except (UnicodeDecodeError, BadZipFile) as e:
            print('cannot open {} because of {}'.format(file.name, e))
            data = ''
    else:
        with open(file, mode='r', errors='ignore') as f:
            data = f.readlines()
    temps = [[int(float(i)) for i in x.group(0).split()] for x in (DM_LOG_TEMPERATURE_PATTERN.search(l) for l in data if 'Camera Temperature' in l) if x is not None]
    temps = list(zip(*temps)) #turn from row-major to column-major
    return temps

def preprocess_rows(temps):
    for k,v in temps.items():
        for i,c in enumerate(v):
            yield {'date': Path(k).stem[:10], 'processor': i, 'min': min(c), 'max': max(c), 'avg': sum(c)/len(c)}

def export_csv(filename, temps):
    with open(filename, mode='x', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['date', 'processor', 'min', 'max', 'avg'])
        writer.writeheader()
        writer.writerows(preprocess_rows(temps))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', '-o', help='A file path to write the .csv output to. File must not already exist.')
    parser.add_argument('files', nargs='*', help='A list of zip files containing .DM.log files and/or a list of .DM.log files directly.')
    args = parser.parse_args()
    files = args.files
    if len(files) == 0:
        print('No paths were provided, attempting to access .DM.log files at the standard path {}'.format(DEFAULT_PATH))
        files = glob(DEFAULT_PATH)
        if len(files) == 0:
            sys.exit('No DM.log file found, exiting')
    all_temps = {}
    for file in files:
        if is_zipfile(file):
            all_temps.update(get_zip_temps(file))
        else:
            all_temps[Path(file).stem[:10]] = get_temps(file)
    if not args.out:
        pprint(list(preprocess_rows(all_temps)))
    else:
        export_csv(args.out, all_temps)
