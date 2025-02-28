import logging
from typing import Dict, Any, Optional, Union, List
from pii_scanner.utils.xlsx_file import read_all_sheets, extract_column_data, clean_data
from pii_scanner.scanners.ner_scanner import SpacyNERScanner
from pii_scanner.file_readers.process_column import process_column_data

  # Adjust import according to your actual module

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



async def process_sheet(sheet_data: Dict[str, Any], sheet_name: str, columns_to_process: List[str], sample_size: Optional[Union[int, float]], region) -> Dict[str, Any]:
    scanner = SpacyNERScanner()  # Initialize your NER Scanner
    sheet_results = {}

    for col in columns_to_process:
        logger.info(f"Processing column: {col} in sheet: {sheet_name}")
        column_data = extract_column_data(sheet_data, col)
        cleaned_data = clean_data(column_data)
        result = await process_column_data(cleaned_data, scanner, sample_size, region=region)
        sheet_results[col] = result

    return sheet_results

async def xlsx_file_pii_detector(file_path: str, sheet_name: Optional[str] = None, sample_size: Optional[Union[int, float]] = None, region=None) -> Dict[str, Any]:
    """
    Main function to detect PII in an Excel file.
    """
    try:
        # Read all sheets from the Excel file
        all_sheets_data = read_all_sheets(file_path)
        logger.info(f"Successfully read file: {file_path}")

        # Check if any sheet data is empty
        if not all_sheets_data:
            logger.warning("No data found in the file.")
            return {"error": "No data found in the file."}

        # Determine sheet(s) to process
        if sheet_name:
            if sheet_name not in all_sheets_data:
                error_message = f"Error: The sheet '{sheet_name}' was not found in the file."
                logger.error(error_message)
                return {"error": error_message}
            sheets_to_process = {sheet_name: all_sheets_data[sheet_name]}
        else:
            sheets_to_process = all_sheets_data  # Process all sheets if no specific sheet is specified

        # Process each sheet sequentially
        results = {}
        for sheet, data in sheets_to_process.items():
            # Determine columns to process
            column_name = None
            columns_to_process = [column_name] if column_name and column_name in data[0].keys() else list(data[0].keys())
            results[sheet] = await process_sheet(sheet_data=data, sheet_name=sheet_name, columns_to_process=columns_to_process, sample_size=sample_size, region=region)

        logger.info("Processing completed successfully.")
        return results

    except FileNotFoundError:
        error_message = f"Error: The file '{file_path}' was not found."
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {"error": str(e)}

