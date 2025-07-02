import sqlite3 
import json
from datetime import datetime 

class Database:
    def __init__(self, db_name="budgetbites.db"):
        self.db_name = db_name # The name of our database file
        self.conn = None # Connection object
        self.cursor = None # Cursor object 
        self._connect() # Connect to the database when the class starts
        self._create_table() # Make sure the 'meals' table exists

    def _connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name) # Connects to or creates the database file
            self.cursor = self.conn.cursor() # Get a cursor to execute commands
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def _create_table(self):
        """Creates the 'meals' table if it doesn't exist."""
        if self.conn:
            try:
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS meals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        meal_idea TEXT NOT NULL,             
                        user_inputs TEXT NOT NULL,           
                        recipe_data TEXT NOT NULL,      
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP 
                    )
                """)
                self.conn.commit() # Save the changes to the database
            except sqlite3.Error as e:
                print(f"Error creating table: {e}")
        else:
            print("Database connection not established. Cannot create table.")


    def save_meal(self, meal_idea, user_inputs, recipe_data):
        """Saves a meal and its associated data to the database."""
        if self.conn:
            try:
                # Convert Python dictionaries/lists to JSON text to store in the database
                user_inputs_json = json.dumps(user_inputs)
                recipe_data_json = json.dumps(recipe_data)
                self.cursor.execute(
                    "INSERT INTO meals (meal_idea, user_inputs, recipe_data) VALUES (?, ?, ?)",
                    (meal_idea, user_inputs_json, recipe_data_json) # Insert data into the table
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error saving meal: {e}")
        else:
            print("Database connection not established. Cannot save meal.")

    def get_meal_history(self):
        """Retrieves all past meals from the database."""
        if self.conn:
            try:
                # Select all columns from the meals table, ordered by newest first
                self.cursor.execute("SELECT meal_idea, user_inputs, recipe_data, timestamp FROM meals ORDER BY timestamp DESC")
                rows = self.cursor.fetchall() # Get all the results
                history = []
                for row in rows:
                    history.append({
                        "meal_idea": row[0],
                        "user_inputs": json.loads(row[1]), # Convert text back to Python dictionary
                        "recipe_data": json.loads(row[2]), # Convert text back to Python dictionary
                        "timestamp": row[3]
                    })
                return history
            except sqlite3.Error as e:
                print(f"Error retrieving meal history: {e}")
                return []
        else:
            print("Database connection not established. Cannot retrieve history.")
            return []

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()