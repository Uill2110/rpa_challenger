import os
import shutil
from services.logger import get_logger

logger = get_logger(__name__)

def cleanup_directory(directory_path: str):
    """Removes all files and subdirectories within a directory."""
    if not os.path.isdir(directory_path):
        logger.warning(f"Directory to clean not found: {directory_path}")
        return

    logger.info(f"Cleaning up directory: {directory_path}")
    for item_name in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item_name)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            logger.error(f"Failed to delete {item_path}. Reason: {e}")
    logger.info(f"Successfully cleaned directory: {directory_path}")
