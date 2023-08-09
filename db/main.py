import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('minig4you.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS users (user_id integer, lang text, currency text, electricity text, phone text)''')
        self.conn.commit()

    def insert_user(self, user_id, lang=None, currency=None,electricity=None, phone=None):
        # Check if the user_id already exists in the table
        self.c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        existing_user = self.c.fetchone()

        if existing_user:
            # Update existing user data if it's not None
            update_query = "UPDATE users SET "
            update_params = []
            if lang is not None:
                update_query += "lang = ?, "
                update_params.append(lang)
            if currency is not None:
                update_query += "currency = ?, "
                update_params.append(currency)
            if electricity is not None:
                update_query += "electricity = ?, "
                update_params.append(electricity)
            if phone is not None:
                update_query += "phone = ?, "
                update_params.append(phone)
            

            # Remove the trailing comma and space from the update_query
            update_query = update_query[:-2]

            # Add the condition to update only the specific user_id
            update_query += " WHERE user_id = ?"
            update_params.append(user_id)

            # Execute the update query
            self.c.execute(update_query, tuple(update_params))
        else:
            # Insert a new user if the user_id doesn't exist in the table
            self.c.execute('''INSERT INTO users(user_id, lang, currency, electricity, phone)
                            VALUES (?, ?, ?, ?, ?)''',
                        (user_id, lang, currency, electricity, phone))

        # Commit the changes to the database
        self.conn.commit()

    def select(self, user_id, column_name=None):
        if column_name is None:
            # If column_name is not provided, select all columns
            self.c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        else:
            # If column_name is provided, select only the specified column
            self.c.execute(f"SELECT {column_name} FROM users WHERE user_id = ?", (user_id,))

        # Fetch and return the result
        result = self.c.fetchone()

        if result is not None:
            return result
        else:
            return None

