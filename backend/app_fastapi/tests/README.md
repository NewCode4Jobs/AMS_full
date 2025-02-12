# Database Testing Configuration

## Running Tests for Different Databases

This test suite supports multiple database types. You can specify the database type using the `TEST_DB_TYPE` environment variable.

pytest backend/app_fastapi/tests/ -v

### Supported Database Types
- `sqlite` (default)
- `postgres`
- `mongodb`

### Running Tests

#### SQLite (Default)
```bash
pytest
```

#### PostgreSQL
```bash
TEST_DB_TYPE=postgres pytest
```

#### MongoDB
```bash
TEST_DB_TYPE=mongodb pytest
```

## Configuration Details

- Each database type has its own configuration file in the `configs/` directory.
- The `conftest.py` dynamically loads the appropriate configuration based on `TEST_DB_TYPE`.
- Ensure you have the necessary database connection settings in your `.env` file.

### Important Notes
- For PostgreSQL and MongoDB, make sure you have the corresponding database running and accessible.
- Connection settings are read from the application's configuration files.
- Test databases are created with a `_test` suffix to avoid interfering with production data.
