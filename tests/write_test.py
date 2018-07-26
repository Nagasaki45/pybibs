import pybibs

expected_entry_output = """
@article{key,
  author = {Israel, Moshe},
  year = {2008}
}
""".strip()


def test_write_entry():
    entry = {
        'key': 'key',
        'type': 'article',
        'author': 'Israel, Moshe',
        'year': '2008',
    }
    assert pybibs._write_entry(entry) == expected_entry_output
