# Manticore CockroachDB Examples

This directory contains example applications demonstrating the usage of the Manticore CockroachDB client library.

## Banking System Example

`banking_system.py` demonstrates a simple banking system with the following features:

- Database and table creation
- Schema migrations
- Account management (create, read, update)
- Money transfers with transaction management
- Batch operations
- Error handling and logging

### Running the Example

1. Install the package:
```bash
pip install manticore-cockroachdb
```

2. Start CockroachDB:
```bash
cockroach start-single-node --insecure
```

3. Run the example:
```bash
python banking_system.py
```

The example will:
1. Create a new database named "bank"
2. Set up tables using migrations
3. Create accounts for Alice and Bob
4. Perform a money transfer
5. Create additional accounts using batch operations

## Authentication System Example

`auth_system.py` demonstrates a production-ready authentication system with the following features:

- User registration and login
- JWT token-based authentication
- Session management and tracking
- Token blacklisting for secure logout
- Account lockout after failed attempts
- Multi-device session support
- Database-backed token revocation

### Running the Auth Example

1. Install required packages:
```bash
pip install manticore-cockroachdb pyjwt
```

2. Start CockroachDB:
```bash
cockroach start-single-node --insecure
```

3. Run the example:
```bash
python auth_system.py
```

The example will:
1. Create a new database named "auth"
2. Set up user and session tables using migrations
3. Register a test user
4. Demonstrate login and token generation
5. Show account lockout after failed attempts
6. Manage multiple device sessions
7. Handle token revocation and blacklisting

## More Examples

More examples will be added to demonstrate:
- Connection pooling optimization
- Advanced transaction patterns
- Schema management
- Integration with web frameworks
- Deployment patterns 