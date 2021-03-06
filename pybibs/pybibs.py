from . import _internals


def read_file(filepath):
    with open(filepath) as f:
        content = f.read()
        return read_string(content)


def write_file(bib, filepath):
    with open(filepath, 'w') as f:
        f.write(write_string(bib))


def read_string(string):
    bib = []
    for raw_entry in _internals.split_entries(string):
        entry = read_entry_string(raw_entry)
        bib.append(entry)
    return bib


def read_entry_string(raw_entry):
    entry = {'fields': {}}
    raw_entry = raw_entry.strip()
    assert raw_entry[0] == '@'
    raw_entry = raw_entry[1:]
    type_, rest = raw_entry.split('{', 1)
    key, rest = rest.split(',', 1)
    assert rest[-1] == '}'
    inner = rest[:-1]
    for k, v in _internals.parse_raw_key_values(inner):
        entry['fields'][k] = v
    entry['key'] = key
    entry['type'] = type_
    return entry


def write_string(bib):
    return '\n\n'.join(_internals.write_entry(entry) for entry in bib)
