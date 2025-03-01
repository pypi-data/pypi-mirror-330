# Synchronous Examples

This page provides practical examples of using the synchronous API of the Manticore CockroachDB client. These examples demonstrate common patterns and best practices for working with the library.

## Basic CRUD Operations

This example shows how to perform basic CRUD operations using the synchronous API:

```python
import uuid
from manticore_cockroachdb import Database, Table

def sync_crud_example():
    # Connect to database
    db = Database(database="testdb", host="localhost")
    db.connect()
    
    try:
        # Create a products table
        products = Table(
            "products",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "name": "TEXT NOT NULL",
                "price": "DECIMAL(10,2) NOT NULL",
                "stock": "INTEGER NOT NULL DEFAULT 0",
                "active": "BOOLEAN NOT NULL DEFAULT TRUE"
            }
        )
        
        # Initialize the table
        products.initialize()
        
        # Create a product
        product = products.create({
            "name": "Smartphone",
            "price": 799.99,
            "stock": 50
        })
        print("Created product: {}".format(product))
        
        # Read the product
        retrieved = products.read(product["id"])
        print("Retrieved product: {}".format(retrieved))
        
        # Update the product
        updated = products.update(product["id"], {
            "price": 749.99,
            "stock": 45
        })
        print("Updated product: {}".format(updated))
        
        # List all products
        all_products = products.list()
        print("All products: {}".format(all_products))
        
        # Delete the product
        deleted = products.delete(product["id"])
        print("Product deleted: {}".format(deleted))
        
    finally:
        # Close the database connection
        db.close()

if __name__ == "__main__":
    sync_crud_example()
```

## Working with Transactions

This example demonstrates how to use transactions with the synchronous API:

```python
from manticore_cockroachdb import Database, Table

def transaction_example():
    # Connect to database
    db = Database(database="testdb", host="localhost")
    db.connect()
    
    try:
        # Create tables
        accounts = Table(
            "accounts",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "owner": "TEXT NOT NULL",
                "balance": "DECIMAL(12,2) NOT NULL"
            }
        )
        accounts.initialize()
        
        # Create initial accounts
        account1 = accounts.create({
            "owner": "Alice",
            "balance": 1000.00
        })
        
        account2 = accounts.create({
            "owner": "Bob",
            "balance": 500.00
        })
        
        # Perform a transfer using a transaction
        def transfer_funds(conn):
            amount = 200.00
            
            # Deduct from account1
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE accounts SET balance = balance - %s WHERE id = %s RETURNING *",
                    (amount, account1["id"])
                )
                sender = cur.fetchone()
                
                # Add to account2
                cur.execute(
                    "UPDATE accounts SET balance = balance + %s WHERE id = %s RETURNING *",
                    (amount, account2["id"])
                )
                recipient = cur.fetchone()
                
                return {
                    "sender": sender,
                    "recipient": recipient,
                    "amount": amount
                }
        
        # Run the transfer in a transaction
        result = db.run_in_transaction(transfer_funds)
        print("Transfer completed: {}".format(result))
        
        # Verify the new balances
        updated_account1 = accounts.read(account1["id"])
        updated_account2 = accounts.read(account2["id"])
        
        print("{}'s balance: {}".format(updated_account1['owner'], updated_account1['balance']))
        print("{}'s balance: {}".format(updated_account2['owner'], updated_account2['balance']))
        
    finally:
        # Clean up
        db.drop_table("accounts")
        db.close()

if __name__ == "__main__":
    transaction_example()
```

## Batch Operations

This example shows how to perform batch operations efficiently:

```python
import random
from manticore_cockroachdb import Database, Table

def batch_operations_example():
    # Connect to database
    db = Database(database="testdb", host="localhost")
    db.connect()
    
    try:
        # Create a sensors table
        sensors = Table(
            "sensors",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "location": "TEXT NOT NULL",
                "type": "TEXT NOT NULL",
                "reading": "FLOAT NOT NULL",
                "timestamp": "TIMESTAMP DEFAULT NOW()"
            }
        )
        sensors.initialize()
        
        # Generate sensor data
        sensor_data = []
        locations = ["kitchen", "living_room", "bedroom", "bathroom", "garage"]
        types = ["temperature", "humidity", "pressure", "light"]
        
        for _ in range(20):
            sensor_data.append({
                "location": random.choice(locations),
                "type": random.choice(types),
                "reading": round(random.uniform(0, 100), 2)
            })
        
        # Insert all records in a batch
        inserted = sensors.batch_create(sensor_data)
        print("Inserted {} sensor readings".format(len(inserted)))
        
        # Query data - temperature sensors with high readings
        high_temps = sensors.list(
            where={"type": "temperature"},
            order_by="reading DESC",
            limit=5
        )
        
        print("\nHighest temperature readings:")
        for reading in high_temps:
            print("Location: {}, Reading: {}°C".format(reading['location'], reading['reading']))
        
        # Update multiple records in batch
        # For example, adjust all humidity readings
        humidity_readings = sensors.list(where={"type": "humidity"})
        for reading in humidity_readings:
            reading["reading"] = round(reading["reading"] * 0.95, 2)  # Adjust by 5%
        
        updated = sensors.batch_update(humidity_readings)
        print("\nUpdated {} humidity readings".format(len(updated)))
        
    finally:
        # Clean up
        db.drop_table("sensors")
        db.close()

if __name__ == "__main__":
    batch_operations_example()
```

## Using Context Managers

This example demonstrates how to use context managers for cleaner code:

```python
from manticore_cockroachdb import Database, Table

def context_manager_example():
    # Use database as context manager
    with Database(database="testdb", host="localhost") as db:
        # Use table as context manager
        with Table(
            "notes",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "title": "TEXT NOT NULL",
                "content": "TEXT",
                "created_at": "TIMESTAMP DEFAULT NOW()"
            }
        ) as notes:
            # Table is automatically initialized
            
            # Create notes
            notes.create({
                "title": "Shopping List",
                "content": "Milk, Eggs, Bread"
            })
            
            notes.create({
                "title": "Meeting Notes",
                "content": "Discuss project timeline and resource allocation"
            })
            
            # List all notes
            all_notes = notes.list(order_by="created_at DESC")
            
            print("Notes:")
            for note in all_notes:
                print("- {}: {}".format(note['title'], note['content']))
        
        # Clean up
        db.drop_table("notes")
        # Connection is automatically closed when exiting the context

if __name__ == "__main__":
    context_manager_example()
```

## Error Handling

This example shows proper error handling with the synchronous API:

```python
from manticore_cockroachdb import Database, Table
from psycopg.errors import UniqueViolation, ForeignKeyViolation

def error_handling_example():
    # Connect to database
    db = Database(database="testdb", host="localhost")
    db.connect()
    
    try:
        # Create a users table
        users = Table(
            "users_example",
            db=db,
            schema={
                "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                "username": "TEXT NOT NULL UNIQUE",  # Unique constraint
                "email": "TEXT NOT NULL"
            }
        )
        users.initialize()
        
        # Create a user
        try:
            user = users.create({
                "username": "johndoe",
                "email": "john@example.com"
            })
            print("Created user: {}".format(user['username']))
            
            # Try to create another user with the same username (will fail)
            duplicate_user = users.create({
                "username": "johndoe",  # Same username
                "email": "another@example.com"
            })
            
        except UniqueViolation as e:
            print("Couldn't create duplicate user: {}".format(e))
            
            # Handle the error and try a different username
            try:
                alternate_user = users.create({
                    "username": "johndoe2",  # Different username
                    "email": "another@example.com"
                })
                print("Created alternative user: {}".format(alternate_user['username']))
                
            except Exception as e2:
                print("Failed to create alternative user: {}".format(e2))
        
        # List all successful users
        all_users = users.list()
        print("Total users: {}".format(len(all_users)))
        for user in all_users:
            print("- {}: {}".format(user['username'], user['email']))
            
    except Exception as e:
        print("Unexpected error: {}".format(e))
        
    finally:
        # Clean up
        db.drop_table("users_example")
        db.close()

if __name__ == "__main__":
    error_handling_example()
```

## Custom SQL Queries

This example demonstrates how to execute custom SQL queries:

```python
from manticore_cockroachdb import Database

def custom_sql_example():
    # Connect to database
    db = Database(database="testdb", host="localhost")
    db.connect()
    
    try:
        # Create a table using raw SQL
        db.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                salary DECIMAL(10,2) NOT NULL,
                hire_date DATE NOT NULL
            )
        """)
        
        # Insert data using parameterized queries
        db.execute(
            """
            INSERT INTO employees (name, department, salary, hire_date)
            VALUES (%s, %s, %s, %s)
            """,
            ("John Smith", "Engineering", 85000.00, "2022-01-15")
        )
        
        db.execute(
            """
            INSERT INTO employees (name, department, salary, hire_date)
            VALUES (%s, %s, %s, %s)
            """,
            ("Sarah Johnson", "Marketing", 75000.00, "2022-03-10")
        )
        
        db.execute(
            """
            INSERT INTO employees (name, department, salary, hire_date)
            VALUES (%s, %s, %s, %s)
            """,
            ("Michael Brown", "Engineering", 92000.00, "2021-11-05")
        )
        
        # Query with aggregation
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    department, 
                    COUNT(*) as employee_count,
                    AVG(salary) as avg_salary,
                    MIN(hire_date) as earliest_hire
                FROM employees
                GROUP BY department
                ORDER BY avg_salary DESC
            """)
            
            results = cursor.fetchall()
            
            print("\nDepartment Statistics:")
            for row in results:
                print("Department: {}".format(row["department"]))
                print("  Employees: {}".format(row["employee_count"]))
                print("  Average Salary: ${:.2f}".format(row["avg_salary"]))
                print("  Earliest Hire: {}".format(row["earliest_hire"]))
                print("")
        
    finally:
        # Clean up
        db.drop_table("employees")
        db.close()

if __name__ == "__main__":
    custom_sql_example()
``` 