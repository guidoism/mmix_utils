import delegator, re
from more_itertools import padded

def parse_source(name):
    "Parse <name.mms> and <name.mmo> in the current directory and return a tuple of dictionaries"
    mmo = delegator.run(f'mmotype {name}.mmo').out
    matches = re.findall(r'(\w{16}): (\w{8}) .*line (\d+)\)', mmo)
    instructions = {int(c)-1: (a, b) for a, b, c in matches}
    
    lines = [''.join(tweak_quote_spaces(s)) for s in open(f'{name}.mms')]
    lines = [re.split(r'\s+', s.rstrip(), 2) for s in lines]
    lines = [list(padded(s, '', 3)) for s in lines]

    # Memory location -> column index
    column_index = {}
    for i, (a, b, c) in enumerate(lines):
        loc, inst = instructions.get(i, ('', ''))
        column_index[loc] = i

    return (lines, instructions, column_index)
    
    
def tweak_quote_spaces(s):
    q = False
    for c in s:
        if q:
            if c == ' ':
                yield '␣'
                continue
            elif c == '"':
                q = False
        else:
            if c == '"':
                q = True
        yield c
