import os
from services.logger import get_logger
from utils.file_utils import cleanup_directory
import config
import credentials
import services.data_provider as data_provider
import services.resume_generator as resume_generator
from services.web_automation import OrangeHRMAutomator

# Setup logger
logger = get_logger(__name__)

def setup_environment():
    """Ensures necessary directories exist and cleans up previous runs."""
    logger.info("Setting up environment...")
    # Create output directories if they don't exist
    os.makedirs(config.RESUME_OUTPUT_PATH, exist_ok=True)
    log_dir = os.path.dirname(config.LOG_FILE_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    # Clean the resume output directory before starting
    cleanup_directory(config.RESUME_OUTPUT_PATH)
    logger.info("Environment setup complete.")

def main():
    """Main orchestrator for the RPA process."""
    setup_environment()
    logger.info("RPA Challenge started.")

    automator = None
    successful_candidates = 0
    failed_candidates = []

    try:
        # 1. Get candidate data from CSV
        logger.info(f"Reading candidates from '{config.CANDIDATES_CSV_URL}'...")
        candidates = data_provider.read_candidates_from_csv(config.CANDIDATES_CSV_URL)
        total_candidates = len(candidates)
        logger.info(f"Found {total_candidates} candidates to process.")

        if not candidates:
            logger.warning("No candidates found to process. Exiting.")
            return

        # 2. Initialize the web automator
        automator = OrangeHRMAutomator(headless=config.HEADLESS_MODE)

        # 3. Login
        automator.login(credentials.ORANGE_HRM_USERNAME, credentials.ORANGE_HRM_PASSWORD)

        # 4. Process each candidate
        for i, candidate in enumerate(candidates, 1):
            candidate_name = f"{candidate.first_name} {candidate.last_name}"
            logger.info(f"Processing candidate {i}/{total_candidates}: {candidate_name}")
            
            try:
                # Navigate to the recruitment section and click add
                automator.navigate_to_recruitment()
                automator.click_add_candidate()

                # Generate a temporary resume file
                resume_path = resume_generator.generate_resume_file(candidate, config.RESUME_OUTPUT_PATH)

                # Fill the form
                automator.fill_candidate_form(candidate, resume_path)

                # Save the candidate
                automator.save_candidate()

                logger.info(f"Successfully processed candidate: {candidate_name}")
                successful_candidates += 1

            except Exception as e:
                logger.error(f"Failed to process candidate {candidate_name}. Error: {e}", exc_info=True)
                failed_candidates.append(candidate_name)
                logger.info("Attempting to recover by re-logging in...")
                if automator:
                    automator.quit()
                automator = OrangeHRMAutomator(headless=config.HEADLESS_MODE)
                automator.login(credentials.ORANGE_HRM_USERNAME, credentials.ORANGE_HRM_PASSWORD)


    except Exception as e:
        logger.critical(f"A critical error occurred in the main process: {e}", exc_info=True)
    finally:
        # 5. Quit the browser
        if automator:
            automator.quit()

        # 6. Final report
        logger.info("="*30)
        logger.info("RPA Process Finished - Summary")
        logger.info("="*30)
        logger.info(f"Total candidates: {len(candidates) if 'candidates' in locals() else 0}")
        logger.info(f"Successfully processed: {successful_candidates}")
        logger.info(f"Failed: {len(failed_candidates)}")
        if failed_candidates:
            logger.warning("Failed candidates list:")
            for name in failed_candidates:
                logger.warning(f"- {name}")
        logger.info("="*30)
        
        # 7. Final cleanup
        cleanup_directory(config.RESUME_OUTPUT_PATH)

if __name__ == "__main__":
    main()