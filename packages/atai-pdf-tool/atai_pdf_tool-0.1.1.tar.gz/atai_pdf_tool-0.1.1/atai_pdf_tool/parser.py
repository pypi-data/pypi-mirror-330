import re
import json
import io
import os
import tempfile
from typing import Optional, Dict, Any

import fitz  # PyMuPDF
import easyocr
from PIL import Image
from PyPDF2 import PdfReader
from tqdm import tqdm

import concurrent.futures
import multiprocessing


def extract_text_with_ocr(pdf_path: str, page_num: int, reader=None, lang: str = "en", 
                         dpi: int = 200, use_gpu: bool = False) -> str:
    """Extract text from a PDF page using OCR with optimizations."""
    # Reuse reader if provided (for batch processing)
    if reader is None:
        reader = easyocr.Reader([lang], gpu=use_gpu)
    
    # Read page as image with configurable DPI
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=dpi)
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    
    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_img_path = temp_file.name
        img.save(temp_img_path)
        
    # Extract text using EasyOCR
    result = reader.readtext(temp_img_path)
    
    # Combine the text from the OCR results into a single string
    text = ' '.join([item[1] for item in result])
    
    # Clean up the temporary image file
    os.remove(temp_img_path)
    
    return text


def is_valid_text(text: str) -> bool:
    """Check if extracted text is valid."""
    # Basic cleaning, remove excessive whitespace
    cleaned_text = re.sub(r'[\t\r\n]+', ' ', text).strip()
    # Check if text contains enough English word characters and numbers
    if re.search(r'[A-Za-z0-9]{3,}', cleaned_text):
        return True
    # Check if text contains meaningful sentences
    if re.search(r'([A-Za-z]+ ){2,}', cleaned_text):
        return True
    return False


def extract_pdf_pages(pdf_path: str, start_page: int = 0, end_page: Optional[int] = None, 
                     lang: str = "en", dpi: int = 200, ocr_threshold: int = 50, 
                     use_gpu: bool = False) -> str:
    """Extract text from PDF pages, using OCR if necessary."""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        if start_page < 0 or start_page >= total_pages:
            print(f"Invalid start page number. Using 0 instead of {start_page}.")
            start_page = 0
            
        if end_page is None:
            end_page = total_pages - 1
        elif end_page < start_page or end_page >= total_pages:
            print(f"Invalid end page number. Using {total_pages - 1} instead of {end_page}.")
            end_page = total_pages - 1
            
        text = ''
        page_range = range(start_page, end_page + 1)
        
        # Initialize OCR reader once (reuse for all pages)
        reader = easyocr.Reader([lang], gpu=use_gpu) if use_gpu else None
        
        iterator = tqdm(page_range, desc="Extracting text", unit="page")

        for page_num in iterator:
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            # Use simpler validation with threshold
            if page_text and len(page_text.strip()) > ocr_threshold:
                text += page_text
            else:
                # If text extraction fails or minimal text, use OCR
                iterator.set_description(f"Using OCR on page {page_num}")
                text += extract_text_with_ocr(pdf_path, page_num, reader, lang=lang, dpi=dpi, use_gpu=use_gpu)
        
        return text

def extract_pdf_pages_parallel(pdf_path: str, start_page: int = 0, end_page: Optional[int] = None, 
                              lang: str = "en", dpi: int = 200, ocr_threshold: int = 50, 
                              max_workers: Optional[int] = None, use_gpu: bool = False) -> str:
    """Extract text from PDF pages in parallel, using OCR if necessary."""
    # Determine number of workers based on CPU cores if not specified
    if max_workers is None:
        max_workers = min(multiprocessing.cpu_count(), 4)  # Limit to prevent excessive memory usage
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        if start_page < 0 or start_page >= total_pages:
            print(f"Invalid start page number. Using 0 instead of {start_page}.")
            start_page = 0
            
        if end_page is None:
            end_page = total_pages - 1
        elif end_page < start_page or end_page >= total_pages:
            print(f"Invalid end page number. Using {total_pages - 1} instead of {end_page}.")
            end_page = total_pages - 1
        
        # Create arguments for parallel processing
        page_range = range(start_page, end_page + 1)
        args_list = [(pdf_path, page_num, lang, dpi, ocr_threshold, use_gpu) for page_num in page_range]
        
        # Process pages in parallel with progress bar
        results = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Map maintains the order of submission
            futures_to_page = {executor.submit(process_page, args): args[1] for args in args_list}
            
            for future in tqdm(concurrent.futures.as_completed(futures_to_page), 
                              total=len(futures_to_page), desc="Extracting text", unit="page"):
                page_num = futures_to_page[future]
                text = future.result()
                results.append((page_num, text))
        
        # Sort results by page number to maintain order
        results.sort(key=lambda x: x[0])
        return ''.join([text for _, text in results])       

def process_page(args):
    """Process a single page for parallel execution."""
    pdf_path, page_num, lang, dpi, ocr_threshold, use_gpu = args
    
    # Try standard extraction first
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    page_text = page.get_text()
    
    # Quick check if text is valid
    if len(page_text.strip()) > ocr_threshold:
        return page_text
    
    # If text extraction fails or returns minimal text, use OCR
    reader = easyocr.Reader([lang], gpu=use_gpu)
    return extract_text_with_ocr(pdf_path, page_num, reader, lang, dpi, use_gpu)


def clean_text(text: str) -> str:
    """Clean and escape text for JSON formatting, without altering non-ASCII characters like Chinese."""
    
    # First, remove non-ASCII characters in general, but preserve Chinese characters
    cleaned_text = ''.join(char for char in text if ord(char) < 128 or ord(char) > 127)
    
    # Remove unwanted control characters (like tabs, newlines, etc.), but leave Chinese intact
    cleaned_text = clean_control_characters(cleaned_text)
    
    # Clean up other unnecessary characters
    cleaned_text = cleaned_text.replace('"', "'")  # Replace quotes with single quotes
    cleaned_text = cleaned_text.replace("\\", "\\\\")  # Escape backslashes
    cleaned_text = cleaned_text.replace("\"", "\\\"")  # Escape double quotes
    
    # Remove excessive whitespaces (spaces, tabs, newlines)
    cleaned_text = re.sub(r'[\t\r\n]+', ' ', cleaned_text).strip()
    
    return cleaned_text

def clean_control_characters(s: str) -> str:
    """Clean control characters from a string."""
    cleaned = ""
    for char in s:
        # Handle ASCII control characters
        if ord(char) < 32:
            # Allow newlines, carriage returns, and tabs, but escape them
            if char in '\n\r\t':
                cleaned += char.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
        else:
            # Add other characters directly (including non-ASCII)
            cleaned += char
    return cleaned


def save_as_json(text: str, output_file: str) -> None:
    """Save extracted text as JSON."""
    cleaned_text = clean_text(text)
    data = {"text": cleaned_text}
    
    # Open the output file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def save_raw_json(text: str, output_file: str) -> None:
    """Save raw extracted text as JSON."""
    data = {"text": text}
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)



def ocr_pdf(pdf_path: str, start_page: int = 0, end_page: Optional[int] = None, 
           lang: str = "en", dpi: int = 200, use_gpu: bool = False) -> str:
    """Extract text from an entire PDF using OCR, with support for page range."""
    doc = fitz.open(pdf_path)
    text = ""
    
    # If end_page is None, process all pages from start_page
    total_pages = len(doc)
    if end_page is None or end_page >= total_pages:
        end_page = total_pages - 1
    
    # Initialize EasyOCR reader
    reader = easyocr.Reader([lang], gpu=use_gpu)

    # Wrap with tqdm for progress bar if requested
    page_range = range(start_page, end_page + 1)
    iterator = tqdm(page_range, desc="OCR processing", unit="page")

    for page_num in iterator:
        # Get page
        page = doc.load_page(page_num)
        
        # Get image from page with configurable DPI
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))

        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_img_path = temp_file.name
            img.save(temp_img_path)

        # Extract text using EasyOCR
        result = reader.readtext(temp_img_path)
        
        # Combine the text from the OCR results into a single string
        page_text = ' '.join([item[1] for item in result])
        text += page_text
        
        # Clean up the temporary image file
        os.remove(temp_img_path)
    
    return text


def ocr_pdf_parallel(pdf_path: str, start_page: int = 0, end_page: Optional[int] = None, 
                   lang: str = "en", dpi: int = 200, max_workers: Optional[int] = None,
                   use_gpu: bool = False) -> str:
    """Extract text from an entire PDF using OCR in parallel."""
    # Determine number of workers
    if max_workers is None:
        max_workers = min(multiprocessing.cpu_count(), 4)
    
    doc = fitz.open(pdf_path)
    
    # If end_page is None, process all pages from start_page
    total_pages = len(doc)
    if end_page is None or end_page >= total_pages:
        end_page = total_pages - 1
    
    # Create arguments for parallel processing
    page_range = range(start_page, end_page + 1)
    
    def process_ocr_page(page_num):
        # Create reader per process to avoid sharing issues
        reader = easyocr.Reader([lang], gpu=use_gpu)
        return extract_text_with_ocr(pdf_path, page_num, reader, lang, dpi, use_gpu)
    
    # Process pages in parallel with progress bar
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and keep track of page numbers
        future_to_page = {executor.submit(process_ocr_page, page_num): page_num for page_num in page_range}
        
        for future in tqdm(concurrent.futures.as_completed(future_to_page), 
                         total=len(future_to_page), desc="OCR processing", unit="page"):
            page_num = future_to_page[future]
            text = future.result()
            results.append((page_num, text))
            
    # Sort results by page number to maintain order
    results.sort(key=lambda x: x[0])
    return ''.join([text for _, text in results])


def batch_ocr_pdf(pdf_path: str, start_page: int = 0, end_page: Optional[int] = None, 
                 lang: str = "en", dpi: int = 200, batch_size: int = 5,
                 use_gpu: bool = False) -> str:
    """Extract text with OCR in batches for better performance."""
    doc = fitz.open(pdf_path)
    text = ""
    
    # If end_page is None, process all pages from start_page
    total_pages = len(doc)
    if end_page is None or end_page >= total_pages:
        end_page = total_pages - 1
    
    # Initialize EasyOCR reader (use once)
    reader = easyocr.Reader([lang], gpu=use_gpu)

    # Process pages in batches
    page_range = range(start_page, end_page + 1)
    
    # Process in batches with progress bar
    with tqdm(total=len(page_range), desc="Batch OCR processing", unit="page") as pbar:
        for i in range(start_page, end_page + 1, batch_size):
            batch_pages = range(i, min(i + batch_size, end_page + 1))
            
            # Prepare batch images
            images = []
            temp_paths = []
            
            for page_num in batch_pages:
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=dpi)
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    temp_img_path = temp_file.name
                    img.save(temp_img_path)
                    temp_paths.append(temp_img_path)
                    images.append(temp_img_path)
            
            # Process batch with OCR
            batch_results = []
            for img_path in images:
                result = reader.readtext(img_path)
                page_text = ' '.join([item[1] for item in result])
                batch_results.append(page_text)
            
            # Add to final text
            text += ''.join(batch_results)
            
            # Clean up temporary files
            for temp_path in temp_paths:
                os.remove(temp_path)
            
            # Update progress bar
            pbar.update(len(batch_pages))
    
    return text