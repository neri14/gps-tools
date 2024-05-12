from garmin_fit_sdk import Decoder, Stream
import argparse
import csv
import os

def get_fit_data(path):
    stream = Stream.from_file(path)
    decoder = Decoder(stream)
    messages,_ = decoder.read()

    data = []
    fields = []

    for msg in messages['record_mesgs']:
        frame = {}

        for k,v in msg.items():
            match k:
                case 'latitude':
                    frame[k] = v / 11930465  # magic value to convert to degrees
                case 'longitude':
                    frame[k] = v / 11930465  # magic value to convert to degrees
                case 'speed':
                    frame[k] = v * 3.6   # convert speed to km/h
                case _:
                    frame[k] = v

            if k not in fields:
                fields.append(k)

        data.append(frame)

    return (fields,data)


def parse_args():
    parser = argparse.ArgumentParser(
        description='FIT to CSV converter',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('fit',
                        metavar='FIT',
                        nargs=1,
                        help='fit file path')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    fit_path = args.fit[0]

    print(f'Reading {fit_path}')
    fields,data = get_fit_data(fit_path)

    fname = os.path.splitext(os.path.basename(fit_path))[0] + '.csv'
    print(f'Writing {fname}')

    with open(fname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
