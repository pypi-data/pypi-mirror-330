"""Example of an authentication system using Manticore CockroachDB.

This example demonstrates:
- User authentication and registration
- Session token management with JWT
- Token blacklisting for logout
- Rate limiting support
- Secure password hashing
- Session tracking and management
"""

import datetime
import hashlib
import json
import logging
import os
from typing import Optional, Dict, List
from uuid import UUID, uuid4

import jwt
from manticore_cockroachdb import Database, DatabaseError, Migrator, ValidationError
import psycopg

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
JWT_SECRET = "your-secret-key"  # In production, use a secure environment variable
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY = datetime.timedelta(hours=24)
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = datetime.timedelta(minutes=15)


class AuthError(ValidationError):
    """Authentication related errors."""
    pass


class AuthSystem:
    """Authentication system example."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 26257,
        database: str = "auth",
        user: str = "root",
        password: str = "",
        sslmode: str = "disable",
        min_pool_size: int = 2,
        max_pool_size: int = 10
    ):
        """Initialize auth system.
        
        Args:
            host: Database host
            port: Database port
            database: Database name
            user: Database user
            password: Database password
            sslmode: SSL mode
            min_pool_size: Minimum connection pool size
            max_pool_size: Maximum connection pool size
        """
        logger.info("Initializing auth system...")
        
        # Use DATABASE_URL if available, otherwise use parameters
        if "DATABASE_URL" in os.environ:
            logger.info("Using DATABASE_URL for connection")
            # Parse the URL to get the base components
            url = os.environ["DATABASE_URL"]
            base_url = url.split("?")[0]
            query_params = url.split("?")[1] if "?" in url else ""
            
            # Connect to default database first
            logger.info("Connecting to default database...")
            default_db = Database.from_url(url)
            try:
                # Create auth database
                logger.info("Creating auth database if it doesn't exist...")
                default_db.run_in_transaction(
                    lambda conn: conn.execute('CREATE DATABASE IF NOT EXISTS "auth"')
                )
            finally:
                default_db.close()
            
            # Create auth database URL
            auth_url = f"{base_url.rsplit('/', 1)[0]}/auth"
            if query_params:
                auth_url = f"{auth_url}?{query_params}"
            
            # Connect to auth database
            logger.info("Connecting to auth database...")
            self.db = Database.from_url(auth_url)
        else:
            logger.info("Using connection parameters")
            # Create auth database
            self.default_db = Database(
                host=host,
                port=port,
                database="defaultdb",
                user=user,
                password=password,
                min_connections=min_pool_size,
                max_connections=max_pool_size,
            )
            
            try:
                logger.info("Setting up auth database...")
                self.default_db.run_in_transaction(
                    lambda conn: conn.execute('CREATE DATABASE IF NOT EXISTS "auth"')
                )
            finally:
                self.default_db.close()
            
            # Connect to auth database
            logger.info("Connecting to auth database...")
            self.db = Database(
                database=database,
                host=host,
                port=port,
                user=user,
                password=password,
                sslmode=sslmode,
                min_connections=min_pool_size,
                max_connections=max_pool_size,
                application_name="auth-system"
            )
        
        # Initialize schema
        self._init_schema()
    
    def _init_schema(self) -> None:
        """Initialize database schema using migrations."""
        logger.info("Initializing database schema...")
        
        # Check if tables exist by querying information schema
        tables_exist = False
        try:
            result = self.db.execute("""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_name IN ('users', 'sessions', 'token_blacklist')
                AND table_schema = 'public'
            """)
            tables_exist = result[0]["count"] == 3
        except DatabaseError:
            logger.info("Error checking tables, assuming they don't exist")
        
        if tables_exist:
            logger.info("Schema already exists")
            return
            
        logger.info("Tables don't exist, creating schema...")
        
        # Create tables in a transaction
        def create_tables(conn):
            with conn.cursor() as cur:
                # Create users table
                cur.execute("""
                    CREATE TABLE users (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        username TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        email TEXT UNIQUE,
                        failed_attempts INTEGER NOT NULL DEFAULT 0,
                        last_failed_attempt TIMESTAMP WITH TIME ZONE,
                        locked_until TIMESTAMP WITH TIME ZONE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create sessions table
                cur.execute("""
                    CREATE TABLE sessions (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id UUID NOT NULL REFERENCES users(id),
                        token TEXT NOT NULL UNIQUE,
                        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        revoked_at TIMESTAMP WITH TIME ZONE,
                        CONSTRAINT valid_session CHECK (
                            revoked_at IS NULL OR revoked_at > created_at
                        )
                    )
                """)
                
                # Create token blacklist table
                cur.execute("""
                    CREATE TABLE token_blacklist (
                        token_hash TEXT PRIMARY KEY,
                        revoked_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        reason TEXT,
                        expires_at TIMESTAMP WITH TIME ZONE NOT NULL
                    )
                """)
        
        # Run table creation in a transaction
        self.db.run_in_transaction(create_tables)
        logger.info("Schema initialization complete")
    
    def _hash_password(self, password: str) -> str:
        """Hash a password (in production, use a proper password hashing library)."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self, user_id: UUID) -> Dict[str, str]:
        """Generate a new JWT token."""
        expires_at = datetime.datetime.utcnow() + TOKEN_EXPIRY
        token_data = {
            "sub": str(user_id),
            "exp": expires_at,
            "iat": datetime.datetime.utcnow(),
            "jti": str(uuid4())
        }
        token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        # Store session
        self.db.insert(
            "sessions",
            {
                "user_id": user_id,
                "token": token,
                "expires_at": expires_at
            }
        )
        
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
        """Register a new user.
        
        Args:
            username: Username
            password: Password
            email: Optional email
            
        Returns:
            New user data with auth token
            
        Raises:
            AuthError: If registration fails
        """
        try:
            # Create user
            user = self.db.insert(
                "users",
                {
                    "username": username,
                    "password_hash": self._hash_password(password),
                    "email": email
                }
            )
            
            # Generate token
            token_data = self._generate_token(user["id"])
            
            return {
                "user_id": str(user["id"]),
                "username": user["username"],
                "token": token_data["token"],
                "expires_at": token_data["expires_at"]
            }
        except DatabaseError as e:
            if isinstance(e.__cause__, psycopg.errors.UniqueViolation):
                if "users_username_key" in str(e.__cause__):
                    raise AuthError(f"Username '{username}' is already taken")
                elif "users_email_key" in str(e.__cause__):
                    raise AuthError(f"Email '{email}' is already registered")
            raise AuthError("Registration failed") from e
    
    def login(self, username: str, password: str) -> Dict[str, str]:
        """Login a user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            User data with auth token
            
        Raises:
            AuthError: If login fails
        """
        # Check if user exists and isn't locked
        users = self.db.select(
            "users",
            where={"username": username}
        )
        
        if not users:
            raise AuthError("Invalid username or password")
        
        user = users[0]
        
        # Check if account is locked
        if user["locked_until"] and user["locked_until"] > datetime.datetime.utcnow():
            raise AuthError(
                f"Account locked until {user['locked_until'].isoformat()}"
            )
        
        # Verify password
        if user["password_hash"] != self._hash_password(password):
            # Update failed attempts
            now = datetime.datetime.utcnow()
            failed_attempts = user["failed_attempts"] + 1
            update_data = {
                "failed_attempts": failed_attempts,
                "last_failed_attempt": now
            }
            
            # Lock account if too many failures
            if failed_attempts >= MAX_FAILED_ATTEMPTS:
                update_data["locked_until"] = now + LOCKOUT_DURATION
            
            self.db.update(
                "users",
                update_data,
                {"id": user["id"]}
            )
            
            raise AuthError("Invalid username or password")
        
        # Reset failed attempts on successful login
        self.db.update(
            "users",
            {
                "failed_attempts": 0,
                "last_failed_attempt": None,
                "locked_until": None
            },
            {"id": user["id"]}
        )
        
        # Generate token
        token_data = self._generate_token(user["id"])
        
        return {
            "user_id": str(user["id"]),
            "username": user["username"],
            "token": token_data["token"],
            "expires_at": token_data["expires_at"]
        }
    
    def logout(self, token: str) -> None:
        """Logout a user by revoking their token.
        
        Args:
            token: JWT token to revoke
        """
        try:
            # Verify token
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            # Revoke session
            self.db.update(
                "sessions",
                {"revoked_at": datetime.datetime.utcnow()},
                {"token": token}
            )
            
            # Add to blacklist
            self.db.insert(
                "token_blacklist",
                {
                    "token_hash": hashlib.sha256(token.encode()).hexdigest(),
                    "reason": "logout",
                    "expires_at": datetime.datetime.fromtimestamp(payload["exp"])
                }
            )
        except jwt.InvalidTokenError as e:
            raise AuthError("Invalid token") from e
    
    def verify_token(self, token: str) -> Dict[str, any]:
        """Verify a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Token payload if valid
            
        Raises:
            AuthError: If token is invalid
        """
        try:
            # Check blacklist
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            blacklisted = self.db.select(
                "token_blacklist",
                where={"token_hash": token_hash}
            )
            if blacklisted:
                raise AuthError("Token has been revoked")
            
            # Verify token
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            # Check if session is still valid
            sessions = self.db.select(
                "sessions",
                where={
                    "token": token,
                    "revoked_at": None
                }
            )
            if not sessions:
                raise AuthError("Session has been revoked")
            
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthError("Invalid token") from e
    
    def get_active_sessions(self, user_id: UUID) -> List[Dict[str, any]]:
        """Get all active sessions for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of active sessions
        """
        return self.db.select(
            "sessions",
            where={
                "user_id": user_id,
                "revoked_at": None,
                "expires_at": {"$gt": datetime.datetime.utcnow()}
            }
        )
    
    def revoke_all_sessions(self, user_id: UUID) -> None:
        """Revoke all active sessions for a user.
        
        Args:
            user_id: User ID
        """
        # Get active sessions
        sessions = self.get_active_sessions(user_id)
        
        # Revoke sessions
        now = datetime.datetime.utcnow()
        self.db.batch_update(
            "sessions",
            [
                {
                    "id": session["id"],
                    "revoked_at": now
                }
                for session in sessions
            ]
        )
        
        # Add tokens to blacklist
        self.db.batch_insert(
            "token_blacklist",
            [
                {
                    "token_hash": hashlib.sha256(session["token"].encode()).hexdigest(),
                    "reason": "user_logout_all",
                    "expires_at": session["expires_at"]
                }
                for session in sessions
            ]
        )


def main():
    """Run example authentication system."""
    auth = AuthSystem()
    
    try:
        # Register a new user
        logger.info("\nRegistering new user...")
        try:
            user_data = auth.register(
                "testuser3",
                "password123",
                "test3@example.com"
            )
            logger.info(f"Registered user: {json.dumps(user_data, indent=2)}")
        except AuthError as e:
            logger.error(f"Registration failed: {e}")
            return
        
        # Try registering same username (should fail)
        logger.info("\nTrying to register duplicate username...")
        try:
            auth.register(
                "testuser3",
                "different_password",
                "other@example.com"
            )
        except AuthError as e:
            logger.info(f"Registration failed as expected: {e}")
        
        # Login with wrong password (demonstrate lockout)
        logger.info("\nTesting account lockout...")
        for i in range(MAX_FAILED_ATTEMPTS + 1):
            try:
                auth.login("testuser3", "wrong_password")
            except AuthError as e:
                logger.info(f"Login attempt {i + 1} failed: {e}")
        
        # Try correct password (should fail due to lockout)
        logger.info("\nTrying correct password while locked...")
        try:
            auth.login("testuser3", "password123")
        except AuthError as e:
            logger.info(f"Login failed as expected: {e}")
        
        # Login successfully (after manually clearing lockout)
        logger.info("\nClearing lockout and logging in...")
        auth.db.update(
            "users",
            {
                "failed_attempts": 0,
                "locked_until": None
            },
            {"username": "testuser3"}
        )
        login_data = auth.login("testuser3", "password123")
        logger.info(f"Login successful: {json.dumps(login_data, indent=2)}")
        
        # Verify token
        logger.info("\nVerifying token...")
        payload = auth.verify_token(login_data["token"])
        logger.info(f"Token payload: {json.dumps(payload, indent=2)}")
        
        # Get active sessions
        logger.info("\nGetting active sessions...")
        sessions = auth.get_active_sessions(UUID(login_data["user_id"]))
        logger.info(f"Active sessions: {len(sessions)}")
        
        # Logout
        logger.info("\nLogging out...")
        auth.logout(login_data["token"])
        
        # Try using revoked token
        logger.info("\nTrying to use revoked token...")
        try:
            auth.verify_token(login_data["token"])
        except AuthError as e:
            logger.info(f"Token verification failed as expected: {e}")
        
        # Login from multiple devices
        logger.info("\nSimulating multi-device login...")
        tokens = []
        for i in range(3):
            login_data = auth.login("testuser3", "password123")
            tokens.append(login_data["token"])
            logger.info(f"Device {i + 1} logged in")
        
        # Revoke all sessions
        logger.info("\nRevoking all sessions...")
        auth.revoke_all_sessions(UUID(login_data["user_id"]))
        
        # Try using any token
        logger.info("\nTrying to use tokens after revocation...")
        for i, token in enumerate(tokens, 1):
            try:
                auth.verify_token(token)
            except AuthError as e:
                logger.info(f"Device {i} token invalid as expected: {e}")
    
    finally:
        auth.db.close()


if __name__ == "__main__":
    main() 