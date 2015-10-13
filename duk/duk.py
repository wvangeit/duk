#!/usr/bin/env python3
"""Ducky"""

from __future__ import print_function

import os
import subprocess
import collections
import argparse
import sys
import warnings

# pylint: disable=E1103


def print_error_files(errors, max_marks):
    """Print the lines with files that generated errors"""

    fmt_error = "{0:<%d} {1:<10}" % (22 + max_marks)

    permission_error = False

    for filename in errors:
        error = errors[filename]

        if "Permission denied" in error:
            error_string = "Permission denied"
            permission_error = True
        else:
            error_string = error

        print(fmt_error.format(error_string, filename))

    return permission_error


def print_normal_files(file_sizes, max_marks, total_size, fmt, args):
    """Print the lines with files that generated no errors"""

    maxsize = max(file_sizes.values()) if file_sizes.values() else 0

    for filename in file_sizes:
        file_size = file_sizes[filename]
        if maxsize != 0:
            nmarks = int((max_marks - 1) * float(file_size) / maxsize) + 1
            percentage = 100 * float(file_size) / total_size
        else:
            nmarks = max_marks
            percentage = 100.0
        if not args.nogrouping:
            file_size = "{:,}".format(file_size)
        print(
            fmt.format(
                file_size,
                "%02.2f" %
                percentage,
                "".join(
                    ["#"] *
                    nmarks),
                filename))


def calculate_file_sizes(files_list, args):
    """Calculate the file sizes"""

    file_sizes = {}
    errors = {}

    for file_number, filename in enumerate(files_list):
        full_filename = os.path.join(args.dirname, filename)
        duks_proc = subprocess.Popen(
            ["du", "-kxs", full_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = duks_proc.communicate()
        error = stderr.decode("utf-8").split("\n")[0]
        if not args.noF:
            is_link = os.path.islink(full_filename)
            is_dir = os.path.isdir(full_filename)
            if is_link:
                filename += "@"
            elif is_dir:
                filename += "/"
        if error == "":
            file_sizes[filename] = int(stdout.decode("utf-8").split("\t")[0])
        else:
            errors[filename] = error
        if not args.noprogress:
            print_progress((file_number + 1) / len(files_list), 80)

    file_sizes = collections.OrderedDict(sorted(
        file_sizes.items(), key=lambda x: x[1]))

    return file_sizes, errors


def print_header(dirname, fmt):
    """Print header string"""

    print("\n\nStatistics of directory \"%s\" :\n" % dirname)
    print(fmt.format("in kByte", "in %", "histogram", "Name"))


def print_tail(total_size, permission_error, args):
    """Print tail string"""

    if not args.nogrouping:
        total_size = "{:,}".format(total_size)
    print("\nTotal directory size: %s kByte\n" % total_size)

    if permission_error:
        print("The Ducky has no permission to access certain "
              "subdirectories !\n", file=sys.stderr)


def print_progress(progress, total_bar_size):
    """Print a progress bar"""

    bar_size = int(round(total_bar_size * progress))
    pbar = "\r{0}".format(
        '>' * bar_size + '-' * (total_bar_size - bar_size))
    sys.stdout.write(pbar)
    sys.stdout.flush()


def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='Show disk usage statistics')
    parser.add_argument('dirname', metavar='dirname',
                        type=str,
                        nargs='?',
                        default='.',
                        help='Directory name')
    parser.add_argument('--nogrouping', action='store_true')
    parser.add_argument('--noprogress', action='store_true')
    parser.add_argument('--noF', action='store_true')
    return parser.parse_args()


def main():
    """Main"""

    args = parse_arguments()
    max_marks = 20
    fmt = "{0:<14} {1:<6} {2:<%d} {3:<10}" % (max_marks)

    files_list = os.listdir(args.dirname)
    permission_error = False

    file_sizes, errors = calculate_file_sizes(files_list, args)

    total_size = sum(file_sizes.values())

    print_header(args.dirname, fmt)
    print_error_files(errors, max_marks)
    print_normal_files(file_sizes, max_marks, total_size, fmt, args)
    print_tail(total_size, permission_error, args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThe Duck was shot by the user !")
        warnings.filterwarnings("ignore")
        sys.exit(1)
    except Exception as e:
        print(
            'Sorry, the Duck was eaten by the Python !\nReason:',
            sys.exc_info()[0])
        if isinstance(e, SystemExit):
            raise  # take the exit
