
class NLPQueryProcessor:
    def __init__(self, database):
        self.database = database

    def understand_query(self, query):
        tables = self.database.get_tables()
        target_table = None
        target_field = None
        for table in tables:
            if table in query:
                target_table = table
                fields = self.database.get_fields(table)
                for field in fields:
                    if field in query:
                        target_field = field
                        break
                break
        return target_table, target_field
