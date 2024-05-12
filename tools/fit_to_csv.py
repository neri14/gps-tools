import argparse
import csv
import os

from misc.fit import get_fit_data

def parse_args():
    parser = argparse.ArgumentParser(
        description='FIT to CSV converter',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('fit',
                        metavar='FIT',
                        nargs=1,
                        help='fit file path')

    return parser.parse_args()


def field_names(data):
    fields = []

    for _,frame in data.items():
        for field,_ in frame.items():
            if field not in fields:
                fields.append(field)

    return fields


if __name__ == '__main__':
    args = parse_args()
    fit_path = args.fit[0]

    print(f'Reading {fit_path}')
    data = get_fit_data(fit_path)

    fname = os.path.splitext(os.path.basename(fit_path))[0] + '.csv'
    print(f'Writing {fname}')

    with open(fname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names(data))
        writer.writeheader()
        writer.writerows(data.values())
