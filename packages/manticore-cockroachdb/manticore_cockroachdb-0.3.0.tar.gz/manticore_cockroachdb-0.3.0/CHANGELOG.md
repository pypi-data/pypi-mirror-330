# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-05-02

### Added
- Improved documentation with MkDocs
- Comprehensive API reference documentation
- Enhanced example code in documentation
- Additional test coverage for async operations
- Better type hints for IDE integration

### Changed
- Refined error handling for better debugging
- Optimized connection pooling for higher performance
- Updated dependencies to latest versions
- Code quality improvements and refactoring

## [0.2.0] - 2024-02-28

### Added
- Full async/await support for all database operations
- New async components:
  - `AsyncDatabase` for core database operations
  - `AsyncTransaction` for transaction management
  - `AsyncMigration` and `AsyncMigrator` for schema migrations
  - `AsyncTable` for high-level CRUD operations
- Comprehensive documentation with MkDocs:
  - Detailed API reference for both sync and async APIs
  - Code examples for common use cases
  - Migration guides
  - Performance optimization guides
- Improved test coverage with pytest-asyncio
- Additional examples for both sync and async APIs

### Changed
- Updated development dependencies
- Improved error handling and logging
- Enhanced connection management in async mode
- Better type annotations

## [0.1.0] - 2024-02-19

### Added
- Initial release of Manticore CockroachDB client
- High-performance connection pooling with configurable settings
- Comprehensive CRUD operations with batch support
- Schema migrations with versioning and rollback support
- Transaction management with automatic retries and exponential backoff
- Type-safe operations with proper error handling
- Extensive test coverage (90%+)
- Production-ready logging and monitoring
- Comprehensive documentation and examples

### Security
- SSL/TLS support for secure database connections
- Proper password and credential handling
- Connection pool security features
- SQL injection prevention through parameterized queries
