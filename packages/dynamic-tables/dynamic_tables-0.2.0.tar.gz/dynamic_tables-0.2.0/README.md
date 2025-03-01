# Dynamic Tables (Python)

A Python library for dynamically creating and managing PostgreSQL tables based on input data.

---

## 🚀 Features
- Automatically creates tables based on incoming data.
- Supports dynamic naming conventions.
- Provides easy database connectivity with PostgreSQL.
- Includes helper functions for querying and deleting tables.

---

## 📥 Installation

### 1️⃣ Install via GitHub (Recommended for Development)
Clone the repository and install in editable mode:

```bash
git clone https://github.com/scottrodeo/dynamic-tables-python.git
cd dynamic-tables-python
pip install -e .
```

### 2️⃣ Install Directly via `pip`
The package is available on PyPI, install it with:

```bash
pip install dynamic-tables
```

---

## 🏃‍♂️ Running the Example

### 1️⃣ Quick Run (Without Installation)
Run the example script directly:

```bash
python3 examples/example.py
```

💡 *This works because the script dynamically adjusts `sys.path`.*


---

## 📌 Example Usage

Once installed, you can use `dynamic_tables` in your Python scripts:

```python
from dynamic_tables import DynamicTables

# Initialize the dynamic table manager
tables = DynamicTables()

# Configure dynamic table properties
tables.set_table_prefix("dtbl_")
tables.set_columns("domain TEXT, category TEXT, lang TEXT")
tables.set_dynamic_column("domain")

# Insert dynamic data
tables.input("wikipedia.org", "cats", "en")
tables.input("wikipedia.org", "dogs", "en")

# Show all tables
tables.show_tables()
```

---

## 🛠️ Available Functions

| Function | Description |
|----------|-------------|
| `set_columns("name TYPE, age TYPE")` | Define table schema |
| `set_table_prefix("prefix_")` | Set a custom table prefix |
| `set_dynamic_column("column_name")` | Set the column that determines dynamic table names |
| `input(value1, value2, ...)` | Insert a new row dynamically |
| `show_tables()` | List all dynamically created tables |
| `show_columns("table_name")` | Show column details for a specific table |
| `show_columns_all()` | Show column details for all tables |
| `select_table("table_name")` | Retrieve all rows from a table |
| `delete_tables()` | Drop all tables matching the prefix |
| `create_table("table_name", [("column1", "TYPE"), ("column2", "TYPE")])` | Create a table dynamically |
| `insert_data("table_name", {"column1": value1, "column2": value2})` | Insert data into a specific table |
| `get_tables()` | Retrieve a list of all tables in the database |
| `get_columns("table_name")` | Retrieve all columns for a given table |
| `get_table_rows("table_name")` | Retrieve all rows from a table |
| `connectHC("dbname", "user", "password", "host")` | Connect using hardcoded credentials |
| `connectJSON("config.json")` | Connect using credentials from a JSON config file |
| `connectENVS()` | Connect using environment variables |
| `connection_open("dbname", "user", "password", "host")` | Open a PostgreSQL database connection |
| `connection_close()` | Close the database connection |
| `status()` | Show the current configuration status |
| `show_db()` | Display the connected database name |
| `setup_logging(level, log_to_file)` | Configure logging settings |
| `change_log_level("LEVEL")` | Change the logging level at runtime |
| `show_version()` | Display the current version of the library |

---

## ⚡ Development

### Running Tests
Run the test suite:

```bash
pytest tests/
```

### Linting
Ensure your code follows best practices:

```bash
flake8 dynamic_tables/
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🌎 Links

- **GitHub Repository:** [Dynamic Tables (Python)](https://github.com/scottrodeo/dynamic-tables-python)
- **Issue Tracker:** [Report Issues](https://github.com/scottrodeo/dynamic-tables-python/issues)

---

### 🚀 Happy Coding!

