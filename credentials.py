import os
from dotenv import load_dotenv

load_dotenv()

ORANGE_HRM_USERNAME = os.getenv("ORANGE_HRM_USERNAME")
ORANGE_HRM_PASSWORD = os.getenv("ORANGE_HRM_PASSWORD")
