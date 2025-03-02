# Data Flow Tool

A modern data lineage visualization tool that helps you understand column-level dependencies between your data tables.

## Features

- Interactive visualization of data lineage
- Column-level dependency tracking
- Support for DBT projects
- Dark/Light mode
- Interactive column highlighting
- Draggable nodes
- Detailed tooltips with metadata

## Installation

```bash
pip install dataflowtool
```

## Usage

1. From the command line:
```bash
dataflowtool
```
This will start the server and open the visualization in your default web browser.

2. As a Python module:
```python
from dataflowtool.dataflowtool.server import run_server

run_server()
```

## DBT Integration

The tool automatically detects DBT projects in the current directory or its parents. If a DBT project is found, it will use the manifest.json and catalog.json files to generate the lineage visualization.

If no DBT project is found, the tool will use sample data to demonstrate its functionality.

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dataflowtool.git
cd dataflowtool
```

2. Install dependencies:
```bash
pip install -e .
cd frontend
npm install
```

3. Build the frontend:
```bash
npm run build
```

4. Run the development server:
```bash
python dataflowtool/server.py
```

## License

MIT License 