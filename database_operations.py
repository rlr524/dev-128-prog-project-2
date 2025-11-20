"""
DATABASE.PY - Business Logic Layer
==================================
This file handles ALL database operations.
It knows NOTHING about the GUI - no tkinter imports!

Think of this as the "WHAT" - what data operations can we perform?
The GUI will be the "HOW" - how do we show this to the user?
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
            email TEXT,
            notes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def add_person(first_name, last_name, email, notes):
    """
    Add a new person to the database.
    
    Parameters:
        first_name (str): Person's first name (required)
        last_name (str): Person's last name (required)
        email (str): Person's email address (optional)
        notes (str): Additional notes about the person (optional)
    
    Returns:
        int: The ID of the newly created person
    
    Business Rule: First and last names are required (enforced by caller)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO people (first_name, last_name, email, notes)
        VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, email, notes))
    
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
        tuple or None: (id, first_name, last_name, email, notes) if found, None if not found
    
    This includes ALL fields including notes, used for detailed views and editing.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM people WHERE id = ?', (person_id,))
    person = cursor.fetchone()
    
    conn.close()
    
    return person


def update_person(person_id, first_name, last_name, email, notes):
    """
    Update an existing person's information.
    
    Parameters:
        person_id (int): The ID of the person to update
        first_name (str): New first name
        last_name (str): New last name
        email (str): New email address
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
        SET first_name=?, last_name=?, email=?, notes=?
        WHERE id=?
    ''', (first_name, last_name, email, notes, person_id))
    
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


def validate_person_data(first_name, last_name):
    """
    Validate that required fields are present.
    
    Parameters:
        first_name (str): First name to validate
        last_name (str): Last name to validate
    
    Returns:
        tuple: (is_valid, error_message)
               is_valid is True if data is valid, False otherwise
               error_message is empty string if valid, error description if invalid
    
    Business Rules:
        - First name is required and cannot be empty/whitespace
        - Last name is required and cannot be empty/whitespace
        - Email and notes are optional (validated elsewhere if needed)
    """
    # Strip whitespace and check if empty
    if not first_name or not first_name.strip():
        return False, "First name is required"
    
    if not last_name or not last_name.strip():
        return False, "Last name is required"
    
    # All validation passed
    return True, ""
