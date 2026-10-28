import csv, json
from json2csv import json_to_csv
from csv2json import csv_to_json, parse

def test_missing_keys(tmp_path):
    s = tmp_path/"a.json"; d = tmp_path/"a.csv"
    s.write_text(json.dumps([{"a":1,"b":2},{"b":3,"c":"x"}]))
    assert json_to_csv(s, d) == 2
    rows = list(csv.DictReader(open(d, newline="")))
    assert rows == [{"a":"1","b":"2","c":""},{"a":"","b":"3","c":"x"}]

def test_escaping_unicode(tmp_path):
    s = tmp_path/"a.json"; d = tmp_path/"a.csv"
    s.write_text(json.dumps([{"t":'he said "hi", ok\nbye',"u":"caf\u00e9"}]), encoding="utf-8")
    json_to_csv(s, d)
    r = list(csv.DictReader(open(d, newline="", encoding="utf-8")))[0]
    assert r["t"] == 'he said "hi", ok\nbye' and r["u"] == "caf\u00e9"

def test_empty(tmp_path):
    s = tmp_path/"a.json"; d = tmp_path/"a.csv"
    s.write_text("[]"); assert json_to_csv(s, d) == 0

def test_semicolon_bom_infer(tmp_path):
    s = tmp_path/"a.csv"; d = tmp_path/"a.json"
    s.write_bytes("\ufeffname;age;ok\nAnn;30;true\nBob;;false\n".encode("utf-8"))
    csv_to_json(s, d, infer=True)
    assert json.load(open(d)) == [{"name":"Ann","age":30,"ok":True},{"name":"Bob","age":None,"ok":False}]

def test_quoted_newline():
    assert parse('a,b\n"x\ny","1,2"\n') == [{"a":"x\ny","b":"1,2"}]
