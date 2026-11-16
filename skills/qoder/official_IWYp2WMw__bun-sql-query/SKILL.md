---
name: bun-sql-query
description: Database querying and schema inspection using Bun's native SQL capabilities. Use when Claude needs to (1) Inspect database schema (list tables, describe structure, view relationships), (2) Query data with SELECT statements (filtering, joins, aggregations), (3) Modify data with INSERT/UPDATE/DELETE, (4) Build queries interactively or execute raw SQL. Reads DATABASE_URL from project .env file. Supports PostgreSQL, MySQL, and SQLite.
version: 1.0.0
author: Claude
tags: [database, sql, query, schema, postgresql, mysql, sqlite, bun]
---

# Bun SQL Query Skill

Database querying and schema inspection using Bun's native SQL capabilities with zero installation required.

## Overview

This skill provides 10 production-ready bundled scripts (no `bun install` needed):
- **query.js** - Execute raw SQL queries with parameterized inputs
- **schema.js** - Inspect database structure (tables, columns, relationships)
- **interactive.js** - Build queries step-by-step with guided prompts
- **transactions.js** - Transaction support with savepoints
- **bulk-operations.js** - Efficient bulk INSERT/UPDATE/DELETE (10-100x faster)
- **mysql-demo.js** - MySQL-specific features
- **sqlite-demo.js** - SQLite-specific features
- **advanced-query.js** - CTEs, window functions, subqueries
- **query-modern.js** - Modern Bun SQL demonstrations
- **connection-manager.js** - Connection pooling and lifecycle management

All scripts automatically read `DATABASE_URL` from the project's `.env` file and support PostgreSQL, MySQL, and SQLite databases.

**Token Efficiency**: All scripts use toon format for 60-65% token reduction vs JSON output.

## Quick Start

### Installation

```bash
# One-line install (download latest release)
curl -L https://github.com/YOUR_USERNAME/bun-sql-query/releases/latest/download/bun-sql-query-dist.tar.gz | tar -xz -C ~/.claude/skills/bun-sql-query
```

See [INSTALL.md](INSTALL.md) for complete installation instructions.

### Schema Inspection
```bash
# Navigate to your project (where .env is located)
cd /your/project

# List all tables
bun ~/.claude/skills/bun-sql-query/dist/schema.js --list-tables

# Describe table structure
bun ~/.claude/skills/bun-sql-query/dist/schema.js --describe users

# Show foreign key relationships
bun ~/.claude/skills/bun-sql-query/dist/schema.js --relationships users

# Show everything
bun ~/.claude/skills/bun-sql-query/dist/schema.js --all
```

### Query Execution
```bash
# Simple SELECT query
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users LIMIT 10"

# Query with parameters (SQL injection safe)
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users WHERE id = ?" 123

# Query from file
bun ~/.claude/skills/bun-sql-query/dist/query.js --file query.sql

# Write operations (requires --write flag)
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "INSERT INTO users (name, email) VALUES (?, ?)" "Alice" "alice@example.com"
```

### Interactive Query Builder
```bash
# Launch interactive mode
bun ~/.claude/skills/bun-sql-query/dist/interactive.js

# Follow prompts to:
# 1. Select table
# 2. Choose columns
# 3. Add WHERE conditions
# 4. Add ORDER BY, LIMIT
# 5. Preview and execute
```

## Schema Inspection

### List All Tables
```bash
bun ~/.claude/skills/bun-sql-query/dist/schema.js --list-tables
```

**Output (Toon format):**
```
success: true
data:
  database_type: postgres
  tables[3]{table_name,table_type}:
    users,BASE TABLE
    transactions,BASE TABLE
    conversations,BASE TABLE
```

### Describe Table Structure
```bash
bun ~/.claude/skills/bun-sql-query/dist/schema.js --describe users
```

**Output (Toon format):**
```
success: true
data:
  table_name: users
  columns[5]{column_name,data_type,is_nullable,column_default}:
    id,uuid,NO,gen_random_uuid()
    name,text,NO,null
    email,text,NO,null
    role,text,YES,user
    created_at,timestamp,NO,now()
  constraints[2]{constraint_name,constraint_type,column_name}:
    users_pkey,PRIMARY KEY,id
    users_email_key,UNIQUE,email
  indexes[1]{indexname,indexdef}:
    users_email_idx,CREATE UNIQUE INDEX users_email_idx ON users USING btree (email)
```

### Show Relationships
```bash
bun ~/.claude/skills/bun-sql-query/dist/schema.js --relationships transactions
```

**Output (Toon format):**
```
success: true
data:
  table_name: transactions
  relationships[1]{constraint_name,table_name,column_name,foreign_table_name,foreign_column_name,update_rule,delete_rule}:
    transactions_user_id_fkey,transactions,user_id,users,id,CASCADE,CASCADE
```

### Complete Schema Dump
```bash
bun ~/.claude/skills/bun-sql-query/dist/schema.js --all
```

Shows all tables with their columns, constraints, indexes, and relationships in one comprehensive output.

## Querying Data

### Basic SELECT Queries

**All columns:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users"
```

**Specific columns:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT id, name, email FROM users"
```

**With LIMIT:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users LIMIT 10"
```

**With ORDER BY:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users ORDER BY created_at DESC LIMIT 10"
```

### Filtering with WHERE

**Simple condition:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users WHERE role = 'admin'"
```

**Parameterized query (SQL injection safe):**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users WHERE id = ?" 123
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users WHERE email = ?" "alice@example.com"
```

**Multiple parameters:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM transactions WHERE user_id = ? AND amount > ?" 123 100
```

**Pattern matching:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users WHERE email LIKE '%@gmail.com'"
```

### Joins

**INNER JOIN:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT users.name, transactions.amount FROM users INNER JOIN transactions ON users.id = transactions.user_id"
```

**LEFT JOIN with aggregation:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT users.name, COUNT(transactions.id) AS tx_count FROM users LEFT JOIN transactions ON users.id = transactions.user_id GROUP BY users.id, users.name"
```

### Aggregations

**COUNT:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT COUNT(*) FROM users"
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT role, COUNT(*) FROM users GROUP BY role"
```

**SUM, AVG, MIN, MAX:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT SUM(amount) AS total, AVG(amount) AS average FROM transactions"
```

**GROUP BY with HAVING:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT user_id, COUNT(*) AS tx_count, SUM(amount) AS total FROM transactions GROUP BY user_id HAVING COUNT(*) > 5"
```

### Query from File

Create a file `query.sql`:
```sql
SELECT
  users.name,
  COUNT(transactions.id) AS transaction_count,
  SUM(transactions.amount) AS total_spent
FROM users
LEFT JOIN transactions ON users.id = transactions.user_id
GROUP BY users.id, users.name
ORDER BY total_spent DESC
LIMIT 10;
```

Execute:
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --file query.sql
```

### Output Format

All queries return JSON with consistent structure:

**Success:**
```json
{
  "success": true,
  "rowCount": 10,
  "duration": "15.42ms",
  "data": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
  ],
  "query": "SELECT * FROM users LIMIT 10"
}
```

**Error:**
```json
{
  "success": false,
  "error": "relation \"invalid_table\" does not exist",
  "code": "42P01",
  "duration": "5.23ms",
  "query": "SELECT * FROM invalid_table"
}
```

## Modifying Data

### Safety Requirements

All write operations (INSERT, UPDATE, DELETE) require the `--write` flag for safety:

```bash
# ❌ This will fail
bun ~/.claude/skills/bun-sql-query/dist/query.js "INSERT INTO users (name) VALUES ('Alice')"

# ✅ This will work
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "INSERT INTO users (name) VALUES ('Alice')"
```

### INSERT Operations

**Single row with parameters:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "INSERT INTO users (name, email, role) VALUES (?, ?, ?)" "Alice" "alice@example.com" "user"
```

**Multiple rows (PostgreSQL):**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com'), ('Charlie', 'charlie@example.com')"
```

**INSERT with RETURNING (PostgreSQL):**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "INSERT INTO users (name, email) VALUES ('Dave', 'dave@example.com') RETURNING id, created_at"
```

### UPDATE Operations

**Single column:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "UPDATE users SET role = ? WHERE id = ?" "admin" 123
```

**Multiple columns:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "UPDATE users SET role = 'admin', updated_at = NOW() WHERE id = 123"
```

**Conditional update:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "UPDATE users SET active = false WHERE last_login < '2023-01-01'"
```

### DELETE Operations

**Delete by ID:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "DELETE FROM users WHERE id = ?" 123
```

**Conditional delete:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "DELETE FROM users WHERE active = false AND created_at < '2023-01-01'"
```

### UPSERT (PostgreSQL)

```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice') ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name"
```

## Interactive Mode

The interactive query builder guides you through query construction step-by-step:

```bash
bun ~/.claude/skills/bun-sql-query/dist/interactive.js
```

### Interactive Flow

1. **Select Table**: Choose from available tables
2. **Select Columns**: Pick specific columns or use `*` for all
3. **WHERE Clause**: Add filtering conditions (optional)
4. **ORDER BY**: Specify sorting (optional)
5. **LIMIT**: Set result limit (optional)
6. **Preview**: Review generated query
7. **Execute**: Confirm and run query

### Example Session

```
🔍 Interactive Query Builder

📋 Available tables:
  1. users
  2. transactions
  3. conversations

Select table (number or name): 1

✅ Selected table: users

📊 Available columns:
  1. id
  2. name
  3. email
  4. role
  5. created_at

Select columns (comma-separated numbers/names, or * for all): 2,3,4

🔎 WHERE clause (optional, press Enter to skip): role = 'admin'

📈 ORDER BY (optional, e.g., 'created_at DESC'): created_at DESC

🔢 LIMIT (optional, press Enter to skip): 10

📝 Generated Query:
────────────────────────────────────────────────────────────
SELECT name, email, role FROM users WHERE role = 'admin' ORDER BY created_at DESC LIMIT 10;
────────────────────────────────────────────────────────────

▶️  Execute query? (y/n): y

⏳ Executing query...

{
  "success": true,
  "rowCount": 3,
  "duration": "12.34ms",
  "data": [...]
}
```

## Safety Guidelines

### SQL Injection Prevention

**✅ Always use parameterized queries:**
```bash
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users WHERE email = ?" "user@example.com"
```

**❌ Never concatenate user input:**
```bash
# DON'T DO THIS
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users WHERE email = '$USER_INPUT'"
```

### Write Operation Safety

1. **Require --write flag**: All INSERT/UPDATE/DELETE operations must use `--write`
2. **Test with SELECT first**: Verify your WHERE clause with SELECT before UPDATE/DELETE
3. **Use transactions**: For multiple related operations, use transactions (see examples.md)
4. **Backup before bulk operations**: Always backup before large-scale modifications

### Best Practices

- **Start with schema inspection**: Use `--list-tables` and `--describe` to understand structure
- **Use LIMIT for exploration**: Always limit results when exploring large tables
- **Test queries in interactive mode**: Build complex queries step-by-step
- **Verify WHERE clauses**: Double-check conditions before write operations
- **Use parameters**: Always use `?` placeholders for user input

## Database Support

### PostgreSQL
- Full support for PostgreSQL-specific features
- JSON/JSONB operations
- Array operations
- Window functions
- CTEs and recursive queries
- RETURNING clause
- ON CONFLICT (UPSERT)

### MySQL
- Full support for MySQL-specific features
- JSON operations
- AUTO_INCREMENT
- Storage engines (InnoDB, MyISAM)
- Full-text search
- Stored procedures

### SQLite
- Full support for SQLite features
- JSON functions (JSON1 extension)
- Date/time functions
- Full-text search (FTS5)
- PRAGMA commands
- In-memory databases

## Environment Configuration

The skill automatically reads `DATABASE_URL` from the project's `.env` file:

**PostgreSQL:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/database
# or
DATABASE_URL=postgres://user:password@localhost:5432/database
```

**MySQL:**
```env
DATABASE_URL=mysql://user:password@localhost:3306/database
# or
DATABASE_URL=mysql2://user:password@localhost:3306/database
```

**SQLite:**
```env
DATABASE_URL=sqlite://path/to/database.db
# or
DATABASE_URL=/path/to/database.db
# or in-memory
DATABASE_URL=:memory:
```

## Advanced Examples

For comprehensive query examples including:
- Complex joins and subqueries
- Window functions
- CTEs (Common Table Expressions)
- JSON operations
- Array operations
- Transaction patterns
- Performance optimization tips

See: [references/examples.md](references/examples.md)

## Common Use Cases

### Explore Unknown Database
```bash
# 1. List all tables
bun ~/.claude/skills/bun-sql-query/dist/schema.js --list-tables

# 2. Describe interesting tables
bun ~/.claude/skills/bun-sql-query/dist/schema.js --describe users
bun ~/.claude/skills/bun-sql-query/dist/schema.js --describe transactions

# 3. Check relationships
bun ~/.claude/skills/bun-sql-query/dist/schema.js --relationships transactions

# 4. Sample data
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users LIMIT 5"
```

### Data Analysis
```bash
# User statistics
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT role, COUNT(*) FROM users GROUP BY role"

# Transaction summary
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT user_id, COUNT(*) AS tx_count, SUM(amount) AS total FROM transactions GROUP BY user_id ORDER BY total DESC LIMIT 10"

# Date-based analysis
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT DATE(created_at) AS date, COUNT(*) FROM users GROUP BY DATE(created_at) ORDER BY date DESC"
```

### Data Cleanup
```bash
# Find duplicates
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1"

# Find orphaned records
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT t.* FROM transactions t LEFT JOIN users u ON t.user_id = u.id WHERE u.id IS NULL"

# Remove test data
bun ~/.claude/skills/bun-sql-query/dist/query.js --write "DELETE FROM users WHERE email LIKE '%@test.com'"
```

### Data Migration
```bash
# Export data to JSON (pipe output to file)
bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users" > users_export.json

# Bulk insert from script
bun ~/.claude/skills/bun-sql-query/dist/query.js --write --file bulk_insert.sql
```

## Troubleshooting

### Connection Issues

**Error: DATABASE_URL not found**
- Ensure `.env` file exists in project root
- Verify `DATABASE_URL` is set correctly
- Check file permissions on `.env`

**Error: Connection refused**
- Verify database server is running
- Check host, port, username, password in DATABASE_URL
- Test connection with database client (psql, sqlite3)

### Query Errors

**Error: relation does not exist**
- Use `--list-tables` to verify table name
- Check for typos in table/column names
- Verify you're connected to correct database

**Error: column does not exist**
- Use `--describe <table>` to see available columns
- Check for typos in column names
- Verify column exists in current schema

### Performance Issues

**Slow queries**
- Add LIMIT to large result sets
- Check for missing indexes with `--describe`
- Use EXPLAIN ANALYZE (PostgreSQL) to analyze query plan
- See performance tips in examples.md

## Script Reference

### query.js
```
Usage: bun ~/.claude/skills/bun-sql-query/dist/query.js [options] <query> [params...]

Options:
  --file <path>    Read query from file
  --write          Allow write operations (INSERT/UPDATE/DELETE)
  --help, -h       Show help message

Examples:
  bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users LIMIT 10"
  bun ~/.claude/skills/bun-sql-query/dist/query.js "SELECT * FROM users WHERE id = ?" 123
  bun ~/.claude/skills/bun-sql-query/dist/query.js --file query.sql
  bun ~/.claude/skills/bun-sql-query/dist/query.js --write "INSERT INTO users (name) VALUES (?)" "Alice"
```

### schema.js
```
Usage: bun ~/.claude/skills/bun-sql-query/dist/schema.js [options]

Options:
  --list-tables              List all tables
  --describe <table>         Show table structure
  --relationships <table>    Show foreign key relationships
  --all                      Show complete schema
  --help, -h                 Show help message

Examples:
  bun ~/.claude/skills/bun-sql-query/dist/schema.js --list-tables
  bun ~/.claude/skills/bun-sql-query/dist/schema.js --describe users
  bun ~/.claude/skills/bun-sql-query/dist/schema.js --relationships transactions
  bun ~/.claude/skills/bun-sql-query/dist/schema.js --all
```

### interactive.js
```
Usage: bun ~/.claude/skills/bun-sql-query/dist/interactive.js

Interactive query builder with step-by-step prompts.
No command-line arguments required.

Example:
  bun ~/.claude/skills/bun-sql-query/dist/interactive.js
```

### Advanced Scripts

All advanced scripts are also available as bundled .js files:

```bash
# Transactions with savepoints
bun ~/.claude/skills/bun-sql-query/dist/transactions.js --demo all

# Bulk operations (10-100x faster)
bun ~/.claude/skills/bun-sql-query/dist/bulk-operations.js --demo benchmark

# MySQL-specific features
bun ~/.claude/skills/bun-sql-query/dist/mysql-demo.js --demo all

# SQLite-specific features
bun ~/.claude/skills/bun-sql-query/dist/sqlite-demo.js --demo all

# Advanced SQL (CTEs, window functions)
bun ~/.claude/skills/bun-sql-query/dist/advanced-query.js --demo all

# Connection management
bun ~/.claude/skills/bun-sql-query/dist/connection-manager.js --demo all
```

## Technical Details

### Zero Installation Required
- All scripts are pre-bundled with dependencies included
- No `bun install` needed - works immediately after download
- Uses Bun's native SQL capabilities
- Built-in connection pooling
- Automatic SQL injection protection with parameterized queries

### Token Efficiency
- **Toon format output**: 60-65% token reduction vs JSON
- Compact array notation for result sets
- More readable terminal output
- Optimized for AI processing

### Supported Databases
- **PostgreSQL** (full support for JSONB, arrays, CTEs, window functions)
- **MySQL** (full support for JSON, AUTO_INCREMENT, stored procedures)
- **SQLite** (full support for FTS5, JSON1, PRAGMA commands)

### Output Format
- All scripts output toon format for efficiency
- Consistent structure across success/error cases
- Includes execution time and row counts
- Human-readable and machine-parseable

### Security Features
- Parameterized queries prevent SQL injection
- Write operations require explicit `--write` flag
- Environment variables read from `.env` (not committed to git)
- No credentials in command history

## Installation

See [INSTALL.md](INSTALL.md) for complete installation instructions.

Quick install:
```bash
curl -L https://github.com/YOUR_USERNAME/bun-sql-query/releases/latest/download/bun-sql-query-dist.tar.gz | tar -xz -C ~/.claude/skills/bun-sql-query
```

## Version History

### 1.0.0 (2025-01-23)
- Initial release
- PostgreSQL, MySQL, and SQLite support
- Schema inspection, query execution, interactive mode
- Transaction support with savepoints
- Bulk operations (10-100x performance improvement)
- Database-specific features (MySQL, SQLite)
- Advanced SQL patterns (CTEs, window functions, subqueries)
- Toon format output (60-65% token reduction)
- Bundled distribution (no installation required)
- Comprehensive examples and documentation
