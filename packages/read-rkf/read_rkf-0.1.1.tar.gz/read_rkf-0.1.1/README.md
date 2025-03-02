# Read RKF

## Overview

`read_rkf` is a Python script designed to extract and parse essential data from `ams.rkf` files, which store critical results from AMS output files. These files typically contain:

- **Trajectories**
- **Gradients**
- **Hessians**
- **Energies**
- **Band gaps and structures**
- And more...

## Installation

Ensure that you have Python ^3.9 installed and run the following command:

```bash
pip install read_rkf
```

## Usage

### 1. Convert an RKF file to a JSON object

```python
from read_rkf.creat_archive import rkf_to_json

json_data = rkf_to_json("path/to/your.rkf")
```

### 2. Convert an RKF file to a Python dictionary

```python
from read_rkf.creat_archive import rkf_to_dict

python_dict = rkf_to_dict("path/to/your.rkf")
```

### 3. Check available sections in an RKF file

```python
from read_rkf.parserkf import KFFile

data = KFFile("path/to/your.rkf")
all_sections = data.sections()
```

### 4. Read the content of a specific section

```python
# Example: Reading the first section
section_content = data.read_section(all_sections[0])
```

## License

This project is licensed under the MIT License.