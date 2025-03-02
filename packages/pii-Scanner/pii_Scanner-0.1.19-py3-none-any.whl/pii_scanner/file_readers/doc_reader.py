import json
import logging
import re
import asyncio
from typing import Optional
from unstructured.partition.auto import partition
from pii_scanner.scanners.spacy_matcher_scanner import SpacyMatchScanner

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Removes unwanted punctuation while preserving email-related symbols like @ and . 
    """
    if not text:
        return ""

    # Preserve emails by replacing them temporarily
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    for i, email in enumerate(emails):
        text = text.replace(email, f"EMAIL_PLACEHOLDER_{i}")

    # Remove all unwanted punctuation except @ 
    text = re.sub(r'[^\w\s@-]', '', text)

    # Restore emails
    for i, email in enumerate(emails):
        text = text.replace(f"EMAIL_PLACEHOLDER_{i}", email)

    return text

async def doc_pii_detector(file_path: str, region: Optional[str] = None) -> str:
    """
    Detect PII in DOCX, PDF, or TXT files using NER Scanner.
    """
    scanner = SpacyMatchScanner()  # Initialize your NER Scanner

    try:
        # Extract elements from the document using Unstructured
        elements = partition(filename=file_path)
        logger.info(f"Successfully read and partitioned file: {file_path}")

        # Preprocess each element's text
        texts = [clean_text(element.text) for element in elements if hasattr(element, 'text')]
        combined_text = ' '.join(texts)
        # print(combined_text)
        # Log details
        logger.info(f"Preprocessed {len(texts)} elements. Combined text: {combined_text}")

        # Perform NER scan
        results = await scanner.scan_async(combined_text, region=region)
        
        logger.info("Processing completed successfully.")
        return results

    except FileNotFoundError:
        error_message = f"Error: The file '{file_path}' was not found."
        logger.error(error_message)
        return json.dumps({"error": error_message}, indent=4)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return json.dumps({"error": str(e)}, indent=4)

