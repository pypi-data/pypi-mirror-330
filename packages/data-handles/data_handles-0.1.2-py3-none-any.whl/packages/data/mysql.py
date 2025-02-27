import socket
import struct

class MySQLSocketHandler:
    def __init__(self, host, port=3306):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print("Connected to MySQL server via socket.")
    
    def send_query(self, query):
        """Sends a raw query to the MySQL server."""
        try:
            self.sock.sendall(query.encode())
            response = self.sock.recv(4096)
            return response
        except Exception as e:
            print(f"Query failed: {e}")
            return None
    
    def create_table(self, table, columns, foreign_keys=None):
        """Creates a table with optional foreign keys."""
        query = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)}"
        
        if foreign_keys:
            fk_constraints = [f"FOREIGN KEY ({fk}) REFERENCES {ref}" for fk, ref in foreign_keys.items()]
            query += f", {', '.join(fk_constraints)}"
        
        query += ")"
        return self.send_query(query)
    
    def insert(self, table, data):
        """Inserts a record into a table."""
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{v}'" for v in data.values()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        return self.send_query(query)
    
    def read_one(self, table, conditions):
        """Fetches a single record based on conditions."""
        condition_str = ' AND '.join([f"{k}='{v}'" for k, v in conditions.items()])
        query = f"SELECT * FROM {table} WHERE {condition_str} LIMIT 1"
        return self.send_query(query)
    
    def read_all(self, table):
        """Fetches all records from a table."""
        query = f"SELECT * FROM {table}"
        return self.send_query(query)
    
    def update(self, table, data, conditions):
        """Updates records based on conditions."""
        set_str = ', '.join([f"{k}='{v}'" for k, v in data.items()])
        condition_str = ' AND '.join([f"{k}='{v}'" for k, v in conditions.items()])
        query = f"UPDATE {table} SET {set_str} WHERE {condition_str}"
        return self.send_query(query)
    
    def delete(self, table, conditions):
        """Deletes records based on conditions."""
        condition_str = ' AND '.join([f"{k}='{v}'" for k, v in conditions.items()])
        query = f"DELETE FROM {table} WHERE {condition_str}"
        return self.send_query(query)
    
    def close(self):
        """Closes the socket connection."""
        self.sock.close()
        print("Connection closed.")
