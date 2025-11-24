"""
DATABASE.PY - Business Logic Layer
==================================
This file handles ALL database operations.
It knows NOTHING about the GUI - no tkinter imports!

Think of this as the "WHAT" - what data operations can we perform?
The GUI will be the "HOW" - how do we show this to the user?

Rob Ranf
DEV 128 Fall 2025 Section 27802
https://github.com/rlr524/dev-128-prog-project-2
"""

import sqlite3

# Database filename - stored at module level for easy access
DATABASE_NAME = 'people.db'


def create_database():
    """
    Initialize the database and create the people table if it doesn't exist.
    
    This should be called when the application starts.
    It's safe to call multiple times - CREATE TABLE IF NOT EXISTS won't error.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            job_title TEXT NOT NULL,
            street TEXT NOT NULL,
            street2 TEXT,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            postal TEXT NOT NULL,
            notes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def add_person(first_name, last_name, email, job_title, street, street2, city, state, postal, notes):
    """
    Add a new person to the database.
    
    Parameters:
        first_name (str): Person's first name (required)
        last_name (str): Person's last name (required)
        email (str): Person's email address (optional)
        job_title (str): Person's job title (required)
        street (str): Person's street address (required)
        street2 (str): Person's suite/apartment/unit (optional)
        city (str): Person's city (required)
        state (str): Person's USPS state code (required)
        postal (str): Person's postal/zip code (required)
        notes (str): Additional notes about the person (optional)
    
    Returns:
        int: The ID of the newly created person
    
    Business Rule: First and last names are required (enforced by caller)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO people (first_name, last_name, email, job_title, street, street2, city, state, postal, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, email, job_title, street, street2, city, state, postal, notes))
    
    # Get the ID of the person we just created
    person_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return person_id


def get_all_people():
    """
    Retrieve all people from the database, sorted by last name then first name.
    
    Returns:
        list of tuples: Each tuple contains (id, first_name, last_name, email)
        Example: [(1, 'John', 'Doe', 'john@email.com'), (2, 'Jane', 'Smith', 'jane@email.com')]
    
    Note: We don't return 'notes' here because the list view doesn't need it.
          This keeps the data transfer efficient.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, first_name, last_name, email 
        FROM people 
        ORDER BY last_name, first_name
    ''')
    
    people = cursor.fetchall()
    conn.close()
    
    return people


def get_person_by_id(person_id):
    """
    Retrieve a single person's complete information by their ID.
    
    Parameters:
        person_id (int): The unique ID of the person to retrieve
    
    Returns:
        tuple or None: (id, first_name, last_name, email, street, street2, city, state, postal, notes) if found,
        None if not found
    
    This includes ALL fields including notes, used for detailed views and editing.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM people WHERE id = ?', (person_id,))
    person = cursor.fetchone()
    
    conn.close()
    
    return person


def update_person(person_id, first_name, last_name, email, job_title, street, street2, city, state, postal, notes):
    """
    Update an existing person's information.
    
    Parameters:
        person_id (int): The ID of the person to update
        first_name (str): New first name
        last_name (str): New last name
        email (str): New email address
        job_title (str): New job title
        street (str): New street address
        street2 (str): New suite/apt/unit (optional)
        city (str): New city
        state (str): New state
        postal (str): New postal/zip code
        notes (str): New notes
    
    Returns:
        bool: True if the update was successful, False if person not found
    
    Business Rule: All fields are updated - this is a complete replacement,
                   not a partial update.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE people 
        SET first_name=?, last_name=?, email=?, job_title=?, street=?, street2=?, city=?, state=?, postal=?, notes=?
        WHERE id=?
    ''', (first_name, last_name, email, job_title, street, street2, city, state, postal, notes, person_id))
    
    # Check if any row was actually updated
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0


def delete_person(person_id):
    """
    Delete a person from the database.
    
    Parameters:
        person_id (int): The ID of the person to delete
    
    Returns:
        bool: True if the person was deleted, False if person not found
    
    Warning: This is permanent! The GUI should confirm before calling this.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM people WHERE id = ?', (person_id,))
    
    # Check if any row was actually deleted
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0


def validate_person_data(first_name, last_name, email, job_title, street, city, state, postal):
    """
    Validate that required fields are present.
    
    Parameters:
        first_name (str): First name to validate
        last_name (str): Last name to validate
        email (str): Email to validate
        job_title (str): Job title to validate
        street (str): Street address to validate
        city (str): City to validate
        state (str): State to validate and confirm matches an abbreviation in the state_codes list
        postal (str): Postal code to validate
    
    Returns:
        tuple: (is_valid, error_message)
               is_valid is True if data is valid, False otherwise
               error_message is empty string if valid, error description if invalid
    
    Business Rules:
        - First name is required and cannot be empty/whitespace
        - Last name is required and cannot be empty/whitespace
        - Email is required and cannot be empty/whitespace
        - Job title is required and cannot be empty/whitespace
        - Street address is required and cannot be empty/whitespace
        - City is required and cannot be empty/whitespace
        - State is required and cannot be empty/whitespace
        - Postal code is required and cannot be empty/whitespace
        - Notes are optional (validated elsewhere if needed)
        - Street address 2 (suite/apt/unit) is optional
    """
    # List of state abbreviations for State dropdown (https://gist.github.com/JeffPaine/3083347)
    state_codes = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
               "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME",
               "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV",
               "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA",
               "VT", "WA", "WI", "WV", "WY"]

    # Strip whitespace and check if empty
    if not first_name or not first_name.strip():
        return False, "First name is required"
    
    if not last_name or not last_name.strip():
        return False, "Last name is required"

    if not email or not email.strip():
        return False, "Email is required"

    if not job_title or not  job_title.strip():
        return False, "Job title is required"

    if not street or not street.strip():
        return False, "Street address is required"

    if not city or not city.strip():
        return False, "City is required"

    # Check if state is a valid US state or DC abbreviation
    if not state or not state.strip() or state not in state_codes:
        return False, "Please enter a valid USPS state abbreviation"

    if not postal or not postal.strip():
        return False, "Please enter a postal/zip code"
    
    # All validation passed
    return True, ""
