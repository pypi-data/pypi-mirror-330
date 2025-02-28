# CyVer
[![License](https://img.shields.io/badge/License-CC_BY_NC_4.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
<div align="center">
    <img src="https://gitlab.com/netmode/CyVer/-/raw/main/logoCyVer.jpg?ref_type=heads" alt="CyVer" width="300">
</div>



**CyVer** is a Python library designed to validate Cypher queries against a given Knowledge Graph schema in Neo4j. It ensures correctness in terms of syntax, schema validity, and property access. 

## Features

* **Syntax Validation**: Validates Cypher queries for correct syntax and detects conflicting labels in nodes and relationships.

* **Schema Validation**: Checks query alignment with a predefined KG schema structure.

* **Property Validation**: Ensures property accesses are correct based on the predefined KG schema structure.

## 📋 Requirements

The following Python packages need to be installed (with Python version >= 3.10)):

* regex>=2024.11.6
* pandas>=2.2.3
* neo4j>=5.27


## 📦 Installation

To install the latest stable version, run:

```sh
pip install git+https://gitlab.com/netmode/CyVer.git
```

or manually,  clone the repo and run:

```sh
cd CyVer
pip install .
```



## 💻 Example Usage 

### Importing the Library

``` sh
import CyVer
from CyVer.validators import SyntaxValidator,PropertiesValidator,SchemaValidator
```

### Connect to Neo4j Database instance
```sh
from neo4j import GraphDatabase,basic_auth

driver = GraphDatabase.driver(database_url, auth=basic_auth(database_username, database_password))
```

### Syntax Validator

```sh
syntax_validator =  SyntaxValidator(driver)
query = 'MATCH (g:Goal) RETURN COUNT(g) AS output'
is_valid = syntax_validator.validate(query)
print(f"Syntax Valid: {is_valid}")
```

### Schema Validator
```sh
schema_validator =  SchemaValidator(driver)
query = 'MATCH (g:Goal)-[:HAS_TARGET]->(t:Target) RETURN g, t'
# Extraction
extracted = schema_validator.extract(query)
print(f"Extracted Nodes, relationships: {extracted}")
# Validation 
schema_score = schema_validator.validate(query)
print(f"Schema Validation Score: {schema_score}")

```


### Properties Validator
```sh
props_validator =  PropertiesValidator(driver)
query = 'MATCH (g:Goal)-[:HAS_TARGET]-(t:Target) WHERE g.code =1 RETURN t'
# Extraction
extracted_props = props_validator.extract(query,strict=True)
print(f"Extracted prperties: {extracted_props}")
# Validation 
props_score = props_validator.validate(query)
print(f"Properties Validation Score: {props_score}")
```

## <img src=https://cdn.jsdelivr.net/gh/Readme-Workflows/Readme-Icons@main/icons/octicons/Wiki.svg width=25> Documentation

For documentation read [Wiki](https://gitlab.com/netmode/CyVer/-/wikis/CyVer-Documentation).
## License

This project is licensed under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license.

## 🤝 Contributing

Contributions are welcome! Please submit a pull request or open an issue.

## Cite

To cite this work, please use:

## Contact

For any request for detailed information or expression of interest for participating at this initiative, you may contact:

- Ioanna Mandilara - ioannamand (at) netmode (dot) ntua (dot) gr
- Christina Maria Androna - andronaxm (at) netmode (dot) ntua (dot) gr
- Eleni Fotopoulou - efotopoulou (at) netmode (dot) ntua (dot) gr
- Anastasios Zafeiropoulos - tzafeir (at) cn (dot) ntua (dot) gr

---