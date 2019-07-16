#!/usr/bin/env python

import os, csv

def write_csv(dn, bn, count, rows):
    with open(os.path.join(dn, bn + '--' + count + '.csv'), 'w', newline='') as op:
        cw = csv.writer(op)
        for r in rows:
            cw.writerow(r)

def read_csv(dn, bn, header_row_count=1, rows_per_file=400):
    headers = []
    output = []
    file_count = 0
    with open(os.path.join(dn, bn + '.csv'), 'r', newline='') as fd:
        cr = csv.reader(fd) #, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for r in cr:
            if len(headers) < header_row_count:
                headers.append(r)
                continue
            output.append(r)
            if len(output) >= rows_per_file:
                writeCSV(dn, bn, file_count, headers + output)
                output = []
                file_count += 1
            continue
        if len(output):
            write_csv(dn, bn, file_count, headers + output)


ROOT = os.path.abspath('.')
HEADER_ROW_COUNT = 1
ROWS_PER_FILE = 400

for dn, dl, fl in os.walk(ROOT):
    for fn in fl:
        qn = os.path.join(dn, fn)
        if not os.path.isfile(qn):
            continue
        (bn, ext) = os.path.splitext(fn)
        if ext.lower() != '.csv':
            continue
        if '--' in bn:
            continue
        # file exists and is a csv
        read_csv(dn, bn, HEADER_ROW_COUNT, ROWS_PER_FILE)
