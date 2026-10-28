#!/usr/bin/env python3
"""json2csv: convert a JSON array of flat objects to CSV (stdlib only).
Usage: python json2csv.py input.json output.csv
"""
import csv, json, sys

def convert(records):
    if not isinstance(records, list):
        raise ValueError("top-level JSON must be an array of objects")
    fields = []
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("every array item must be an object")
        for k in r:
            if k not in fields:
                fields.append(k)
    rows = []
    for r in records:
        row = {}
        for k in fields:
            v = r.get(k, "")
            if v is None:
                v = ""
            elif isinstance(v, (dict, list)):
                v = json.dumps(v, ensure_ascii=False)
            row[k] = v
        rows.append(row)
    return fields, rows

def json_to_csv(src, dst):
    with open(src, encoding="utf-8-sig") as f:
        fields, rows = convert(json.load(f))
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return len(rows)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print(f"wrote {json_to_csv(sys.argv[1], sys.argv[2])} rows")
