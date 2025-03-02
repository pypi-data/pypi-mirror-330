import json
import logging
import time
from pii_scanner.scanners.ner_scanner import SpacyNERScanner
from typing import Dict, Any, Optional, Union, List
from pii_scanner.utils.csv_file import read_csv, extract_column_data, clean_data
from pii_scanner.file_readers.process_column import process_column_data

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def csv_file_pii_detector(file_path: str, sample_size: Optional[Union[int, float]] = None, region=None) -> Dict[str, Any]:
    """
    Detects PII in a CSV file and logs the time taken by each step.
    """
    scanner = SpacyNERScanner()  # Initialize your NER Scanner
    
    start_time = time.time()
    
    try:
        # Read CSV file
        read_start = time.time()
        data = read_csv(file_path)
        read_end = time.time()
        logger.info(f"Successfully read file: {file_path} (Time taken: {read_end - read_start:.4f} sec)")
        
        # Check if data is empty
        if not data:
            logger.warning("No data found in the file.")
            return {"error": "No data found in the file."}

        # Initialize a dictionary to store results
        results = {}

        column_name = None
        # Process the specified column or all columns if not specified
        columns_to_process = [column_name] if column_name and column_name in data[0] else list(data[0].keys())

        # Process each column sequentially
        for col in columns_to_process:
            col_start = time.time()
            logger.info(f"Processing column: {col}")
            try:
                extract_start = time.time()
                column_data = clean_data(extract_column_data(data, col))
                extract_end = time.time()
                
                process_start = time.time()
                result = await process_column_data(column_data, scanner, sample_size, region=region)
                process_end = time.time()
                
                results[col] = result
                logger.info(f"Processed column: {col} (Extraction time: {extract_end - extract_start:.4f} sec, Processing time: {process_end - process_start:.4f} sec)")
            except Exception as e:
                logger.error(f"Error processing column: {col} - {e}")
                results[col] = {"error": str(e)}
            col_end = time.time()
            logger.info(f"Total time for column {col}: {col_end - col_start:.4f} sec")

        total_time = time.time() - start_time
        logger.info(f"Processing completed successfully. Total execution time: {total_time:.4f} sec")
        return results

    except FileNotFoundError:
        error_message = f"Error: The file '{file_path}' was not found."
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {"error": str(e)}
