import sys
import argparse
from .parser import (
    extract_pdf_pages, 
    extract_pdf_pages_parallel,
    ocr_pdf, 
    ocr_pdf_parallel,
    batch_ocr_pdf,
    save_as_json
)


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
    
    # Add new performance-related arguments
    parser.add_argument(
        "--dpi", 
        type=int, 
        default=200, 
        help="DPI for image rendering during OCR (default: 200). Lower values are faster."
    )
    parser.add_argument(
        "--parallel", 
        action="store_true", 
        help="Use parallel processing for faster extraction"
    )
    parser.add_argument(
        "--max-workers", 
        type=int, 
        default=None, 
        help="Maximum number of parallel workers (default: auto-detected based on CPU cores)"
    )
    parser.add_argument(
        "--batch", 
        action="store_true", 
        help="Use batch processing instead of parallel (more memory efficient for large PDFs)"
    )
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=5, 
        help="Number of pages to process in each batch (default: 5)"
    )
    parser.add_argument(
        "--ocr-threshold", 
        type=int, 
        default=50, 
        help="Minimum characters required to skip OCR (default: 50)"
    )
    parser.add_argument(
        "--gpu", 
        action="store_true", 
        help="Enable GPU acceleration for OCR (if available)"
    )

    args = parser.parse_args()

    try:
        # For OCR-only mode
        if args.ocr_only:
            if args.parallel:
                extracted_text = ocr_pdf_parallel(
                    args.pdf_path, 
                    args.start_page, 
                    args.end_page,
                    lang=args.lang,
                    dpi=args.dpi,
                    max_workers=args.max_workers,
                    use_gpu=args.gpu
                )
            elif args.batch:
                extracted_text = batch_ocr_pdf(
                    args.pdf_path, 
                    args.start_page, 
                    args.end_page,
                    lang=args.lang,
                    dpi=args.dpi,
                    batch_size=args.batch_size,
                    use_gpu=args.gpu
                )
            else:
                extracted_text = ocr_pdf(
                    args.pdf_path, 
                    args.start_page, 
                    args.end_page,
                    lang=args.lang,
                    dpi=args.dpi,
                    use_gpu=args.gpu
                )
        # For regular mode with OCR fallback
        else:
            if args.parallel:
                extracted_text = extract_pdf_pages_parallel(
                    args.pdf_path, 
                    args.start_page, 
                    args.end_page,
                    lang=args.lang,
                    dpi=args.dpi,
                    max_workers=args.max_workers,
                    ocr_threshold=args.ocr_threshold,
                    use_gpu=args.gpu
                )
            else:
                extracted_text = extract_pdf_pages(
                    args.pdf_path, 
                    args.start_page, 
                    args.end_page,
                    lang=args.lang,
                    dpi=args.dpi,
                    ocr_threshold=args.ocr_threshold,
                    use_gpu=args.gpu
                )
        
        if args.output:
            save_as_json(extracted_text, args.output)
            print(f"Text extracted and saved to {args.output} in JSON format.")
        else:
            print(extracted_text)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()