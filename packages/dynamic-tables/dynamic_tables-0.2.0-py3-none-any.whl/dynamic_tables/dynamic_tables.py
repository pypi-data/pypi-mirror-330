# this is dynamic_tables.py

import psycopg2, re, logging
from psycopg2 import sql

class DynamicTables:
    
    def __init__(self):
        """Initialize the class by calling self.initialize() to set up default values."""
        self.initialize()

    def initialize(self):
        """Sets up default attributes for the table structure."""
        self.column_list = []
        self.column_dynamic = ''
        self.table_prefix = 'dtbl_'
        self.table_name_dynamic = ''
        self.version = '0.1.2'
        """Initialize with default logging level (CRITICAL) and no file logging."""
        self.log_file_handler = None
        self.setup_logging(level=logging.CRITICAL, log_to_file=False)
  
    def setup_logging(self, level=logging.CRITICAL, log_to_file=False):
        """
        Configures logging level and optionally enables file logging.

        Args:
            level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
            log_to_file (bool): Enable or disable file logging.
        """
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()]  # Console only by default
        )

        # Enable file logging if requested
        if log_to_file and not self.log_file_handler:
            self.log_file_handler = logging.FileHandler("dynamic_tables.log")
            self.log_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            logging.getLogger().addHandler(self.log_file_handler)

        # Disable file logging if requested
        elif not log_to_file and self.log_file_handler:
            logging.getLogger().removeHandler(self.log_file_handler)
            self.log_file_handler.close()
            self.log_file_handler = None

        logging.info(f"Logging level set to {logging.getLevelName(level)}")
        if log_to_file:
            logging.info("File logging enabled (dynamic_tables.log)")

    def change_log_level(self, level_name):
        """
        Change the logging level at runtime.
        Args:
            level_name (str): "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        """
        level = getattr(logging, level_name.upper(), logging.CRITICAL)
        logging.getLogger().setLevel(level)
        logging.info(f"Log level changed to {level_name.upper()}")
        
    def set_columns(self, input_columns):
        """Sets the columns for table creation based on user input."""
        self.column_list = []
        for column in input_columns.split(','):
            column = column.strip()
            parts = column.split(maxsplit=1)
            if len(parts) == 2:
                self.column_list.append((parts[0], parts[1]))
            else:
                logging.warning(f"Invalid column format: '{column}'")

    def set_table_prefix(self, input_prefix):
        """Defines a custom table name prefix."""
        self.table_prefix = input_prefix

    def set_dynamic_column(self, input_column):
        """Sets the column that determines dynamic table names."""
        self.column_dynamic = input_column       
        
    def connection_open(self, dbname, user, password, host):
        """Opens a connection to the PostgreSQL database and initializes the cursor."""
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cur = self.conn.cursor()

    def connectHC(self, database, user, password, host):
        """Helper function to open a connection using hardcoded credentials."""
        self.connection_open(database, user, password, host)

    def connectJSON(self, config_path="config.json"):
        """Opens a database connection using credentials from a JSON config file."""
        import json
        with open(config_path) as config_file:
            config = json.load(config_file)
        database=config["database"]
        user=config["user"]
        password=config["password"]
        host=config["host"]
        self.connection_open(database, user, password, host)

    def connectENVS(self):
        """Opens a database connection using environment variables."""
        import os
        database=os.getenv("DTABLES_ENVS_PGSQL_DATABASE")
        user=os.getenv("DTABLES_ENVS_PGSQL_USER")
        password=os.getenv("DTABLES_ENVS_PGSQL_PASSWORD")
        host=os.getenv("DTABLES_ENVS_PGSQL_HOST")
        self.connection_open(database, user, password, host)

    def connection_close(self):
        """Closes the database cursor and connection."""
        self.cur.close()
        self.conn.close()

    def close(self):
        """Alias for connection_close() to improve readability."""
        self.connection_close()

    def get_tables(self):
        """Returns a list of all table names in the public schema."""
        try:
            self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = self.cur.fetchall()

            if tables:
                table_list = [table[0] for table in tables]  # Convert to a simple list of table names
                logging.info(f"Found {len(table_list)} tables.")
                logging.debug(f"Tables: {table_list}")
                return table_list
            else:
                logging.info("No tables found.")
                return []  # Empty list instead of None for consistency

        except Exception as e:
            logging.error(f"Error retrieving tables: {e}", exc_info=True)
            return None

    def get_columns(self, table_name):
        """Returns a list of all columns and their data types for a given table."""
        try:
            query = sql.SQL("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position;
            """)
            self.cur.execute(query, (table_name,))
            columns = self.cur.fetchall()

            if columns:
                logging.info(f"Retrieved {len(columns)} columns from '{table_name}'.")
                return columns
            else:
                logging.warning(f"No columns found for table '{table_name}' or the table does not exist.")
                return []

        except Exception as e:
            logging.error(f"Error retrieving columns for '{table_name}': {e}", exc_info=True)
            return None

    def get_table_rows(self, table_name):
        """Retrieves all rows from the specified table and returns them."""
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
            self.cur.execute(query)
            rows = self.cur.fetchall()

            if rows:
                logging.info(f"Retrieved {len(rows)} rows from '{table_name}'.")
                logging.debug(f"Rows from '{table_name}': {rows}")
                return rows  # Returns data for other functions
            else:
                logging.info(f"Table '{table_name}' exists but has no data.")
                return []

        except Exception as e:
            logging.error(f"Error retrieving rows from '{table_name}': {e}", exc_info=True)
            return None

    def show_db(self):
        """Displays the name of the current database."""
        self.cur.execute("SELECT current_database();")
        db_name = self.cur.fetchone()[0]
        logging.info(f"Connected to database: {db_name}")

    def show_tables(self):
        """Prints a list of all table names (uses get_tables)."""
        tables = self.get_tables()
        
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(f" - {table}")
        else:
            print("No tables found or an error occurred.")

    def show_columns(self, table_name):
        """Prints column details for human readability (uses get_columns)."""
        columns = self.get_columns(table_name)
        
        if columns:
            print(f"Columns in '{table_name}':")
            for name, dtype in columns:
                print(f" - {name}: {dtype}")
        else:
            print(f"No columns found for '{table_name}' or the table does not exist.")

    def show_columns_all(self):
        """Lists column details for all tables."""
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        for table in self.cur.fetchall():
            self.show_columns(table[0])

    def show_table(self, table_name):
        """Displays all rows from the specified table (uses get_table_rows)."""
        rows = self.get_table_rows(table_name)
        
        if rows:
            print(f"Rows in '{table_name}':")
            for row in rows:
                print(f" - {row}")
        else:
            print(f"Table '{table_name}' exists but has no data or an error occurred.")

    def show_version(self):
        """Show the current software version"""
        print(self.version)

    def select_table(self, table_name):
        """Retrieves and prints all rows from the specified table."""
        self.show_table(table_name)
        
    def insert_data(self, table_name, data_dict):
        """Inserts data into a dynamically created table."""
        columns = data_dict.keys()
        values = list(data_dict.values())

        query = sql.SQL("""
            INSERT INTO {} ({})
            VALUES ({});
        """).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() for _ in columns)
        )

        self.cur.execute(query, values)
        self.conn.commit()

    def create_table(self, table_name, columns):
        """Creates a table dynamically if it does not already exist."""
        column_definitions = sql.SQL(", ").join(
            sql.SQL("{} {}").format(sql.Identifier(col_name), sql.SQL(col_type))
            for col_name, col_type in columns
        )

        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                {}
            );
        """).format(sql.Identifier(table_name), column_definitions)

        self.cur.execute(query)
        self.conn.commit()

    def delete_tables(self):
        """Deletes all tables that match the current table prefix."""
        try:
            query = """
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name LIKE %s;
            """
            prefix_pattern = self.table_prefix + "%"  # Dynamic prefix
            logging.debug(f"Prefix pattern: {prefix_pattern}")

            self.cur.execute(query, (prefix_pattern,))
            tables = self.cur.fetchall()

            if tables:
                logging.info(f"Found {len(tables)} tables to delete.")
                logging.debug(f"Tables to delete: {tables}")

                for table in tables:
                    table_name = table[0]
                    logging.info(f"Dropping table: {table_name}")

                    drop_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(sql.Identifier(table_name))
                    self.cur.execute(drop_query)

                self.conn.commit()
                logging.info("Successfully deleted matching tables.")
            else:
                logging.info("No tables found matching the prefix.")

        except Exception as e:
            logging.error(f"Error deleting tables: {e}", exc_info=True)

    def status(self):
        """Logs the currently configured column settings."""
        if self.column_list:
            logging.info("Configured Columns:")
            for column in self.column_list:
                logging.info(f" - {column}")
        else:
            logging.info("No columns configured.")

        logging.info(f"Dynamic Column: {self.column_dynamic if self.column_dynamic else 'None'}")

    def format_table_name(self, input_column):
        """Formats an input column name to create a valid table name."""
        cleaned = re.sub(r'[^a-zA-Z0-9_]', '', input_column)
        return self.table_prefix + cleaned

    def input(self, *args):
        """Handles data insertion by dynamically determining the table name and inserting values."""
        column_dict = {}
        self.table_name_dynamic = ''

        for column_number, (column_name, _) in enumerate(self.column_list):
            if column_name == self.column_dynamic:
                self.table_name_dynamic = self.format_table_name(args[column_number])
                column_dict[column_name] = args[column_number]
            else:
                column_dict[column_name] = args[column_number]

        if self.table_name_dynamic:
            self.create_table(self.table_name_dynamic, self.column_list)

        self.insert_data(self.table_name_dynamic, column_dict)
