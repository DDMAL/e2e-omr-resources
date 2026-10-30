#!/usr/bin/env python3
"""Apply the manual review of liquescent <nc> elements that had no @curve (#20).

Input is the reviewed CSV (columns: file, nc_xml_id, curve, notes), where
`curve` is one of:
  - "not a liquescent" -> remove the <liquescent/> child; <nc> becomes self-closing
  - "down"             -> add curve="c"  (Downwards liquescent, as in the Cress/Rodan mapping)
  - "up"               -> add curve="a"  (Upwards liquescent)

Every target must have exactly this three-line shape, otherwise the script stops
without writing anything:

    <nc xml:id="..." ...>
        <liquescent xml:id="..."/>
    </nc>

Edits are made line by line, so untouched lines stay byte-identical.
Dry run by default; pass --write to modify files.

Usage:
    python3 scripts/apply_no_curve_review.py REVIEW.csv resulting_mei_files/Einsiedeln/Reviewed_once [--write]
"""
import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

from lxml import etree

CURVE = {"down": "c", "up": "a"}
REMOVE = "not a liquescent"
NC_OPEN = re.compile(r'^(\s*)<nc (xml:id="([^"]+)"[^>]*?)>(\r?\n)$')
LIQ = re.compile(r'^\s*<liquescent xml:id="[^"]+"/>\r?\n$')
NC_CLOSE = re.compile(r"^\s*</nc>\r?\n$")
MEI_NS = "http://www.music-encoding.org/ns/mei"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def load_review(path):
    jobs = defaultdict(dict)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            decision = row["curve"].strip().lower()
            if decision != REMOVE and decision not in CURVE:
                sys.exit(f"Unknown decision {row['curve']!r} for {row['nc_xml_id']}")
            jobs[row["file"].strip()][row["nc_xml_id"].strip()] = decision
    return jobs


def apply(path, targets):
    lines = path.read_bytes().decode("utf-8").splitlines(keepends=True)
    out, i, done = [], 0, {}
    while i < len(lines):
        m = NC_OPEN.match(lines[i])
        if m and m.group(3) in targets:
            nc_id = m.group(3)
            if i + 2 >= len(lines) or not LIQ.match(lines[i + 1]) or not NC_CLOSE.match(lines[i + 2]):
                sys.exit(f"{path.name}: {nc_id} is not in the expected 3-line shape; nothing written")
            if "curve=" in m.group(2):
                sys.exit(f"{path.name}: {nc_id} already has @curve; nothing written")
            indent, attrs, eol = m.group(1), m.group(2), m.group(4)
            decision = targets[nc_id]
            if decision == REMOVE:
                out.append(f"{indent}<nc {attrs}/>{eol}")
            else:
                out.append(f'{indent}<nc {attrs} curve="{CURVE[decision]}">{eol}')
                out.extend(lines[i + 1:i + 3])
            done[nc_id] = decision
            i += 3
            continue
        out.append(lines[i])
        i += 1
    missing = set(targets) - set(done)
    if missing:
        sys.exit(f"{path.name}: not found: {sorted(missing)}; nothing written")
    return "".join(out), done


def verify(text, done):
    root = etree.fromstring(text.encode("utf-8"))
    for nc in root.iter(f"{{{MEI_NS}}}nc"):
        nc_id = nc.get(XML_ID)
        if nc_id not in done:
            continue
        liqs = nc.findall(f"{{{MEI_NS}}}liquescent")
        if done[nc_id] == REMOVE:
            ok = len(liqs) == 0 and nc.get("curve") is None and len(nc) == 0
        else:
            ok = len(liqs) == 1 and nc.get("curve") == CURVE[done[nc_id]]
        if not ok:
            return nc_id
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("review_csv")
    ap.add_argument("mei_dir")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    jobs = load_review(args.review_csv)
    results = {}
    for fname, targets in sorted(jobs.items()):
        path = Path(args.mei_dir) / fname
        text, done = apply(path, targets)
        bad = verify(text, done)
        if bad:
            sys.exit(f"{fname}: verification failed at {bad}; nothing written")
        results[path] = (text, done)

    counts = defaultdict(int)
    for path, (text, done) in results.items():
        for d in done.values():
            counts[d] += 1
        if args.write:
            path.write_bytes(text.encode("utf-8"))
    print(f"{len(results)} files, " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    print("written" if args.write else "dry run (use --write to apply)")


if __name__ == "__main__":
    main()
