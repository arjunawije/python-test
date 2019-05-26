#!/usr/bin/env python3

import argparse
import operator
import requests
import gzip

# Base URL of the Debian mirror
MIRROR_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("arch", type=str, help="architecture")
    args = parser.parse_args()
    arch = args.arch

    pkg_filename = MIRROR_URL + "Contents-" + arch + ".gz"
    print(pkg_filename)

    response = requests.get(pkg_filename)
    if response.status_code == 200:
        binary = response.raw.read()
        with open("/tmp/contents.gz", "w") as f:
            f.write(binary)

    result_map = dict()

    with gzip.open("/tmp/contents.gz") as file:
        for line in file:
            row_content = line.split()
            file_name = row_content[0]
            pkg_names = row_content[1]
            pkg_names_list = pkg_names.split(",")
            for pkg_name in pkg_names_list:
                print("file_name, pkg_name", file_name, pkg_name)
                result_map[pkg_name] = result_map.get(pkg_name, 0) + 1

    d_view = [(v, k) for k, v in result_map.items()]
    d_view.sort(reverse=True)  # natively sort tuples by first element
    for v, k in d_view:
        print("%s %d" % (k, v))

if __name__ == "__main__":
    main()
