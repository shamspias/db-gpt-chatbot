class NLPQueryProcessor:
    def __init__(self, database, language_model_processor):
        self.database = database
        self.llm = language_model_processor

    # todo add the llm way to detected tables and fileds
    def understand_query(self, query):
        tables = self.database.get_tables()
        target_table = self.llm.get_table_based_on_query(tables, query)
        target_field = None
        fields = self.database.get_fields(target_table)
        # target_field = self.llm.get_column_based_on_query(fields, query)
        target_query = self.llm.generate_query_by_llm(tables, fields, query)
        return target_table, target_field, target_query

        ## OLD Way
        # for table in tables:
        #     if table in query:
        #         target_table = table
        #         fields = self.database.get_fields(table)
        #         for field in fields:
        #             if field in query:
        #                 target_field = field
        #                 break
        #         break
        # return target_table, target_field
