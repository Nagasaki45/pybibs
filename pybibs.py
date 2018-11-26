import re

def read_file(filepath):
    with open(filepath) as f:
        content = f.read()
        return read_string(content)


def write_file(bib, filepath):
    with open(filepath, 'w') as f:
        f.write(write_string(bib))


def read_string(string):
    bib = []
    for raw_entry in _split_entries(string):
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
    for k, v in _parse_raw_key_values(inner):
        entry['fields'][k] = v
    entry['key'] = key
    entry['type'] = type_
    return entry


def write_string(bib):
    return '\n\n'.join(_write_entry(entry) for entry in bib)


def _split_entries(string):
    depth = 0
    start = 0
    for i, char in enumerate(string):
        if depth == 0 and char == '@':
            start = i
        if char == '{':
            depth += 1
        if char == '}':
            depth -= 1
            if depth == 0:
                yield string[start:i + 1]


def _parse_raw_key_values(key_values):
    for line in key_values.splitlines():
        if line:
            key, value = line.split('=', 1)
            key = key.strip().lower()
            value = _parse_value(value)
            yield key, value


def _parse_value(value):
    delimiters = [
        '{}',
        '""',
    ]
    value = value.strip()
    if value[-1] == ',':
        value = value[:-1]
    for delimiter in delimiters:
        if value[0] == delimiter[0] and value[-1] == delimiter[-1]:
            value = value[1:-1]
            break
    return value


def _write_entry(entry):
    parts = []
    parts += ['@', entry['type'], '{', entry['key']]
    for k, v in entry['fields'].items():
        parts += [',\n', '  ', k, ' = {', v, '}']
    parts.append('\n}')
    return ''.join(parts)
