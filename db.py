import sqlite3
from sqlite3 import Error


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Class for working with the database
class BiographyDatabaseManager:
    def __init__(self, db_file):
        """Initialize and connect to the database"""
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.conn.row_factory = dict_factory
            print("Connection to the database established.")
        except Error as e:
            print(f"Error connecting to the database: {e}")

    def create_tables(self):
        """Create tables to store data about persons"""
        try:
            sql_create_person_table = """
            CREATE TABLE IF NOT EXISTS person (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK (LENGTH(name) <= 100),
                info TEXT CHECK (LENGTH(info) <= 10000)
            );
            """

            sql_create_facts_table = """
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                fact TEXT NOT NULL CHECK (LENGTH(fact) <= 100000),
                include BOOLEAN NOT NULL,
                FOREIGN KEY (person_id) REFERENCES person (id) ON DELETE CASCADE
            );
            """

            sql_create_histories_table = """
            CREATE TABLE IF NOT EXISTS histories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                history TEXT NOT NULL CHECK (LENGTH(history) <= 10000000),
                FOREIGN KEY (person_id) REFERENCES person (id) ON DELETE CASCADE
            );
            """

            if self.conn:
                c = self.conn.cursor()
                c.execute(sql_create_person_table)
                c.execute(sql_create_facts_table)
                c.execute(sql_create_histories_table)
                print("Tables created.")
        except Error as e:
            print(f"Error creating tables: {e}")

    def add_person(self, name, info, facts_to_include, facts_to_exclude):
        """Add a new person to the database"""
        try:
            sql = """
            INSERT INTO person (name, info)
            VALUES (?, ?, ?, ?)
            """
            cur = self.conn.cursor()
            cur.execute(sql, (name, info))
            self.conn.commit()
            print(f"Person '{name}' added.")
        except Error as e:
            print(f"Error adding person: {e}")

    def add_fact(self, person_id, fact, include=True):
        """Add a fact about specific person"""
        try:
            sql = """
            INSERT INTO facts (person_id, fact, include)
            VALUES (?, ?, ?)
            """
            cur = self.conn.cursor()
            cur.execute(sql, (person_id, fact, include))
            self.conn.commit()
            print(f"Fact added for person with ID {person_id}.")
        except Error as e:
            print(f"Error adding fact: {e}")

    def add_history(self, person_id, file_name):
        """Add a history related to a person"""
        try:
            sql = """
            INSERT INTO histories (person_id, history)
            VALUES (?, ?)
            """

            with open(file_name, 'r', encoding="cp1251", errors='ignore') as f:
                text = f.read()
                cur = self.conn.cursor()
                cur.execute(sql, (person_id, text))
                self.conn.commit()

            print(f"File '{file_name}' added for person with ID {person_id}.")
        except Error as e:
            print(f"Error adding file: {e}")

    def delete_person(self, person_id):
        """Delete a person and all related data"""
        try:
            sql = "DELETE FROM person WHERE id = ?"
            cur = self.conn.cursor()
            cur.execute(sql, (person_id,))
            self.conn.commit()
            print(f"Person with ID {person_id} deleted.")
        except Error as e:
            print(f"Error deleting person: {e}")

    def update_person(self, person_id, name=None, info=None):
        """Update person information"""
        try:
            cur = self.conn.cursor()
            if name:
                cur.execute("UPDATE person SET name = ? WHERE id = ?", (name, person_id))
            if info:
                cur.execute("UPDATE person SET info = ? WHERE id = ?", (info, person_id))
            self.conn.commit()
            print(f"Information for person with ID {person_id} updated.")
        except Error as e:
            print(f"Error updating person information: {e}")

    def get_person(self, person_id):
        """Get person data by ID"""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM person WHERE id = ?", (person_id,))
            person = cur.fetchone()

            return person
        except Error as e:
            print(f"Error retrieving person data: {e}")
            return None

    def get_all_persons(self):
        """Get a list of all persons"""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM person")
            persons = cur.fetchall()
            return persons
        except Error as e:
            print(f"Error retrieving persons list: {e}")
            return None

    def get_person_histories(self, person_id):
        """Get all histories for a specific person by person ID"""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM histories WHERE person_id = ?", (person_id,))
            histories = cur.fetchall()

            return histories
        except Error as e:
            print(f"Error retrieving histories for person ID {person_id}: {e}")
            return None

    def get_person_facts(self, person_id, include=None):
        """Get all facts for a specific person by person ID, with an optional filter on the 'include' field"""
        try:
            cur = self.conn.cursor()

            if include is not None:
                cur.execute("SELECT * FROM facts WHERE person_id = ? AND include = ?", (person_id, include))
            else:
                cur.execute("SELECT * FROM facts WHERE person_id = ?", (person_id,))

            facts = cur.fetchall()

            return facts
        except Error as e:
            print(f"Error retrieving facts for person ID {person_id}: {e}")
            return None
