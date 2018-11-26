import os

import pybibs

bib_string = """
@article{key1,
  author = "Israel, Moshe",
  title = "Some title",
  year = 2008
}

@inproceedings{key2,
  author = "Israel, Moshe",
  title = "Some title",
  year = 2009
}
""".strip()

raw_entry_key_values = """
author = "Israel, Moshe",
title = "Some title",
year = 2008
"""


def test_read_string():
    bib = pybibs.read_string(bib_string)
    entry = bib[0]
    assert entry['key'] == 'key1'
    assert entry['type'] == 'article'
    assert entry['fields']['author'] == 'Israel, Moshe'
    assert entry['fields']['year'] == '2008'


def test_read_file():
    filepath = os.path.join('tests', 'data', 'huge.bib')
    bib = pybibs.read_file(filepath)
    for entry in bib:
        if entry['key'] == 'bailenson2005digital':
            break
    else:
        raise AssertionError('Couldn\'t find bailenson2005digital in parsed data')


def test_split_entries():
    raw_entries = list(pybibs._split_entries(bib_string))
    assert len(raw_entries) == 2


def test_entry_contains_key_and_type():
    bib = pybibs.read_string(bib_string)
    assert bib[0]['key'] == 'key1'
    assert bib[0].get('type') == 'article'


def test_parse_raw_key_values():
    gen = pybibs._parse_raw_key_values(raw_entry_key_values)
    key, val = next(gen)
    assert key == 'author'
    assert val == 'Israel, Moshe'
    key, val = next(gen)
    assert key == 'title'
    assert val == 'Some title'


def test_parse_value():
    assert pybibs._parse_value(' "Israel, Moshe",\n') == 'Israel, Moshe'
    assert pybibs._parse_value(' 2008\n') == '2008'
