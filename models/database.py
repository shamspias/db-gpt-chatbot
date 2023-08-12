import os


class DynamicDatabase:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.engine = None
        self.connection = None
        self.db_type = os.environ.get("DATABASE_TYPE").lower()
        self.use_mock_data = os.environ.get("USE_MOCK_DATA", "True").lower() == "true"

    def connect(self):
        """Establish a connection to the specified database using environment variables."""
        try:
            if self.connection:
                return  # Already connected
            if self.db_type in ["mysql", "postgresql", "oracle", "sqlite"]:
                connection_string = self._get_sql_connection_string()
                self._import_sqlalchemy()
                self.engine = sqlalchemy.create_engine(connection_string)
                self.connection = self.engine.connect()
            elif self.db_type == "mongodb":
                self.connection = self._get_mongodb_connection()
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            raise ValueError(f"Error connecting to the database: {str(e)}")

    def _get_sql_connection_string(self):
        """Generate an SQL connection string based on the database type and environment variables."""
        user = os.environ.get(f"{self.db_type.upper()}_USER", "")
        password = os.environ.get(f"{self.db_type.upper()}_PASSWORD", "")
        host = os.environ.get(f"{self.db_type.upper()}_HOST", "")
        port = os.environ.get(f"{self.db_type.upper()}_PORT", "")
        dbname = os.environ.get(f"{self.db_type.upper()}_DBNAME", "")

        if self.db_type == "mysql":
            self._import_pymysql()
            return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
        elif self.db_type == "postgresql":
            self._import_psycopg2()
            return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        elif self.db_type == "oracle":
            self._import_cx_oracle()
            return f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{dbname}"
        elif self.db_type == "sqlite":
            return f"sqlite:///{dbname}"

    def _get_mongodb_connection(self):
        """Establish a connection to MongoDB using environment variables."""
        self._import_pymongo()
        user = os.environ.get("MONGODB_USER")
        password = os.environ.get("MONGODB_PASSWORD")
        host = os.environ.get("MONGODB_HOST")
        port = os.environ.get("MONGODB_PORT")
        dbname = os.environ.get("MONGODB_DBNAME")

        connection_string = f"mongodb+srv://{user}:{password}@{host}:{port}/{dbname}"
        client = MongoClient(connection_string)
        return client[dbname]

    # Conditional imports for necessary libraries
    def _import_sqlalchemy(self):
        global sqlalchemy
        import sqlalchemy

    def _import_pymysql(self):
        import pymysql

    def _import_psycopg2(self):
        import psycopg2

    def _import_cx_oracle(self):
        import cx_oracle

    def _import_pymongo(self):
        global MongoClient
        from pymongo import MongoClient

    # Methods related to mock database data for chatbot demo
    @property
    def data(self):
        return {
            "users": [
                {"id": 1, "name": "Alice", "age": 25},
                {"id": 2, "name": "Bob", "age": 30},
                {"id": 3, "name": "Charlie", "age": 35},
            ],
            "orders": [
                {"id": 1, "user_id": 1, "product": "Laptop", "quantity": 1},
                {"id": 2, "user_id": 2, "product": "Phone", "quantity": 2},
                {"id": 3, "user_id": 3, "product": "Tablet", "quantity": 3},
            ]
        }

    def get_tables(self):
        return list(self.data.keys())

    def get_fields(self, table_name):
        if table_name in self.data:
            return list(self.data[table_name][0].keys())
        return []

    def query(self, table_name, field=None):
        if self.use_mock_data:
            return self._query_mock_data(table_name, field)
        return self._query_real_data(table_name, field)

    def _query_mock_data(self, table_name, field=None):
        if table_name in self.data:
            if field:
                return [entry[field] for entry in self.data[table_name]]
            return self.data[table_name]
        return []

    def _query_real_data(self, table_name, field=None):
        if not self.connection:
            self.connect()
        if self.db_type in ["mysql", "postgresql", "oracle", "sqlite"]:
            return self._query_sql_data(table_name, field)
        elif self.db_type == "mongodb":
            return self._query_mongodb_data(table_name, field)
        return []

    def _query_sql_data(self, table_name, field=None):
        query = f"SELECT * FROM {table_name}"
        result = self.connection.execute(query).fetchall()
        if field:
            return [entry[field] for entry in result]
        return [dict(row) for row in result]

    def _query_mongodb_data(self, table_name, field=None):
        collection = self.connection[table_name]
        result = list(collection.find())
        if field:
            return [entry[field] for entry in result]
        return result
