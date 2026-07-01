# PDF Splitter

A lightweight command-line tool to split a PDF document into multiple files at
variable page ranges. Built with [PyPDF2](https://pypdf2.readthedocs.io/).

## Features

- Split a PDF into multiple files using custom, variable page ranges.
- Accepts ranges (`1-3`), single pages (`5`), or a mix (`1-3,4,5-8`).
- Automatically clamps ranges to valid page numbers and skips invalid ones.
- Simple CLI interface — no code changes required to run different splits.
- Container-ready with Docker and CI-ready with Azure Pipelines.

## Requirements

- Python 3.9+
- Dependencies listed in [`requirements.txt`](requirements.txt)

## Installation

```powershell
# Clone the repository
git clone <your-repo-url>
cd PDF_Splitter

# (Optional) create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Usage

```powershell
python main.py --input <path-to-pdf> --output <output-folder> --ranges "<ranges>"
```

### Arguments

| Argument         | Short | Default             | Description                                              |
| ---------------- | ----- | ------------------- | -------------------------------------------------------- |
| `--input`        | `-i`  | `data/input.pdf`    | Path to the input PDF file.                              |
| `--output`       | `-o`  | `data/split_output` | Output folder for the split files.                       |
| `--ranges`       | `-r`  | _required_          | Page ranges to split at, e.g. `"1-3,4-7,8-10"` or `"5"`. |

### Examples

```powershell
# Split into three parts: pages 1-3, 4-7 and 8-10
python main.py --ranges "1-3,4-7,8-10"

# Use a custom input file and output folder
python main.py -i data/input.pdf -o data/split_output -r "1-5,6"

# Extract single pages and a range
python main.py -r "1,2,5-8"
```

Output files are named using the pattern:

```
document_part_<index>_pages_<start>-<end>.pdf
```

## Project Structure

```
PDF_Splitter/
├── data/
│   └── split_output/        # Generated split PDFs
├── main.py                  # CLI entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container image definition
├── azure-pipelines.yml      # CI/CD pipeline
└── README.md
```

## Running with Docker

Build the image:

```powershell
docker build -t pdf-splitter .
```

Run the container, mounting a local `data` folder so the tool can read the input
PDF and write the output:

```powershell
docker run --rm -v ${PWD}/data:/app/data pdf-splitter --ranges "1-3,4-7"
```

## Continuous Integration

This repository includes an [Azure Pipelines](azure-pipelines.yml) definition
that:

1. Sets up Python.
2. Installs dependencies from `requirements.txt`.
3. Performs a syntax/build check of the source.
4. Builds the Docker image.

## License

This project is provided as-is. Add your preferred license here.
