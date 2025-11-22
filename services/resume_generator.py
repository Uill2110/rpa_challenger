import os
from models.candidate import Candidate
from services.logger import get_logger

logger = get_logger(__name__)

def generate_resume_file(candidate: Candidate, output_dir: str) -> str:
    """Creates a TXT file with candidate details and returns its path."""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created resume directory: {output_dir}")

        # Sanitize filename
        first_name = "".join(c for c in candidate.first_name if c.isalnum() or c in (' ', '_')).rstrip()
        last_name = "".join(c for c in candidate.last_name if c.isalnum() or c in (' ', '_')).rstrip()
        filename = f"{first_name}_{last_name}_resume.txt"
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(f"Resume for: {candidate.first_name} {candidate.last_name}\n")
            f.write("-" * 20 + "\n")
            f.write(f"Email: {candidate.email}\n")
            f.write(f"Contact Number: {candidate.contact_number}\n")
            f.write(f"Applying for Vacancy: {candidate.vacancy}\n")
            f.write(f"Date of Application: {candidate.date_of_application}\n")
            f.write("\n")
            f.write("Keywords:\n")
            f.write(f"{candidate.keywords}\n")
            f.write("\n")
            f.write("Notes:\n")
            f.write(f"{candidate.notes}\n")

        logger.info(f"Generated resume file for {candidate.first_name} {candidate.last_name} at {file_path}")
        return file_path
    except IOError as e:
        logger.error(f"Failed to generate resume file for {candidate.first_name} {candidate.last_name}: {e}")
        raise
