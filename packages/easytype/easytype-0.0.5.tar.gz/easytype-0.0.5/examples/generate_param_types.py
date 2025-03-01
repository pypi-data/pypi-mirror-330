from easytype.core import PrimitiveType
from random import choices, choice

all_types = []
sts = [t for t in PrimitiveType.supported_types()]


def to_type_name(t):
    if t == 'any':
        return 'typing.Any'
    if t == 'optional':
        return 'typing.Optional'
    if t == 'union':
        return 'typing.Union'

    return t


for o in ['list', 'optional']:
    for t in sts:
        all_types.append(f"{o}_of_{t}_value={to_type_name(o)}[{to_type_name(t)}],")

for t in sts:
    all_types.append(f"dict_of_{t}_value=dict[str, {to_type_name(t)}],")

for so in ['tuple', 'union']:
    combos = set()
    for i in range(5):
        k = choice([2, 3])
        ps = choices(sts, k=k)
        name_str = '_'.join(ps)
        type_str = ','.join([to_type_name(t) for t in ps])
        combos.add((name_str, type_str))
    for name_str, type_str in combos:
        all_types.append(f"{so}_of_{name_str}_value={to_type_name(so)}[{type_str}],")

for line in all_types:
    print(line)
