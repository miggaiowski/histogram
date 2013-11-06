#! /usr/bin/env python

"""
Usage:
  histogram.py [<input>] [-n=<num_bins>] [-o=<output>] [-rsf]
  histogram.py (-h | --help)

  <input>        org file one [default: -]
Options:
  -h --help                 Show this screen.
  -n --num_bins=<num_bins>  Number of bins [default: 80]
  -o --output=<output>      Save the chart to this file
  -s --no_show              Don't show the chart
  -r --remove_outliers      Disconsider values that are more than two stddev from the avg.
  -f --force                Overwrite output file
"""

from docopt import docopt
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def histogram(filename, num_bins, remove_outliers=False):
    if not filename or filename == '-':
        all_lines = sys.stdin.readlines()
    else:
        with open(filename, 'r') as f:
            all_lines = f.readlines()
    cleaned = [l.strip() for l in all_lines if l]
    seq = [float(i) for i in cleaned]
    if remove_outliers:
        avg = np.average(seq)
        std = np.std(seq)
        seq = [i for i in seq if avg - 4 * std < i < avg + 4 * std]
    # the histogram of the data
    n, bins, patches = plt.hist(seq, num_bins, normed=False, facecolor='blue', alpha=0.65)
    xlabels = ["(%.2f, %.2f)" % (bins[i], bins[i+1]) for i in xrange(len(bins)-1)]
    xticks = [(bins[i] + bins[i+1])/2 for i in xrange(len(bins)-1)]
    plt.xticks(xticks, xlabels, rotation='45', horizontalalignment='right', size='x-small')
    plt.ylabel('Number of samples')
    plt.xlabel('Value range')
    # plt.title(r'Distribution of local search improvement ratio')
    plt.axis([min(seq), max(seq), 0, max(n)])
    plt.grid(False)
    # import matplotlib.mlab as mlab
    # mean = np.average(seq)
    # sigma = np.std(seq)
    # x = np.linspace(min(seq), max(seq), 1000)
    # plt.plot(x, map(lambda x: x*1, mlab.normpdf(x, mean, sigma)), 'g-')


if __name__ == "__main__":
    arguments = docopt(__doc__, version='0.1')
    # print arguments
    filename = arguments['<input>']
    num_bins = int(arguments['--num_bins'])
    output = arguments['--output']
    no_show = arguments['--no_show']
    force = arguments['--force']
    remove_outliers = arguments['--remove_outliers']

    histogram(filename, num_bins, remove_outliers)

    if output:
        if not os.path.exists(output) or force:
            plt.savefig(output, dpi=400, bbox_inches='tight')
        else:
            print "File exists:", output
    if not no_show:
        plt.show()
