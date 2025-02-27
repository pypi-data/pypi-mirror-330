import sqlite3

class SQLiteHandler:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def create_table(self, table, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})"
        self.cursor.execute(query)
        self.conn.commit()
    
    def create(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query, tuple(data.values()))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def read(self, table, conditions=None):
        query = f"SELECT * FROM {table}"
        if conditions:
            cond_str = ' AND '.join([f"{k}=?" for k in conditions.keys()])
            query += f" WHERE {cond_str}"
            self.cursor.execute(query, tuple(conditions.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def update(self, table, data, conditions):
        set_str = ', '.join([f"{k}=?" for k in data.keys()])
        cond_str = ' AND '.join([f"{k}=?" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_str} WHERE {cond_str}"
        self.cursor.execute(query, tuple(data.values()) + tuple(conditions.values()))
        self.conn.commit()
        return self.cursor.rowcount
    
    def delete(self, table, conditions):
        cond_str = ' AND '.join([f"{k}=?" for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {cond_str}"
        self.cursor.execute(query, tuple(conditions.values()))
        self.conn.commit()
        return self.cursor.rowcount
    
    def get_single_value(self, table, column, conditions):
        cond_str = ' AND '.join([f"{k}=?" for k in conditions.keys()])
        query = f"SELECT {column} FROM {table} WHERE {cond_str} LIMIT 1"
        self.cursor.execute(query, tuple(conditions.values()))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def update_single_value(self, table, column, value, conditions):
        return self.update(table, {column: value}, conditions)
    
    def close(self):
        self.cursor.close()
        self.conn.close()
