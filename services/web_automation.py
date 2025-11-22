import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from models.candidate import Candidate
from services.logger import get_logger
import config

logger = get_logger(__name__)

class OrangeHRMAutomator:
    """A class to automate interactions with the OrangeHRM website."""

    def __init__(self, headless: bool = True):
        """Initializes the WebDriver."""
        logger.info(f"Initializing WebDriver in {'headless' if headless else 'headed'} mode.")
        self.driver = self._create_driver(headless)
        self.wait = WebDriverWait(self.driver, config.EXPLICIT_WAIT_SECONDS)

    def _create_driver(self, headless: bool) -> WebDriver:
        """Creates and configures a new Chrome WebDriver instance."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080") # Ensure headless has a good resolution
        
        # The new versions of selenium do not require a driver path if the chromedriver is in the path
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(config.IMPLICIT_WAIT_SECONDS)
        return driver

    def login(self, username, password):
        """Logs into OrangeHRM."""
        logger.info("Navigating to login page.")
        self.driver.get(config.ORANGE_HRM_BASE_URL)
        try:
            logger.info("Attempting to log in.")
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username_field.send_keys(username)
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            
            login_button = self.driver.find_element(By.TAG_NAME, "button")
            login_button.click()

            # Wait for the dashboard to be visible
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxd-topbar-header-breadcrumb")))
            logger.info("Login successful.")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Login failed. Page might have changed. Error: {e}")
            self.quit()
            raise

    def navigate_to_recruitment(self):
        """Navigates to the Recruitment module."""
        try:
            logger.info("Navigating to Recruitment page.")
            recruitment_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[.//span[text()="Recruitment"]]'))
            )
            recruitment_link.click()
            # Wait for the recruitment page header to be visible
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxd-table-filter-header-title")))
            logger.info("Successfully navigated to Recruitment page.")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Could not navigate to Recruitment page. Error: {e}")
            self.quit()
            raise

    def click_add_candidate(self):
        """Clicks the 'Add' button to create a new candidate."""
        try:
            logger.info("Clicking 'Add' to create a new candidate.")
            add_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()=" Add "]'))
            )
            add_button.click()
            # Wait for the 'Add Candidate' form header
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//h6[text()="Add Candidate"]')))
            logger.info("On the Add Candidate page.")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Could not click the 'Add' candidate button. Error: {e}")
            self.quit()
            raise

    def fill_candidate_form(self, candidate: Candidate, resume_filepath: str):
        """Fills out the candidate information form."""
        try:
            logger.info(f"Filling form for candidate: {candidate.first_name} {candidate.last_name}")
            # Fill text fields
            self.driver.find_element(By.NAME, "firstName").send_keys(candidate.first_name)
            self.driver.find_element(By.NAME, "lastName").send_keys(candidate.last_name)
            
            # The vacancy field is a dropdown, so we need to interact with it
            vacancy_dropdown = self.driver.find_element(By.XPATH, '//*[@class="oxd-select-wrapper"]')
            vacancy_dropdown.click()
            
            # Wait for dropdown options to be visible
            vacancy_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[@role="listbox"]//span[text()="{candidate.vacancy}"]')))
            vacancy_option.click()


            # The email input is the 5th input in the form
            email_input = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/div/div[1]/div/div[2]/input')
            email_input.send_keys(candidate.email)
            
            # The contact number is the next input field
            contact_input = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/div/div[2]/div/div[2]/input')
            contact_input.send_keys(candidate.contact_number)


            # Upload resume
            resume_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
            # Get absolute path for the resume file
            absolute_resume_path = os.path.abspath(resume_filepath)
            resume_input.send_keys(absolute_resume_path)

            time.sleep(2) # Brief pause for file upload to register

            logger.info(f"Successfully filled form for {candidate.first_name} {candidate.last_name}.")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to fill candidate form. A field may not have been found. Error: {e}")
            self.quit()
            raise

    def save_candidate(self):
        """Saves the candidate information."""
        try:
            logger.info("Saving candidate...")
            save_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            save_button.click()

            # Wait for the "Application Stage" to confirm save
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Application Stage"]')))
            logger.info("Candidate saved successfully.")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to save candidate. Confirmation element not found. Error: {e}")
            self.quit()
            raise
    
    def quit(self):
        """Quits the WebDriver."""
        if self.driver:
            logger.info("Closing the browser.")
            self.driver.quit()
            self.driver = None

