import sqlite3

class HistorydbManager:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            session_id TEXT NOT NULL,
            created_time REAL DEFAULT (strftime('%s', 'now')),
            update_time REAL
        )
    """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            timestamp REAL DEFAULT (strftime('%s', 'now')),
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            turn INTEGER NOT NULL,
            FOREIGN KEY (session_id) REFERENCES conversations(session_id) ON DELETE CASCADE
        )
    """)
    
    
    def message_insert(
        self, 
        message: str, 
        session_id: str, 
        timestamp: float, 
        role: str, 
        turn: int
    ):
        """Insert one piece message include all metadatas. 

        All the args are necessary.
        
        Args:
            message: The content of message you want to store
            timestamp: Must be formatted of the module datetime which method datetime.timestamp()
            role: Only one of ["system","user"](of course you can set that assistant)
            turn: The turn of the session, it must be a int type
        """
        
        self.conn.execute("""INSERT INTO messages 
                        (message, session_id, timestamp, role, turn) VALUES (?, ?, ?, ? ,?)""", 
                        (message, session_id, timestamp, role, turn))
        self.conn.execute("UPDATE conversations SET update_time = ? where session_id = ?", 
                          (timestamp, session_id))
        self.conn.commit()
        
    def session_insert(
        self, 
        session_id: str, 
        timestamp: float,
        name: str = "新对话"
    ):
        """
        A inner func, when create a new session use.

        You should not use this func unless you know what you are doing.
        """
        
        self.conn.execute("INSERT INTO conversations (name, session_id, created_time, update_time) VALUES (?, ?, ?, ?)",
                          (name, session_id, timestamp, timestamp))
        self.conn.commit()
        
    def get_history(self, session_id: str):
        """Get the latest 10 messages by session_id"""
        cursor = self.conn.execute("SELECT role, message FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT 10", (session_id,))
        rows = cursor.fetchall()
        messages = []
        for row in rows:
            messages.append({"role": row[0], "content": row[1]})
        cursor = self.conn.execute("SELECT turn FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT 1", (session_id,))
        turn = cursor.fetchone()[0]
        return messages, turn

    def get_conversations_info(self):
        """get info of conversations to list"""
        cursor = self.conn.execute("SELECT session_id, name FROM conversations")
        rows = cursor.fetchall()
        options = []
        for row in rows:
            options.append(row)
        return options
    
        