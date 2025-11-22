# RPA Challenge

This project automates the process of adding candidates to the OrangeHRM demo website.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Uill2110/rpa_challenger.git
   cd rpa_challenge
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your credentials:**
   - Rename the `.env.example` file to `.env`.
   - Open the `.env` file and replace the placeholder values with your OrangeHRM username and password.

## Running the Application

To run the automation, execute the `main.py` script:

```bash
python main.py
