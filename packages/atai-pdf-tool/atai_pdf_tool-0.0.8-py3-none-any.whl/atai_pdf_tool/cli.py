import sys
import argparse
from .parser import extract_pdf_pages, ocr_pdf, save_as_json


def main():
    """Main entry point for the command-line tool."""
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files with fallback to OCR."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "-s", "--start-page", 
        type=int, 
        default=0, 
        help="Starting page number (0-indexed, default: 0)"
    )
    parser.add_argument(
        "-e", "--end-page", 
        type=int, 
        default=None, 
        help="Ending page number (0-indexed, default: last page)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output JSON file path (if not provided, prints to stdout)"
    )
    parser.add_argument(
        "--ocr-only", 
        action="store_true", 
        help="Use OCR for all pages regardless of extractable text"
    )
    parser.add_argument(
        "-l", "--lang", 
        default="en", 
        help="Language for OCR (default: en). Use format like 'en', 'ch_sim', 'fr', etc."
    )

    args = parser.parse_args()

    try:
        if args.ocr_only:
            extracted_text = ocr_pdf(
                args.pdf_path, 
                args.start_page, 
                args.end_page,
                lang=args.lang,
            )
        else:
            extracted_text = extract_pdf_pages(
                args.pdf_path, 
                args.start_page, 
                args.end_page,
                lang=args.lang,
            )
        
        if args.output:
            save_as_json(extracted_text, args.output)
            #save_raw_json(extracted_text, 'raw.json')
            print(f"Text extracted and saved to {args.output} in JSON format.")
        else:
            print(extracted_text)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()