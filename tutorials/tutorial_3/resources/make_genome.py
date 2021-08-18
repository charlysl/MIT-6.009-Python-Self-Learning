#!/usr/bin/env python3

import json, csv, sys

# CSV has columns
# title
# url
# everything starting with "?" becomes a feature, and is assumed to be in {0,1}

# JSON outputs a list of dictionaries, each of which has fields
# title - title from CSV
# url - url from CSV
# genes - ordered list of {0,1} from non-ignored columns

def convert(name):
    music = []
    with open(name + '.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song = {}
            song["title"] = row['title']
            song["url"] = row['url']
            genes = []
            for k in sorted(row.keys()):
                if k.startswith('?'):
                    genes.append(1 if row[k]=="1" else 0)
            song["genes"] = genes
            music.append(song)

    print(json.dumps(music))

def print_usage():
    print(sys.argv[0] + " [name of csv file, without .csv]")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return 1
    name = sys.argv[1]
    convert(name)

if __name__ == "__main__":
    main()

