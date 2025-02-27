import sqlite3

class SQLiteHandler:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.enable_foreign_keys()
    
    def enable_foreign_keys(self):
        """Ensures foreign key constraints are enforced."""
        self.cursor.execute("PRAGMA foreign_keys = ON")
    
    def create_table(self, table, columns, foreign_keys=None):
        """Creates a table with optional foreign keys."""
        query = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)}"
        
        if foreign_keys:
            fk_constraints = [f"FOREIGN KEY ({fk}) REFERENCES {ref}" for fk, ref in foreign_keys.items()]
            query += f", {', '.join(fk_constraints)}"
        
        query += ")"
        self.cursor.execute(query)
        self.conn.commit()
    
    def create(self, table, data):
        """Inserts a record while handling foreign key constraints."""
        columns = ', '.join(data.keys())
        values = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        
        try:
            self.cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Foreign key constraint failed: {e}")
            return None
    
    def read(self, table, conditions=None):
        """Fetches records with optional conditions."""
        query = f"SELECT * FROM {table}"
        if conditions:
            cond_str = ' AND '.join([f"{k}=?" for k in conditions.keys()])
            query += f" WHERE {cond_str}"
            self.cursor.execute(query, tuple(conditions.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def update(self, table, data, conditions):
        """Updates records while maintaining constraints."""
        set_str = ', '.join([f"{k}=?" for k in data.keys()])
        cond_str = ' AND '.join([f"{k}=?" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_str} WHERE {cond_str}"
        
        try:
            self.cursor.execute(query, tuple(data.values()) + tuple(conditions.values()))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.IntegrityError as e:
            print(f"Foreign key update failed: {e}")
            return 0

    def delete(self, table, conditions):
        """Deletes records with foreign key constraints."""
        cond_str = ' AND '.join([f"{k}=?" for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {cond_str}"
        
        try:
            self.cursor.execute(query, tuple(conditions.values()))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.IntegrityError as e:
            print(f"Foreign key delete failed: {e}")
            return 0

    def get_single_value(self, table, column, conditions):
        """Retrieves a single value from a table based on conditions."""
        cond_str = ' AND '.join([f"{k}=?" for k in conditions.keys()])
        query = f"SELECT {column} FROM {table} WHERE {cond_str} LIMIT 1"
        self.cursor.execute(query, tuple(conditions.values()))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_single_value(self, table, column, value, conditions):
        """Updates a single column in a table."""
        return self.update(table, {column: value}, conditions)

    def close(self):
        """Closes the database connection."""
        self.cursor.close()
        self.conn.close()
