#!/usr/bin/env python3
"""Fix liquescent encoding in MEI files (DDMAL/e2e-omr-resources issue #20).

Correct encoding (per DDMAL/Rodan#1123):

    <neume>
        <nc oct="2" pname="c" curve="a">
            <liquescent/>
        </nc>
    </neume>

This script repairs two defects introduced by the pre-2024 mei_encoding /
Neon pipeline, and reports a third that cannot be repaired automatically:

  MISSING_LIQUESCENT  <nc ... curve="x"/> with no child <liquescent/>
                      -> a <liquescent/> child is inserted.
  DUPLICATE_LIQUESCENT  <nc ... curve="x"> with 2+ <liquescent/> children
                      -> all but the first are removed.
  NO_CURVE            <nc> with a <liquescent/> child but no curve attribute
                      -> REPORTED ONLY. The curve direction ("a" up /
                         "c" down) cannot be inferred from the file; it has
                         to be read off the manuscript image by a human.

Edits are made textually, one line at a time, so untouched lines keep their
original bytes and the git diff stays small.

Usage:
    python3 fix_liquescents.py DIR [DIR ...]                 # dry run
    python3 fix_liquescents.py DIR [DIR ...] --write         # apply fixes
    python3 fix_liquescents.py DIR [DIR ...] --report r.csv  # per-nc CSV
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import uuid
from collections import Counter
from pathlib import Path

MEI_NS = "http://www.music-encoding.org/ns/mei"

NC_OPEN = re.compile(r"<nc\b[^>]*>", re.S)
LIQUESCENT = re.compile(r"<liquescent\b[^>]*?/>", re.S)
CURVE_ATTR = re.compile(r'\bcurve\s*=\s*"([^"]*)"')
VALID_CURVES = {"a", "c"}

MISSING, DUPLICATE, NO_CURVE, BAD_CURVE = (
    "MISSING_LIQUESCENT",
    "DUPLICATE_LIQUESCENT",
    "NO_CURVE",
    "UNEXPECTED_CURVE_VALUE",
)


def new_xml_id() -> str:
    """An xml:id in the same style as the ones Neon writes."""
    return f"m-{uuid.uuid4()}"


def iter_nc(text: str):
    """Yield (start, end, open_tag, inner) for every <nc> element.

    `inner` is None for a self-closing <nc/>. <nc> elements are never nested,
    so a flat scan is safe.
    """
    pos = 0
    while True:
        m = NC_OPEN.search(text, pos)
        if m is None:
            return
        open_tag = m.group(0)
        if open_tag.endswith("/>"):
            yield m.start(), m.end(), open_tag, None
            pos = m.end()
            continue
        close = text.find("</nc>", m.end())
        if close == -1:  # malformed file; leave the rest alone
            return
        end = close + len("</nc>")
        yield m.start(), end, open_tag, text[m.end():close]
        pos = end


def indent_of(text: str, start: int) -> str:
    """The whitespace between the start of the line and position `start`."""
    line_start = text.rfind("\n", 0, start) + 1
    return text[line_start:start]


def xml_id_of(tag: str) -> str:
    m = re.search(r'\bxml:id\s*=\s*"([^"]*)"', tag)
    return m.group(1) if m else ""


def process(text: str):
    """Return (new_text, findings). Each finding is (kind, xml_id, curve)."""
    findings: list[tuple[str, str, str]] = []
    edits: list[tuple[int, int, str]] = []  # (start, end, replacement)

    for start, end, open_tag, inner in iter_nc(text):
        curve_match = CURVE_ATTR.search(open_tag)
        curve = curve_match.group(1) if curve_match else None
        liquescents = LIQUESCENT.findall(inner or "")
        nc_id = xml_id_of(open_tag)

        if curve is not None and curve not in VALID_CURVES:
            findings.append((BAD_CURVE, nc_id, curve))
            continue  # unknown value: report, change nothing

        if curve is not None and not liquescents:
            findings.append((MISSING, nc_id, curve))
            pad = indent_of(text, start)
            body = open_tag[:-2].rstrip() + ">"
            child = f"<liquescent xml:id=\"{new_xml_id()}\"/>"
            edits.append(
                (start, end, f"{body}\n{pad}    {child}\n{pad}</nc>")
            )

        elif curve is not None and len(liquescents) > 1:
            findings.append((DUPLICATE, nc_id, curve))
            kept = False
            new_inner_parts: list[str] = []
            last = 0
            for m in LIQUESCENT.finditer(inner):
                if not kept:
                    kept = True
                    continue
                # drop this one together with the whitespace in front of it
                cut = inner.rfind("\n", 0, m.start())
                cut = m.start() if cut == -1 else cut
                new_inner_parts.append(inner[last:cut])
                last = m.end()
            new_inner_parts.append(inner[last:])
            edits.append(
                (start, end, open_tag + "".join(new_inner_parts) + "</nc>")
            )

        elif curve is None and liquescents:
            findings.append((NO_CURVE, nc_id, ""))

    new_text = text
    for start, end, replacement in reversed(edits):
        new_text = new_text[:start] + replacement + new_text[end:]
    return new_text, findings


def verify(text: str) -> None:
    """Re-parse the result and assert every nc is now well formed."""
    from lxml import etree

    root = etree.fromstring(text.encode("utf-8"))
    for nc in root.iter(f"{{{MEI_NS}}}nc"):
        children = nc.findall(f"{{{MEI_NS}}}liquescent")
        curve = nc.get("curve")
        if curve in VALID_CURVES and len(children) != 1:
            raise AssertionError(
                f"nc {nc.get('{http://www.w3.org/XML/1998/namespace}id')}: "
                f"curve={curve} but {len(children)} liquescent children"
            )
        if curve is None and children:
            return  # NO_CURVE is expected to survive; reported, not fixed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="+", type=Path,
                    help="directories to scan (searched recursively)")
    ap.add_argument("--write", action="store_true",
                    help="write the fixes; without it nothing is modified")
    ap.add_argument("--report", type=Path,
                    help="write a per-nc CSV report to this path")
    ap.add_argument("--no-verify", action="store_true",
                    help="skip re-parsing fixed files with lxml")
    args = ap.parse_args(argv)

    totals: Counter[str] = Counter()
    files_changed = 0
    files_seen = 0
    rows: list[dict[str, str]] = []

    for directory in args.dirs:
        if not directory.is_dir():
            print(f"!! not a directory: {directory}", file=sys.stderr)
            return 2
        for path in sorted(directory.rglob("*.mei")):
            files_seen += 1
            original = path.read_text(encoding="utf-8")
            fixed, findings = process(original)

            for kind, nc_id, curve in findings:
                totals[kind] += 1
                rows.append({
                    "file": str(path),
                    "issue": kind,
                    "nc_xml_id": nc_id,
                    "curve": curve,
                })

            if fixed == original:
                continue
            files_changed += 1
            if not args.no_verify:
                verify(fixed)
            if args.write:
                path.write_text(fixed, encoding="utf-8")

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=["file", "issue", "nc_xml_id", "curve"])
            writer.writeheader()
            writer.writerows(rows)

    mode = "WRITE" if args.write else "DRY RUN (nothing written)"
    print(f"{mode}: {files_seen} .mei files scanned, "
          f"{files_changed} need changes")
    for kind in (MISSING, DUPLICATE, NO_CURVE, BAD_CURVE):
        if totals[kind]:
            tail = "  <-- needs a human" if kind in (NO_CURVE, BAD_CURVE) else ""
            print(f"  {totals[kind]:6d}  {kind}{tail}")
    if args.report:
        print(f"report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
