from keeshond import logging_logger
log = logging_logger.getlogger(__name__, logging_logger.DEBUG)

from keeshond.ktoga.keystore.database import Database
import bcrypt


class Auth:
    def __init__(self, _database_path, _pepper=b"enter yout pepper value here"):
        self.db = Database(_database_path, "sqlite3")
        self.pepper = _pepper  # Fixed pepper value for all passwords

    def is_password_set(self):
        """Check if password has been set"""
        return self.db.get_password_hash() is not None

    def set_password(self, password):
        """Hash and store password with pepper"""
        # Combine password with pepper
        peppered_password = password.encode('utf-8') + self.pepper

        # Generate salt and hash password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(peppered_password, salt)

        # Store hash in database
        self.db.store_password_hash(password_hash.decode('utf-8'))

    def verify_password(self, password):
        """Verify provided password against stored hash"""
        stored_hash = self.db.get_password_hash()
        if not stored_hash:
            return False

        # Combine password with pepper for verification
        peppered_password = password.encode('utf-8') + self.pepper

        return bcrypt.checkpw(
            peppered_password,
            stored_hash.encode('utf-8')
        )
