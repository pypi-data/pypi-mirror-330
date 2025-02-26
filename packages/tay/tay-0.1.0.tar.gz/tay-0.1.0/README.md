# tay

Python library that provides interface for table formats such as csv, xlsx.


## Quick Start

```sh
pip install tay
```

```python
from dataclasses import dataclass

import tay


@dataclass
class Entity:
    id: int
    name: str


entity = Entity(0, 'sword')
with tay.CSV('entities.csv', 'w') as sheet:
    sheet.write_header(Entity)
    sheet.write_record(entity)
```

```python
import tay

with tay.CSV('entities.csv', 'r') as sheet:
    records = sheet.read(Entity)
```

## Interfaces

Interface name | File type
--- | ---
`CSV` | `.csv`
`Excel` | `.xlsx`
