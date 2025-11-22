import pandas as pd
import requests
from typing import List
from models.candidate import Candidate
from services.logger import get_logger
import os

logger = get_logger(__name__)

def download_csv(url: str, download_folder: str = 'data'):
    """
    Downloads a file from a URL into a local folder.
    Returns the local file path.
    """
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        
    local_filename = url.split('/')[-1]
    local_path = os.path.join(download_folder, local_filename)

    logger.info(f"Downloading CSV from {url} to {local_path}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        logger.info("Download successful.")
        return local_path
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading CSV from {url}: {e}")
        raise

def read_candidates_from_csv(file_path: str) -> List[Candidate]:
    """
    Reads candidate data from a CSV file using pandas, splitting 'full_name'
    into 'first_name' and 'last_name'.
    """
    candidates = []
    logger.info(f"Reading candidates from CSV: {file_path}")
    try:
        df = pd.read_csv(file_path)

        # Expected columns: full_name,vacancy,email,contact_number,keywords
        if "full_name" not in df.columns:
            logger.error(f"CSV file '{file_path}' is missing the required 'full_name' column.")
            return []

        for index, row in df.iterrows():
            try:
                full_name = row.get('full_name', '').strip()
                # Split full_name into first_name and last_name
                name_parts = full_name.split(' ', 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ''

                candidate_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': row.get('email', ''),
                    'vacancy': row.get('vacancy', ''),
                    'contact_number': row.get('contact_number', ''),
                    'keywords': row.get('keywords', ''),
                    'date_of_application': '', # Default value
                    'notes': '' # Default value
                }
                
                # Handle potential NaN values from pandas
                for key, value in candidate_data.items():
                    if pd.isna(value):
                        candidate_data[key] = ''

                candidates.append(Candidate(**candidate_data))
            except (TypeError, IndexError) as e:
                logger.warning(f"Skipping row {index} due to a data processing error: {e}. Data: {row.to_dict()}")

    except FileNotFoundError:
        logger.error(f"CSV file not found at path: {file_path}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while reading the CSV with pandas: {e}", exc_info=True)
        raise
        
    logger.info(f"Successfully loaded {len(candidates)} candidates.")
    return candidates
