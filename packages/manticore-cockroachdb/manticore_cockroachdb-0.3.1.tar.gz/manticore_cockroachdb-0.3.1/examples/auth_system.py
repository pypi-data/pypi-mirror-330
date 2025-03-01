"""Simple authentication system example using Manticore CockroachDB.

This example demonstrates:
- User authentication and registration
- Session token management with JWT
- Secure password hashing
"""

import datetime
import hashlib
import logging
import os
from typing import Dict, List, Optional
from uuid import UUID, uuid4

import jwt
from manticore_cockroachdb import Database, Table, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
JWT_SECRET = "your-secret-key"  # In production, use a secure environment variable
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY = datetime.timedelta(hours=24)


class AuthError(ValidationError):
    """Authentication related errors."""
    pass


class AuthSystem:
    """Simple authentication system example."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 26257,
        database: str = "auth",
        user: str = "root",
        password: str = "",
        min_pool_size: int = 2,
        max_pool_size: int = 10
    ):
        """Initialize auth system."""
        logger.info("Initializing auth system...")
        
        # Connect to default database first to ensure auth database exists
        default_db = Database(
            host=host,
            port=port,
            user=user,
            password=password,
            min_connections=min_pool_size,
            max_connections=max_pool_size,
        )
        
        try:
            logger.info("Setting up auth database...")
            default_db.execute('CREATE DATABASE IF NOT EXISTS "auth"', fetch=False)
        finally:
            default_db.close()
        
        # Connect to auth database
        logger.info("Connecting to auth database...")
        self.db = Database(
            database=database,
            host=host,
            port=port,
            user=user,
            password=password,
            min_connections=min_pool_size,
            max_connections=max_pool_size,
        )
        
        # Initialize schema
        self._init_schema()
        
        # Create table objects for easier access
        self.users_table = Table("users", self.db)
        self.sessions_table = Table("sessions", self.db)
    
    def _init_schema(self) -> None:
        """Initialize database schema."""
        logger.info("Initializing database schema...")
        
        # Define table schemas
        users_schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "username": "TEXT NOT NULL UNIQUE",
            "password": "TEXT NOT NULL",
            "email": "TEXT UNIQUE",
            "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
        }
        
        sessions_schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "user_id": "UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE",
            "token": "TEXT NOT NULL UNIQUE",
            "expires_at": "TIMESTAMP WITH TIME ZONE NOT NULL",
            "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
            "revoked_at": "TIMESTAMP WITH TIME ZONE"
        }
        
        token_blacklist_schema = {
            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "token_hash": "TEXT NOT NULL UNIQUE",
            "revoked_at": "TIMESTAMP WITH TIME ZONE NOT NULL",
            "reason": "TEXT NOT NULL",
            "expires_at": "TIMESTAMP WITH TIME ZONE NOT NULL",
            "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
        }
        
        # Check if tables exist
        users_exists = self.db.exists("users")
        sessions_exists = self.db.exists("sessions")
        blacklist_exists = self.db.exists("token_blacklist")
        
        if users_exists and sessions_exists and blacklist_exists:
            logger.info("Schema already exists")
            # Initialize the tables
            self.users_table = Table("users", db=self.db, schema=users_schema)
            self.users_table.initialize()
            return
        
        # Create tables
        logger.info("Creating database schema...")
        
        def create_tables(conn):
            # Create users table
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create sessions table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        token TEXT NOT NULL UNIQUE,
                        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        revoked_at TIMESTAMP WITH TIME ZONE
                    )
                """)
                
                # Create token blacklist table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS token_blacklist (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        token_hash TEXT NOT NULL UNIQUE,
                        revoked_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        reason TEXT NOT NULL,
                        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        
        # Run in transaction
        self.db.run_in_transaction(create_tables)
        
        # Initialize the tables
        self.users_table = Table("users", db=self.db, schema=users_schema)
        self.users_table.initialize()
        
        self.sessions_table = Table("sessions", db=self.db, schema=sessions_schema)
        self.sessions_table.initialize()
    
    def _hash_password(self, password: str) -> str:
        """Hash a password."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self, user_id: UUID) -> Dict[str, str]:
        """Generate a JWT token for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with token and expiration
        """
        # Set expiration to 1 hour from now
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        
        # Create a payload
        payload = {
            "sub": str(user_id),
            "exp": int(expires_at.timestamp()),
            "iat": int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
            "jti": str(uuid4())
        }
        
        # Generate token
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        # Store in database
        session_data = {
            "user_id": user_id,
            "token": token,
            "expires_at": expires_at
        }
        
        # Use direct database operations instead of Table
        self.db.insert("sessions", session_data)
        
        return {
            "token": token,
            "expires_at": expires_at.isoformat()
        }
    
    def register(
        self,
        username: str,
        password: str,
        email: Optional[str] = None
    ) -> Dict[str, str]:
        """Register a new user."""
        try:
            # Check if username already exists
            existing_user = self.db.select("users", where={"username": username})
            if existing_user:
                raise AuthError(f"Username '{username}' is already taken")
            
            # Check if email already exists (if provided)
            if email:
                existing_email = self.db.select("users", where={"email": email})
                if existing_email:
                    raise AuthError(f"Email '{email}' is already registered")
            
            # Create user
            user = self.users_table.create({
                "username": username,
                "password_hash": self._hash_password(password),
                "email": email
            })
            
            # Generate token
            token_data = self._generate_token(user["id"])
            
            return {
                "user_id": str(user["id"]),
                "username": user["username"],
                "token": token_data["token"],
                "expires_at": token_data["expires_at"]
            }
        except Exception as e:
            if isinstance(e, AuthError):
                raise
            logger.error(f"Registration failed: {str(e)}")
            raise AuthError("Registration failed") from e
    
    def login(self, username: str, password: str) -> Dict[str, str]:
        """Login a user."""
        # Check if user exists
        users = self.db.select("users", where={"username": username})
        
        if not users:
            raise AuthError("Invalid username or password")
        
        user = users[0]
        
        # Check password
        if user["password_hash"] != self._hash_password(password):
            raise AuthError("Invalid username or password")
        
        # Generate token
        token_data = self._generate_token(user["id"])
        
        return {
            "user_id": str(user["id"]),
            "username": user["username"],
            "token": token_data["token"],
            "expires_at": token_data["expires_at"]
        }
    
    def verify_token(self, token: str) -> Dict[str, any]:
        """Verify a JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Dict with user data
            
        Raises:
            AuthError: If token is invalid
        """
        try:
            # Check if token is in blacklist
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            blacklisted = self.db.execute(
                "SELECT COUNT(*) as count FROM token_blacklist WHERE token_hash = %s",
                (token_hash,)
            )[0]["count"] > 0
            
            if blacklisted:
                raise AuthError("Token has been revoked")
            
            # Check if token exists and is not expired or revoked
            session = self.db.execute(
                """
                SELECT * FROM sessions 
                WHERE token = %s AND expires_at > %s AND revoked_at IS NULL
                """,
                (token, datetime.datetime.now(datetime.timezone.utc))
            )
            
            if not session:
                raise AuthError("Invalid or expired token")
            
            # Decode token
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            # Get user
            users = self.db.select("users", where={"id": payload["sub"]})
            
            if not users:
                raise AuthError("User not found")
            
            user = users[0]
            
            return {
                "user_id": str(user["id"]),
                "username": user["username"],
                "email": user["email"],
                "exp": datetime.datetime.fromtimestamp(payload["exp"], tz=datetime.timezone.utc)
            }
            
        except jwt.PyJWTError as e:
            raise AuthError(f"Invalid token: {str(e)}")
    
    def logout(self, token: str) -> None:
        """Logout a user by revoking their token.
        
        Args:
            token: JWT token
            
        Raises:
            AuthError: If token is invalid
        """
        # Verify token first
        token_data = self.verify_token(token)
        
        # Mark token as revoked
        self.db.execute(
            "UPDATE sessions SET revoked_at = %s WHERE token = %s",
            (datetime.datetime.now(datetime.timezone.utc), token)
        )
        
        # Add to blacklist
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        expires_at = datetime.datetime.fromtimestamp(payload["exp"], tz=datetime.timezone.utc)
        
        self.db.execute(
            """
            INSERT INTO token_blacklist (token_hash, revoked_at, reason, expires_at)
            VALUES (%s, %s, %s, %s)
            """,
            (token_hash, datetime.datetime.now(datetime.timezone.utc), "User logout", expires_at)
        )
    
    def close(self):
        """Close database connection."""
        if hasattr(self, 'db'):
            self.db.close()


def main():
    """Run the example."""
    try:
        # Initialize auth system
        auth = AuthSystem()
        
        # Register a new user
        print("\nRegistering new user...")
        try:
            # Try with a different username to avoid conflicts
            user = auth.register("testuser_new", "password123")
            print(f"Registered user: {user}")
        except AuthError as e:
            print(f"Registration error: {str(e)}")
        
        # Try to register with the same username
        print("\nTrying to register duplicate username...")
        try:
            auth.register("testuser_new", "password456")
        except AuthError as e:
            print(f"Expected error: {str(e)}")
        
        # Login
        print("\nLogging in...")
        try:
            # Use the username that exists in the database
            login_data = auth.login("testuser", "password123")
            print(f"Login successful: {login_data}")
            
            # Verify token
            print("\nVerifying token...")
            try:
                user_data = auth.verify_token(login_data["token"])
                print(f"Token verified, user data: {user_data}")
            except AuthError as e:
                print(f"Token verification error: {str(e)}")
            
            # Logout
            print("\nLogging out...")
            auth.logout(login_data["token"])
            print("Logout successful")
            
            # Try to verify token after logout
            print("\nTrying to verify token after logout...")
            try:
                auth.verify_token(login_data["token"])
            except AuthError as e:
                print(f"Expected error: {str(e)}")
        except AuthError as e:
            print(f"Login error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Close database connection
        if 'auth' in locals():
            auth.close()


if __name__ == "__main__":
    main() 