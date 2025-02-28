# atai-pdf-tool

A command-line tool for parsing and extracting text from PDF files with OCR capabilities and performance optimization options.

## Installation

```bash
pip install atai-pdf-tool
```

## Usage

### Command Line Interface

#### Basic Usage with Default Settings

```bash
atai-pdf-tool path/to/your/document.pdf -o output.json
```

#### Parallel Processing (Faster for Multi-core Systems)

```bash
atai-pdf-tool path/to/your/document.pdf -o output.json --parallel --max-workers 4
```

#### Lower DPI for Faster Processing

```bash
atai-pdf-tool path/to/your/document.pdf -o output.json --dpi 150
```

#### Batch Processing for Large PDFs (Memory-Efficient)

```bash
atai-pdf-tool path/to/your/document.pdf -o output.json --batch --batch-size 10
```

#### OCR-Only Mode with Parallel Processing

```bash
atai-pdf-tool path/to/your/document.pdf -o output.json --ocr-only --parallel --gpu
```

#### Process Specific Page Range with Optimizations

```bash
atai-pdf-tool path/to/your/document.pdf -s 5 -e 15 -o output.json --parallel --dpi 180 --gpu
```

### Options:

- `-s`, `--start-page`: Starting page number (0-indexed, default: 0)
- `-e`, `--end-page`: Ending page number (0-indexed, default: last page)
- `-o`, `--output`: Output JSON file path (if not provided, prints to stdout)
- `--ocr-only`: Use OCR for all pages regardless of extractable text
- `-l`, `--lang`: Language for OCR processing (default: en)
- `--parallel`: Enable parallel processing for faster performance (multi-core systems)
- `--max-workers`: Control the number of parallel workers for processing
- `--dpi`: Control image resolution for OCR (lower DPI improves speed)
- `--batch`: Use memory-efficient batch processing for large PDFs
- `--batch-size`: Control the batch size for batch processing
- `--ocr-threshold`: Set the threshold for when to fallback to OCR
- `--gpu`: Enable GPU acceleration for OCR processing

### Supported Languages

The language option (`-l`, `--lang`) accepts language codes supported by EasyOCR. Some common ones include:

- `en`: English
- `ch_sim`: Simplified Chinese
- `ch_tra`: Traditional Chinese
- `fr`: French
- `de`: German
- `jp`: Japanese
- `ko`: Korean
- `sp`: Spanish

For a complete list of language codes, see the [EasyOCR documentation](https://www.jaided.ai/easyocr/).

### As a Python Module

```python
from atai_pdf_tool.parser import extract_pdf_pages, ocr_pdf, save_as_json

# Extract text from specific pages with English OCR
text = extract_pdf_pages("document.pdf", start_page=0, end_page=5, lang="en")

# Extract text with different language
chinese_text = extract_pdf_pages("chinese_document.pdf", lang="ch_sim")

# Extract without progress bar
text = extract_pdf_pages("document.pdf", show_progress=False)

# Save to JSON
save_as_json(text, "output.json")

# OCR an entire PDF with a specific language
french_ocr_text = ocr_pdf("french_document.pdf", lang="fr")
```

## Key Improvements and Performance Enhancements

- **Parallel Processing**: Use multiple CPU cores for faster processing of large PDFs.
- **DPI Control**: Adjust the resolution for OCR processing to balance speed and quality (`--dpi`).
- **Batch Processing**: Process large PDFs in memory-efficient batches (`--batch`, `--batch-size`).
- **GPU Acceleration**: Leverage GPU resources for OCR processing (`--gpu`).
- **OCR Threshold**: Set a configurable threshold for when to switch to OCR processing (`--ocr-threshold`).
- **Reused OCR Reader**: Optimized OCR integration for better speed, especially with multi-page documents.

These updates allow you to customize the extraction process based on hardware capabilities, whether you're looking for faster processing or better memory efficiency.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---