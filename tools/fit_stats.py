import argparse
from statistics import mean,median,stdev

from misc.fit import get_fit_data
from misc.slope import calculate_slope


def parse_args():
    parser = argparse.ArgumentParser(
        description='FIT stats generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('fit',
                        metavar='FIT',
                        nargs=1,
                        help='fit file path')

    return parser.parse_args()


def print_stat(field, data):
    d = [x[field] for _,x in data.items() if field in x]
    
    if len(d) > 0:
        print(f'{field:27s}: min: {min(d):7.1f} max: {max(d):7.1f} avg: {mean(d):7.1f} median: {median(d):7.1f} stdev: {stdev(d):7.1f}')


def print_stats(data):
    print_stat('speed', data)
    print_stat('power', data)
    print_stat('cadence', data)
    print_stat('heart_rate', data)
    print_stat('enhanced_respiration_rate', data)
    print_stat('altitude', data)
    print_stat('slope', data)


if __name__ == '__main__':
    args = parse_args()
    fit_path = args.fit[0]

    print(f'Reading {fit_path}')
    data = get_fit_data(fit_path)
    data = calculate_slope(data)


    print_stats(data)
