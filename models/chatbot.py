class EnhancedChatbot:
    def __init__(self, database, nlp_processor):
        self.database = database
        self.nlp_processor = nlp_processor
        self.previous_query = None
        self.previous_response = None

    def respond(self, user_input):
        target_table, target_field = self.nlp_processor.understand_query(user_input)
        if not target_table:
            response = "I'm not sure how to help with that."
        else:
            data = self.database.query(target_table, target_field)
            if target_field:
                response = f"The {target_field} in {target_table} are: {', '.join(map(str, data))}"
            else:
                response = f"Data from {target_table}: {data}"
        self.previous_query = user_input
        self.previous_response = response
        return response

    def feedback(self, feedback):
        return "Thank you for your feedback!"

    def follow_up(self, follow_up_query):
        if "previous" in follow_up_query or "last" in follow_up_query:
            return self.previous_response
        else:
            return self.respond(follow_up_query)
