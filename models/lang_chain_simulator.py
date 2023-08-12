class LangChainSimulator:
    def __init__(self):
        self.known_tables = ["users", "orders"]
        self.known_fields = {
            "users": ["id", "name", "age"],
            "orders": ["id", "user_id", "product", "quantity"]
        }

    def process(self, question):
        # This is a very basic simulation. In a real-world scenario, this method would process the question 
        # using LangChain or a similar NLP service to determine the table and field.
        # Here we'll use simple keyword matching for demonstration.

        detected_table = None
        detected_field = None

        for table in self.known_tables:
            if table in question:
                detected_table = table
                for field in self.known_fields[table]:
                    if field in question:
                        detected_field = field
                        break
                break

        return detected_table, detected_field
