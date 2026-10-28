#!/usr/bin/env python3
"""csv2json: convert CSV to JSON (stdlib only). Detects delimiter, BOM, encodings.
Usage: python csv2json.py input.csv output.json [--infer] [--ndjson]
"""
import csv, json, sys

def _read(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass

def _infer(v):
    s = v.strip()
    if s == "": return None
    if s.lower() in ("true", "false"): return s.lower() == "true"
    try: return int(s)
    except ValueError: pass
    try: return float(s)
    except ValueError: return v

def parse(text, infer=False):
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    import io
    rows = list(csv.DictReader(io.StringIO(text, newline=""), dialect=dialect))
    if infer:
        rows = [{k: _infer(v) if isinstance(v, str) else v for k, v in r.items()} for r in rows]
    return rows

def csv_to_json(src, dst, infer=False, ndjson=False):
    rows = parse(_read(src), infer)
    with open(dst, "w", encoding="utf-8") as f:
        if ndjson:
            for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
        else:
            json.dump(rows, f, ensure_ascii=False, indent=2)
    return len(rows)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) != 2: sys.exit(__doc__)
    print(f"wrote {csv_to_json(a[0], a[1], '--infer' in sys.argv, '--ndjson' in sys.argv)} rows")
