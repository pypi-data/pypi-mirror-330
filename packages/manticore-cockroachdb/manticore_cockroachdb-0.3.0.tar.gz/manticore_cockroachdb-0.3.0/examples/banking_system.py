"""Example of a simple banking system using Manticore CockroachDB.

This example demonstrates:
- Database connection and connection pooling
- CRUD operations with error handling
- Advanced transaction management with retries
- Batch operations
- Schema migrations
- Production-ready logging
"""

import logging
import os
from decimal import Decimal
from typing import List, Optional, Tuple, Union
from uuid import UUID

from manticore_cockroachdb import Database, DatabaseError, Migrator, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InsufficientFundsError(ValidationError):
    """Raised when account has insufficient funds."""
    pass


class AccountNotFoundError(DatabaseError):
    """Raised when account is not found."""
    pass


class BankingSystem:
    """Enterprise banking system example."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 26257,
        database: str = "bank",
        user: str = "root",
        password: str = "",
        sslmode: str = "disable",
        min_pool_size: int = 2,
        max_pool_size: int = 10
    ):
        """Initialize banking system.
        
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
        # First connect to the default database to create our bank database
        logger.info("Initializing banking system...")
        
        # Use DATABASE_URL if available, otherwise use parameters
        if "DATABASE_URL" in os.environ:
            logger.info("Using DATABASE_URL for connection")
            self.default_db = Database.from_url(os.environ["DATABASE_URL"])
        else:
            logger.info("Using connection parameters")
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
            # Drop the bank database if it exists
            logger.info("Cleaning up existing database...")
            self.default_db.run_in_transaction(
                lambda conn: conn.execute('DROP DATABASE IF EXISTS "bank" CASCADE;')
            )
            
            # Create the bank database
            logger.info("Creating new database...")
            self.default_db.run_in_transaction(
                lambda conn: conn.execute('CREATE DATABASE "bank";')
            )
        finally:
            self.default_db.close()
        
        # Connect to bank database with connection pooling
        logger.info("Connecting to bank database with connection pool...")
        if "DATABASE_URL" in os.environ:
            # Modify DATABASE_URL to use the bank database
            url_parts = os.environ["DATABASE_URL"].split("/")
            url_parts[-1] = "bank" + "?" + url_parts[-1].split("?", 1)[1]
            bank_url = "/".join(url_parts)
            self.db = Database.from_url(bank_url)
        else:
            self.db = Database(
                database=database,
                host=host,
                port=port,
                user=user,
                password=password,
                sslmode=sslmode,
                min_connections=min_pool_size,
                max_connections=max_pool_size,
                application_name="banking-system"
            )
        
        # Initialize schema
        self._init_schema()
    
    def _init_schema(self) -> None:
        """Initialize database schema using migrations."""
        logger.info("Initializing database schema...")
        migrator = Migrator(self.db)
        
        # Get existing migrations
        existing = migrator.load_migrations()
        if not existing:
            # Create initial schema
            migrator.create_migration(
                "create_accounts",
                """
                CREATE TABLE accounts (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    owner TEXT NOT NULL,
                    balance DECIMAL(19,4) NOT NULL DEFAULT 0.0000,
                    type TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT balance_non_negative CHECK (balance >= 0.0000)
                )
                """,
                "DROP TABLE accounts"
            )
            
            # Add account status and metadata
            migrator.create_migration(
                "add_account_status",
                """
                ALTER TABLE accounts 
                ADD COLUMN status TEXT NOT NULL DEFAULT 'active',
                ADD COLUMN email TEXT UNIQUE,
                ADD COLUMN last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                ADD CONSTRAINT valid_status CHECK (status IN ('active', 'inactive', 'suspended'))
                """,
                """
                ALTER TABLE accounts 
                DROP COLUMN status,
                DROP COLUMN email,
                DROP COLUMN last_updated
                """
            )
            
            # Create transactions table with constraints
            migrator.create_migration(
                "create_transactions",
                """
                CREATE TABLE transactions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    from_account UUID REFERENCES accounts(id),
                    to_account UUID REFERENCES accounts(id),
                    amount DECIMAL(19,4) NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP WITH TIME ZONE,
                    description TEXT,
                    CONSTRAINT amount_positive CHECK (amount > 0.0000),
                    CONSTRAINT valid_type CHECK (type IN ('transfer', 'deposit', 'withdrawal')),
                    CONSTRAINT valid_status CHECK (status IN ('pending', 'completed', 'failed'))
                )
                """,
                "DROP TABLE transactions"
            )
        
        # Apply all migrations
        migrator.migrate()
        logger.info("Schema initialization complete")
    
    def create_account(
        self,
        owner: str,
        account_type: str,
        initial_balance: Decimal = Decimal("0.0000"),
        email: Optional[str] = None
    ) -> dict:
        """Create a new account.
        
        Args:
            owner: Account owner name
            account_type: Account type (checking/savings)
            initial_balance: Initial account balance
            email: Optional email address
            
        Returns:
            Created account
            
        Raises:
            ValidationError: If account data is invalid
        """
        # Validate input
        if initial_balance < 0:
            raise ValidationError("Initial balance cannot be negative")
        if account_type not in ("checking", "savings"):
            raise ValidationError("Invalid account type")
            
        try:
            return self.db.insert(
                "accounts",
                {
                    "owner": owner,
                    "balance": initial_balance,
                    "type": account_type,
                    "status": "active",
                    "email": email
                }
            )
        except Exception as e:
            logger.error(f"Failed to create account: {e}")
            raise DatabaseError("Failed to create account") from e
    
    def get_account(self, account_id: Union[str, UUID]) -> dict:
        """Get account details.
        
        Args:
            account_id: Account ID (string or UUID)
            
        Returns:
            Account details
            
        Raises:
            AccountNotFoundError: If account is not found or ID is invalid
        """
        # Validate UUID format if string
        if isinstance(account_id, str):
            try:
                account_id = UUID(account_id)
            except ValueError:
                raise AccountNotFoundError(f"Invalid account ID format: {account_id}")
            
        accounts = self.db.select("accounts", where={"id": account_id})
        if not accounts:
            raise AccountNotFoundError(f"Account {account_id} not found")
        return accounts[0]
    
    def get_balance(self, account_id: str) -> Decimal:
        """Get account balance.
        
        Args:
            account_id: Account ID
            
        Returns:
            Account balance
            
        Raises:
            AccountNotFoundError: If account is not found
        """
        account = self.get_account(account_id)
        return account["balance"]
    
    def transfer(
        self,
        from_account: str,
        to_account: str,
        amount: Decimal,
        description: Optional[str] = None
    ) -> dict:
        """Transfer money between accounts.
        
        Args:
            from_account: Source account ID
            to_account: Target account ID
            amount: Transfer amount
            description: Optional transfer description
            
        Returns:
            Transaction record
            
        Raises:
            ValidationError: If transfer amount is invalid
            AccountNotFoundError: If either account is not found
            InsufficientFundsError: If source account has insufficient funds
        """
        # Validate amount
        if amount <= 0:
            raise ValidationError("Transfer amount must be positive")
            
        def execute_transfer(conn):
            with conn.cursor() as cur:
                # Lock accounts in consistent order to prevent deadlocks
                account_ids = sorted([from_account, to_account])
                cur.execute(
                    "SELECT * FROM accounts WHERE id = ANY(%s) FOR UPDATE",
                    (account_ids,)
                )
                accounts = cur.fetchall()
                
                if len(accounts) != 2:
                    raise AccountNotFoundError("One or both accounts not found")
                    
                # Map accounts by ID
                account_map = {str(a["id"]): a for a in accounts}
                source = account_map[str(from_account)]
                target = account_map[str(to_account)]
                
                # Verify accounts are active
                if source["status"] != "active":
                    raise ValidationError("Source account is not active")
                if target["status"] != "active":
                    raise ValidationError("Target account is not active")
                
                # Check sufficient funds
                if source["balance"] < amount:
                    raise InsufficientFundsError(
                        f"Insufficient funds: {source['balance']} < {amount}"
                    )
                
                # Create transaction record
                cur.execute(
                    """
                    INSERT INTO transactions (
                        from_account, to_account, amount, type,
                        status, description, completed_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    RETURNING *
                    """,
                    (
                        from_account, to_account, amount,
                        "transfer", "completed", description
                    )
                )
                transaction = cur.fetchone()
                
                # Update account balances
                cur.execute(
                    """
                    UPDATE accounts 
                    SET balance = balance - %s,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (amount, from_account)
                )
                cur.execute(
                    """
                    UPDATE accounts 
                    SET balance = balance + %s,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (amount, to_account)
                )
                
                return transaction
        
        try:
            return self.db.run_in_transaction(execute_transfer)
        except (ValidationError, AccountNotFoundError, InsufficientFundsError):
            raise
        except Exception as e:
            logger.error(f"Transfer failed: {e}")
            raise DatabaseError("Transfer failed") from e
    
    def batch_create_accounts(
        self,
        accounts: List[dict]
    ) -> List[dict]:
        """Create multiple accounts in a batch.
        
        Args:
            accounts: List of account data
            
        Returns:
            List of created accounts
            
        Raises:
            ValidationError: If any account data is invalid
        """
        # Validate all accounts first
        for account in accounts:
            if account.get("balance", 0) < 0:
                raise ValidationError("Initial balance cannot be negative")
            if account.get("type") not in ("checking", "savings"):
                raise ValidationError("Invalid account type")
        
        try:
            return self.db.batch_insert("accounts", accounts)
        except Exception as e:
            logger.error(f"Batch account creation failed: {e}")
            raise DatabaseError("Failed to create accounts") from e
    
    def get_transaction_history(
        self,
        account_id: str,
        limit: int = 10
    ) -> List[dict]:
        """Get transaction history for an account.
        
        Args:
            account_id: Account ID
            limit: Maximum number of transactions to return
            
        Returns:
            List of transactions
            
        Raises:
            AccountNotFoundError: If account is not found
        """
        # Verify account exists
        self.get_account(account_id)
        
        return self.db.select(
            "transactions",
            where={
                "from_account": account_id,
                "status": "completed"
            },
            order_by="created_at DESC",
            limit=limit
        )
    
    def get_account_statistics(self, account_id: str) -> dict:
        """Get account statistics.
        
        Args:
            account_id: Account ID
            
        Returns:
            Account statistics
            
        Raises:
            AccountNotFoundError: If account is not found
        """
        def calculate_stats(conn):
            with conn.cursor() as cur:
                # Get total sent
                cur.execute(
                    """
                    SELECT COALESCE(SUM(amount), 0) as total_sent,
                           COUNT(*) as num_sent
                    FROM transactions
                    WHERE from_account = %s AND status = 'completed'
                    """,
                    (account_id,)
                )
                sent_stats = cur.fetchone()
                
                # Get total received
                cur.execute(
                    """
                    SELECT COALESCE(SUM(amount), 0) as total_received,
                           COUNT(*) as num_received
                    FROM transactions
                    WHERE to_account = %s AND status = 'completed'
                    """,
                    (account_id,)
                )
                received_stats = cur.fetchone()
                
                return {
                    "total_sent": sent_stats["total_sent"],
                    "total_received": received_stats["total_received"],
                    "num_transactions": sent_stats["num_sent"] + received_stats["num_received"],
                    "net_transfer": received_stats["total_received"] - sent_stats["total_sent"]
                }
        
        # Verify account exists first
        self.get_account(account_id)
        
        try:
            return self.db.run_in_transaction(calculate_stats)
        except Exception as e:
            logger.error(f"Failed to get account statistics: {e}")
            raise DatabaseError("Failed to get account statistics") from e
    
    def close(self) -> None:
        """Close database connections."""
        self.db.close()


def main():
    """Run example banking system."""
    # Initialize banking system with connection pooling
    bank = BankingSystem(
        min_pool_size=2,
        max_pool_size=10
    )
    
    try:
        # Create accounts with email addresses
        logger.info("\nCreating accounts...")
        alice = bank.create_account(
            "Alice",
            "checking",
            Decimal("1000.0000"),
            "alice@example.com"
        )
        bob = bank.create_account(
            "Bob",
            "savings",
            Decimal("500.0000"),
            "bob@example.com"
        )
        
        logger.info("Created accounts:")
        logger.info(f"Alice: {alice}")
        logger.info(f"Bob: {bob}")
        
        # Demonstrate error handling for insufficient funds
        logger.info("\nTesting insufficient funds error...")
        try:
            bank.transfer(
                alice["id"],
                bob["id"],
                Decimal("2000.0000"),
                "This should fail"
            )
        except InsufficientFundsError as e:
            logger.info(f"Transfer failed as expected: {e}")
        
        # Perform successful transfer
        logger.info("\nPerforming transfer...")
        transfer = bank.transfer(
            alice["id"],
            bob["id"],
            Decimal("100.0000"),
            "Test transfer"
        )
        logger.info(f"Transfer completed: {transfer}")
        
        # Check balances
        logger.info("\nChecking balances...")
        alice_balance = bank.get_balance(alice["id"])
        bob_balance = bank.get_balance(bob["id"])
        
        logger.info("Final balances:")
        logger.info(f"Alice: ${alice_balance}")
        logger.info(f"Bob: ${bob_balance}")
        
        # Batch create accounts
        logger.info("\nBatch creating accounts...")
        new_accounts = [
            {
                "owner": f"User {i}",
                "balance": Decimal(f"{i}00.0000"),
                "type": "checking",
                "status": "active",
                "email": f"user{i}@example.com"
            }
            for i in range(1, 4)
        ]
        
        created = bank.batch_create_accounts(new_accounts)
        logger.info(f"Batch created accounts: {created}")
        
        # Get transaction history
        logger.info("\nGetting Alice's transaction history...")
        history = bank.get_transaction_history(alice["id"])
        logger.info(f"Transaction history: {history}")
        
        # Get account statistics
        logger.info("\nGetting account statistics...")
        alice_stats = bank.get_account_statistics(alice["id"])
        logger.info(f"Alice's statistics: {alice_stats}")
        
        # Demonstrate error handling for invalid account
        logger.info("\nTesting invalid account error...")
        try:
            bank.get_account("invalid-id")
        except AccountNotFoundError as e:
            logger.info(f"Account lookup failed as expected: {e}")
        
    finally:
        bank.close()


if __name__ == "__main__":
    main() 