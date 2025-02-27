# ATAI Image Tool

A command line tool to extract text from images using OCR and either save the results as JSON or print to console.

## Installation

```bash
pip install atai-image-tool
```

## Usage

```bash
# Basic usage with output to JSON file
atai-image-tool input.jpg output.json

# Print OCR results to console (no output file)
atai-image-tool input.jpg

# Specify languages (default is English), other languages need to download the models
atai-image-tool input.jpg output.json --languages ch_sim

# Show help
atai-image-tool --help
```

## Python API

You can also use ATAI Image Tool as a Python library:

```python
from atai_image_tool import extract_image_content, save_as_json

# Extract text from an image
text = extract_image_content("input.jpg")

# Print the text
print(text)

# Or save the text as JSON
save_as_json(text, "output.json")
```

## License

MIT