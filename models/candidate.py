from dataclasses import dataclass

@dataclass
class Candidate:
    """Data structure for a candidate."""
    first_name: str
    last_name: str
    email: str
    vacancy: str
    contact_number: str = ""
    keywords: str = ""
    date_of_application: str = ""
    notes: str = ""
