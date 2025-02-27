from keeshond import logging_logger

log = logging_logger.getlogger(__name__, logging_logger.ERROR)

import sqlite3


class Database:
    def __init__(self, _db_file, _db_system):
        self.db_file = _db_file
        if _db_system == "sqlite3":
            self.init_db()
        else:
            log.error(f"Unsupported database system: {_db_system}")
            raise SystemError(12)

    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create password table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "password" (
                id INTEGER PRIMARY KEY,
                hash TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def get_password_hash(self):
        """Retrieve stored password hash"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT hash FROM password WHERE id = 1')
        result = cursor.fetchone()

        conn.close()
        return result[0] if result else None

    def store_password_hash(self, password_hash):
        """Store password hash in database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM password')  # Remove any existing password
        cursor.execute('INSERT INTO password (id, hash) VALUES (1, ?)', (password_hash,))

        conn.commit()
        conn.close()
