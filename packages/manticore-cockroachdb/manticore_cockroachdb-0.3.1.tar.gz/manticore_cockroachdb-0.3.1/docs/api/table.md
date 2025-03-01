# Table API

The `Table` class provides a convenient interface for performing CRUD operations on a specific database table using the synchronous API.

## Class Documentation

::: manticore_cockroachdb.crud.table.Table
    options:
      show_root_heading: true
      show_root_full_path: false
      show_source: true
      heading_level: 3
      members_order: source

## Usage Examples

```python
from manticore_cockroachdb import Database, Table

# Connect to database
db = Database(database="example_db")

# Create a table
db.create_table(
    "users",
    {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "name": "TEXT NOT NULL",
        "email": "TEXT UNIQUE NOT NULL",
        "age": "INTEGER",
        "active": "BOOLEAN DEFAULT TRUE"
    },
    if_not_exists=True
)

# Create a Table instance
users = Table("users", db=db)

# Create a user
user = users.create({
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})
print(f"Created user with ID: {user['id']}")

# Read a user
retrieved_user = users.read(user["id"])
print(f"Retrieved user: {retrieved_user['name']}")

# Update a user
updated_user = users.update(user["id"], {"age": 31})
print(f"Updated user age: {updated_user['age']}")

# List all users
all_users = users.list()
print(f"Total users: {len(all_users)}")

# Filter users
active_users = users.list(where={"active": True})
print(f"Active users: {len(active_users)}")

# Count users
user_count = users.count()
print(f"User count: {user_count}")

# Delete a user
users.delete(user["id"])
print("User deleted")

# Batch operations
batch_users = [
    {"name": "User 1", "email": "user1@example.com", "age": 21},
    {"name": "User 2", "email": "user2@example.com", "age": 22},
    {"name": "User 3", "email": "user3@example.com", "age": 23}
]

# Create multiple users in a batch
created_batch = users.batch_create(batch_users)
print(f"Created {len(created_batch)} users in batch")

# Update multiple users in a batch
updates = [
    {"id": created_batch[0]["id"], "age": 31},
    {"id": created_batch[1]["id"], "age": 32},
    {"id": created_batch[2]["id"], "age": 33}
]
updated_batch = users.batch_update(updates)
print(f"Updated {len(updated_batch)} users in batch")

# Delete multiple users in a batch
ids_to_delete = [user["id"] for user in created_batch]
users.batch_delete(ids_to_delete)
print(f"Deleted {len(ids_to_delete)} users in batch")
``` 