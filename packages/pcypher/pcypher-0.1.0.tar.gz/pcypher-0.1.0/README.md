# pcypher

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

## Overview

Pcypher is a Python library to parse Cypher queries.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage as CLI command](#usage-as-cli-command)
- [Usage as Python library](#usage-as-python-library)
- [Release Notes](#release-notes)
- [Known Issues](#known-issues)
- [License](#license)

## Prerequisites

- Python 3.9 or higher

## Installation

pcypher offers two options of use patterns:

- CLI command to parse Cypher queries
- Python library to parse Cypher queries

As a CLI command, install pcypher with brew.

```bash
brew tap rioriost/pcypher
brew install pcypher
```

As a Python library, install pcypher with pip / uv.

python venv on macOS, Linux
```bash
mkdir your_directory
cd your_directory
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pcypher
```

uv on macOS, Linux
```bash
uv init your_directory
cd your_directory
uv venv
source .venv/bin/activate
uv add pcypher
```

python venv on Windows
```bash
md your_directory
cd your_directory
python -m venv venv
source .\venv\Scripts\activate
python -m pip install pcypher
```

## Usage as CLI command

Execute pcypher command.

```bash
pcypher --help
usage: pcypher [-h] query

positional arguments:
  query       Query to parse

optional arguments:
  -h, --help  show this help message and exit
```

```bash
pcypher "CREATE (adam:User {name: 'Adam'}), (pernilla:User {name: 'Pernilla'}), (david:User {name: 'David'}), (adam)-[:FRIEND]->(pernilla), (pernilla)-[:FRIEND]->(david)"
[('CREATE', [('node', 'adam', ['User'], [('name', 'Adam')]), ('node', 'pernilla', ['User'], [('name', 'Pernilla')]), ('node', 'david', ['User'], [('name', 'David')]), ('chain', ('node', 'adam', [], None), [(('directed', ('relationship', [{'variable': None, 'type': 'FRIEND'}], None, None)), ('node', 'pernilla', [], None))]), ('chain', ('node', 'pernilla', [], None), [(('directed', ('relationship', [{'variable': None, 'type': 'FRIEND'}], None, None)), ('node', 'david', [], None))])])]
```

## Usage as Python library

```python
from pcypher import CypherParser

def main():
    query = "CREATE (adam:User {name: 'Adam'}), (pernilla:User {name: 'Pernilla'}), (david:User {name: 'David'}), (adam)-[:FRIEND]->(pernilla), (pernilla)-[:FRIEND]->(david)"
    parser = CypherParser()
    result = parser.parse(query)
    print(f"{str(result)}")

if __name__ == "__main__":
    main()
```

## Release Notes

### 0.1.0 Release
* Initial release.

## Known Issues
* pcypher is based on the [Cypher Query Language Reference, Version 9](https://s3.amazonaws.com/artifacts.opencypher.org/openCypher9.pdf).
pcypher 0.1.0 can not parse the following four queries in the reference.
```python
    """MATCH (martin:Person {name: 'Martin Sheen'}), (oliver:Person {name: 'Oliver Stone'}), p = shortestPath((martin)-[*..15]-(oliver)) RETURN p""",  # in page 67
    """MATCH (martin:Person {name: 'Martin Sheen'}), (michael:Person {name: 'Michael Douglas'}), p = allShortestPaths((martin)-[*]-(michael)) RETURN p""",  # in page 67
    """MATCH (n:Member) RETURN org.opencypher.function.example.join(collect(n.name)) AS members""",  # in page 193
    """MATCH (n:Member) RETURN org.opencypher.function.example.longestString(n.name) AS member""",  # in page 193
```

## License
MIT License
