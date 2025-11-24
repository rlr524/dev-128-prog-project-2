"""
PEOPLE_GUI.PY - Presentation Layer
================================
This file handles ALL GUI operations using Tkinter.
It imports database_operations.py to access business logic.

Think of this as the "HOW" - how do we show data to the user?
The database_operations.py file is the "WHAT" - what operations can we perform?

Key Pattern: GUI methods call database functions, then update the display.
Flow: User Action → GUI Method → Database Function → Update GUI

Rob Ranf
DEV 128 Fall 2025 Section 27802
https://github.com/rlr524/dev-128-prog-project-2
"""

import tkinter as tk
from tkinter import messagebox
import database_operations as database # Our business logic layer


class CRUDApplication:
    """
    Main application class that manages the GUI and interacts with database.
    
    This class follows the principle: "Don't talk to the database directly,
    use the database module's functions instead."
    """
    
    def __init__(self, root):
        """
        Initialize the application window and all GUI components.
        
        Parameters:
            root: The main Tkinter window (Tk instance)
        """
        self.root = root
        self.root.title("Simple CRUD Application")
        self.root.geometry("600x600")
        
        # Initialize database - safe to call every time
        database.create_database()
        
        # Build the GUI components
        self.create_menu()
        self.create_main_layout()
        
        # Load initial data
        self.refresh_list()
    
    
    # =========================================================================
    # GUI SETUP METHODS - Build the interface
    # =========================================================================
    
    def create_menu(self):
        """
        Create the top menu bar with all CRUD operations listed under "Actions". Note that this menu contains
        two additional operations - REFRESH list and EXIT.
        
        Menu Structure:
            Actions
                ├── Add Person
                ├── Read Person
                ├── Edit Person
                ├── Delete Person
                ├── (separator)
                ├── Refresh List
                ├── (separator)
                └── Exit
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Create "Actions" dropdown menu
        crud_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Actions", menu=crud_menu)
        
        # Add menu items that call our CRUD methods
        crud_menu.add_command(label="Add Person", command=self.add_person)
        crud_menu.add_command(label="Read Person", command=self.read_person)
        crud_menu.add_command(label="Edit Person", command=self.edit_person)
        crud_menu.add_command(label="Delete Person", command=self.delete_person)
        crud_menu.add_separator()
        crud_menu.add_command(label="Refresh List", command=self.refresh_list)
        crud_menu.add_separator()
        crud_menu.add_command(label="Exit", command=self.root.quit)
    
    
    def create_main_layout(self):
        """
        Create the main window layout with listbox and buttons.
        
        Layout Structure:
            ┌─────────────────────────────┐
            │      "People List"          │
            ├─────────────────────────────┤
            │                             │
            │      [Listbox with         │
            │       scrollbar]            │
            │                             │
            ├─────────────────────────────┤
            │ [Add] [Read] [Edit] [Delete]│
            └─────────────────────────────┘
        """
        # Main container frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title label
        tk.Label(main_frame, text="People List", 
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(main_frame)
        listbox_frame.pack(fill="both", expand=True)
        
        # Scrollbar on the right
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox shows people - stores one person per line
        self.listbox = tk.Listbox(listbox_frame, 
                                  yscrollcommand=scrollbar.set, 
                                  font=('Arial', 14))
        self.listbox.pack(side="left", fill="both", expand=True)
        
        # Connect scrollbar to listbox
        scrollbar.config(command=self.listbox.yview)
        
        # Button frame at bottom
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Create action buttons - duplicate menu functionality for convenience
        tk.Button(button_frame, text="Add", 
                 command=self.add_person, width=10).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Read", 
                 command=self.read_person, width=10).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Edit", 
                 command=self.edit_person, width=10).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Delete", 
                 command=self.delete_person, width=10).grid(row=0, column=3, padx=5)
    
    
    # =========================================================================
    # CRUD OPERATION METHODS - Interface with database layer
    # =========================================================================
    
    def add_person(self):
        """
        CREATE operation - Open a form to add a new person.
        
        Flow:
            1. Open popup window with empty form
            2. User fills in data
            3. User clicks Save
            4. Validate data (using database.validate_person_data)
            5. If valid, call database.add_person()
            6. Refresh the list to show new person
            7. Close popup
        """
        # Create popup window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Person")
        add_window.geometry("600x600")
        add_window.option_add("*Font", "Arial 14")
        
        # Form fields - using grid layout for alignment
        tk.Label(add_window, text="First Name*:").grid(
            row=0, column=0, sticky='e', padx=5, pady=5)
        first_entry = tk.Entry(add_window, width=30)
        first_entry.grid(row=0, column=1, padx=5, pady=5)
        first_entry.focus()  # Cursor starts here
        
        tk.Label(add_window, text="Last Name*:").grid(
            row=1, column=0, sticky='e', padx=5, pady=5)
        last_entry = tk.Entry(add_window, width=30)
        last_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(add_window, text="Email*:").grid(
            row=2, column=0, sticky='e', padx=5, pady=5)
        email_entry = tk.Entry(add_window, width=30)
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Job Title*:").grid(
            row=3, column=0, sticky='e', padx=5, pady=5)
        job_title_entry = tk.Entry(add_window, width=30)
        job_title_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Street Address*:").grid(
            row=4, column=0, sticky='e', padx=5, pady=5)
        street_address_entry = tk.Entry(add_window, width=30)
        street_address_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Suite/Apt/Unit:").grid(
            row=5, column=0, sticky='e', padx=5, pady=5)
        street_address_2_entry = tk.Entry(add_window, width=30)
        street_address_2_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(add_window, text="City*:").grid(
            row=6, column=0, sticky='e', padx=5, pady=5)
        city_entry = tk.Entry(add_window, width=30)
        city_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(add_window, text="State*:").grid(
            row=7, column=0, sticky='e', padx=5, pady=5)
        state_entry = tk.Entry(add_window, width=3)
        state_entry.grid(row=7, column=1, sticky='w', padx=5, pady=5)

        tk.Label(add_window, text="Postal Code*:").grid(
            row=8, column=0, sticky='e', padx=5, pady=5)
        postal_entry = tk.Entry(add_window, width=30)
        postal_entry.grid(row=8, column=1, padx=5, pady=5)

        # Need to move notes to last here as, weirdly, code order determines the field tab focus order, not the row attribute
        tk.Label(add_window, text="Notes:").grid(
            row=9, column=0, sticky='ne', padx=5, pady=5)
        notes_text = tk.Text(add_window, width=30, height=5)
        notes_text.grid(row=9, column=1, padx=5, pady=5)

        def save_person():
            """
            Inner function that handles the Save button click.
            This has access to all the entry widgets above (closure).
            """
            # Get values from form fields
            first = first_entry.get().strip()
            last = last_entry.get().strip()
            email = email_entry.get().strip()
            job = job_title_entry.get().strip()
            street = street_address_entry.get().strip()
            street2 = street_address_2_entry.get().strip()
            city = city_entry.get().strip()
            state = state_entry.get().strip()
            postal = postal_entry.get().strip()
            notes = notes_text.get("1.0", tk.END).strip()
            
            # Validate using business logic layer
            is_valid, error_message = database.validate_person_data(first, last, email, job, street, city, state, postal)
            
            if not is_valid:
                messagebox.showerror("Validation Error", error_message)
                return
            
            # Call business logic to add person
            person_id = database.add_person(first, last, email, job, street, street2, city, state, postal, notes)
            
            # Show success message
            messagebox.showinfo("Success", 
                              f"Person added successfully!\nID: {person_id}")
            
            # Close the popup window
            add_window.destroy()
            
            # Refresh the main list to show the new person
            self.refresh_list()

        def cancel_window():
            add_window.destroy()

        # Save button
        tk.Button(add_window, text="Save", command=save_person, width=10).grid(row=10, column=0, pady=10)

        # Cancel button
        tk.Button(add_window, text="Cancel", command=cancel_window, width=10).grid(row=10, column=1, pady=10)
    
    
    def read_person(self):
        """
        READ operation - Display selected person's full details.
        
        Flow:
            1. Get selected item from listbox
            2. Extract person ID from selected text
            3. Call database.get_person_by_id()
            4. Display all fields in a popup window
        """
        # Check if something is selected
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                 "Please select a person from the list!")
            return
        
        # Get the selected text from listbox
        # Format is: "ID - First Last (email)"
        person_info = self.listbox.get(selection[0])
        
        # Extract ID (everything before " - ")
        person_id = int(person_info.split(" - ")[0])
        
        # Fetch full details from database
        person = database.get_person_by_id(person_id)
        
        if not person:
            messagebox.showerror("Error", "Person not found in database!")
            return
        
        # Unpack tuple for readability
        # person = (id, first_name, last_name, email, notes)
        pid, first, last, email, job, street, street2, city, state, postal, notes = person
        
        # Create display window
        read_window = tk.Toplevel(self.root)
        read_window.title("Person Details")
        read_window.geometry("800x600")
        read_window.option_add("*Font", "Arial 14")
        
        # Format details nicely
        details = f"""
ID: {pid}
First Name: {first}
Last Name: {last}
Email: {email}
Job Title: {job}
Street Address: {street}
Street Address 2: {street2 if street2 else '(not provided)'}
City: {city}
State: {state}
Postal Code: {postal}

Notes:
{notes if notes else '(no notes)'}
        """
        
        # Display as label
        tk.Label(read_window, text=details, wraplength=400,
                justify='left', font=('Arial', 12)).pack(padx=20, pady=20)
        
        # Close button
        tk.Button(read_window, text="Close", 
                 command=read_window.destroy).pack(pady=10)
    
    
    def edit_person(self):
        """
        UPDATE operation - Edit selected person's information.
        
        Flow:
            1. Get selected person from listbox
            2. Call database.get_person_by_id() to get current data
            3. Open form pre-filled with current values
            4. User modifies data
            5. User clicks Update
            6. Validate data
            7. If valid, call database.update_person()
            8. Refresh list to show updated info
            9. Close popup
        """
        # Check if something is selected
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                 "Please select a person to edit!")
            return
        
        # Get person ID
        person_info = self.listbox.get(selection[0])
        person_id = int(person_info.split(" - ")[0])
        
        # Fetch current data
        person = database.get_person_by_id(person_id)
        
        if not person:
            messagebox.showerror("Error", "Person not found in database!")
            return
        
        # Unpack current values
        pid, first, last, email, job, street, street2, city, state, postal, notes = person
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Person")
        edit_window.geometry("600x600")
        edit_window.option_add("*Font", "Arial 14")
        
        # Form fields pre-filled with current data
        tk.Label(edit_window, text="First Name*:").grid(
            row=0, column=0, sticky='e', padx=5, pady=5)
        first_edit = tk.Entry(edit_window, width=30)
        first_edit.insert(0, first)  # Pre-fill with current value
        first_edit.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(edit_window, text="Last Name*:").grid(
            row=1, column=0, sticky='e', padx=5, pady=5)
        last_edit = tk.Entry(edit_window, width=30)
        last_edit.insert(0, last)
        last_edit.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(edit_window, text="Email*:").grid(
            row=2, column=0, sticky='e', padx=5, pady=5)
        email_edit = tk.Entry(edit_window, width=30)
        email_edit.insert(0, email)
        email_edit.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Job Title*:").grid(
            row=3, column=0, sticky='e', padx=5, pady=5)
        job_edit = tk.Entry(edit_window, width=30)
        job_edit.insert(0, job)
        job_edit.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Street Address*:").grid(
            row=4, column=0, sticky='e', padx=5, pady=5)
        street_edit = tk.Entry(edit_window, width=30)
        street_edit.insert(0, street)
        street_edit.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Suite/Apt/Unit:").grid(
            row=5, column=0, sticky='e', padx=5, pady=5)
        street_2_edit = tk.Entry(edit_window, width=30)
        street_2_edit.insert(0, street2)
        street_2_edit.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="City*:").grid(
            row=6, column=0, sticky='e', padx=5, pady=5)
        city_edit = tk.Entry(edit_window, width=30)
        city_edit.insert(0, city)
        city_edit.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="State*:").grid(
            row=7, column=0, sticky='e', padx=5, pady=5)
        state_edit = tk.Entry(edit_window, width=30)
        state_edit.insert(0, state)
        state_edit.grid(row=7, column=1, sticky='w', padx=5, pady=5)

        tk.Label(edit_window, text="Postal Code*:").grid(
            row=8, column=0, sticky='e', padx=5, pady=5)
        postal_edit = tk.Entry(edit_window, width=30)
        postal_edit.insert(0, postal)
        postal_edit.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Notes:").grid(
            row=9, column=0, sticky='ne', padx=5, pady=5)
        notes_text_edit = tk.Text(edit_window, width=30, height=5)
        notes_text_edit.insert("1.0", notes if notes else "")
        notes_text_edit.grid(row=9, column=1, padx=5, pady=5)
        
        def update_person():
            """
            Function that handles the Update button click.
            """
            # Get modified values (recall that strip will remove any leading or ending spaces)
            first_e = first_edit.get().strip()
            last_e = last_edit.get().strip()
            email_e = email_edit.get().strip()
            job_e = job_edit.get().strip()
            street_e = street_edit.get().strip()
            street_2_e = street_2_edit.get().strip()
            city_e = city_edit.get().strip()
            state_e = state_edit.get().strip()
            postal_e = postal_edit.get().strip()
            notes_e = notes_text_edit.get("1.0", tk.END).strip() # from the starting position of line 1 character 0 to the end of all text
            
            # Validate all required fields
            is_valid, error_message = database.validate_person_data(first_e, last_e, email_e, job_e, street_e, city_e, state_e, postal_e)

            if not is_valid:
                messagebox.showerror("Validation Error", error_message)
                return
            
            # Call business logic to update database file
            success = database.update_person(person_id, first_e, last_e, email_e, job_e, street_e, street_2_e, city_e, state_e, postal_e, notes_e)
            
            if success:
                messagebox.showinfo("Success", "Person updated successfully!")
                edit_window.destroy() # kill the window
                self.refresh_list() # refresh the list of people in our main frame
            else:
                messagebox.showerror("Error", "Failed to update person!")

        def cancel_window():
            edit_window.destroy()
        
        # Update button
        tk.Button(edit_window, text="Update", 
                 command=update_person, width=15).grid(row=10, column=0, pady=10)

        # Cancel button
        tk.Button(edit_window, text="Cancel", command=cancel_window, width=10).grid(row=10, column=1, pady=10)
    
    
    def delete_person(self):
        """
        DELETE operation - Remove selected person from database.
        
        Flow:
            1. Get selected person from listbox
            2. Show confirmation dialog (important for destructive actions!)
            3. If confirmed, call database.delete_person()
            4. Refresh list to remove deleted person
        
        Safety: Always confirm before delete operations!
        """
        # Check if something is selected
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", 
                                 "Please select a person to delete!")
            return
        
        # Get person info for confirmation message
        person_info = self.listbox.get(selection[0])
        person_id = int(person_info.split(" - ")[0])
        
        # Confirm deletion - CRITICAL for destructive operations
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete:\n\n{person_info}\n\nThis cannot be undone!"
        )
        
        if not confirm:
            return  # User clicked "No" - abort deletion
        
        # Call business logic to delete
        success = database.delete_person(person_id)
        
        if success:
            messagebox.showinfo("Success", "Person deleted successfully!")
            self.refresh_list()
        else:
            messagebox.showerror("Error", "Failed to delete person!")
    
    
    # =========================================================================
    # UTILITY METHODS - Helper functions
    # =========================================================================
    
    def refresh_list(self):
        """
        Refresh the listbox with current database contents.
        
        This is called after any operation that changes the data:
        - After adding a person
        - After editing a person
        - After deleting a person
        - When the application first starts
        - When user clicks "Refresh List" menu item
        
        Flow:
            1. Clear current listbox contents
            2. Call database.get_all_people()
            3. Format each person as "ID - First Last (email)"
            4. Insert into listbox
        """
        # Clear existing items
        self.listbox.delete(0, tk.END)
        
        # Get all people from database
        people = database.get_all_people()
        
        # Add each person to listbox
        for person in people:
            # person is a tuple: (id, first_name, last_name, email)
            person_id, first, last, email = person
            
            # Format for display
            display_text = f"{person_id} - {first} {last} ({email if email else 'no email'})"
            
            # Insert into listbox
            self.listbox.insert(tk.END, display_text)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    
    # Create application instance (builds GUI and initializes database)
    app = CRUDApplication(root)
    
    # Start the GUI event loop (waits for user actions)
    root.mainloop()
