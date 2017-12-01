#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import glob
import json
import argparse

def mk_img_json(label_dir, cfg_file, out_file):
    print("label_dir: %s\ncfg_file: %s\nout_file: %s\n"
          % (label_dir, cfg_file, out_file))

    data = {}
    data["labels"] = []
    data["categories"] = []

    for file in glob.glob("%s/*.png" % label_dir):
        fname = os.path.basename(file)
        idx = int((os.path.splitext(fname))[0])
        data["labels"].append({
            "file_name": "%s" % fname,
            "width": -1,
            "id": idx,
            "height": -1
        })

    cats = []
    with open(cfg_file, 'r') as cfg_json:
        cfg_labels = json.load(cfg_json)
        idx = 0
        for cat in cfg_labels["labels"]:
            lb_name = cat["readable"]
            data['categories'].append({
                "id": idx,
                "name": lb_name
            })
            idx = idx + 1
    
    with open(out_file, 'w') as outfile:  
        json.dump(data, outfile)

    return True

def main():
    parser = argparse.ArgumentParser(description='Create a json file for a dict of labels')
    parser.add_argument('--label_dir', required=True)
    parser.add_argument('--vista_cfg_file', required=True)
    parser.add_argument('--output_json', required=True)
    args = parser.parse_args()

    label_dir = os.path.abspath(args.label_dir)
    if mk_img_json(label_dir, args.vista_cfg_file, args.output_json):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
