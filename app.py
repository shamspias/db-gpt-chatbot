from flask import Flask, request, jsonify
from models.database import DynamicDatabase
from models.nlp_processor import NLPQueryProcessor
from models.llm_helpers import LanguageModelRequest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
db = DynamicDatabase()
language_model_processor = LanguageModelRequest()
nlp_processor = NLPQueryProcessor(db, language_model_processor)


@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    use_mock_data = request.json.get("use_mock_data", False)

    db.set_mock_data(use_mock_data)

    # Process the question using NLPQueryProcessor to detect table and field
    table_name, field, target_query = nlp_processor.understand_query(question)

    # If a table is detected in the question
    if table_name:
        data = db.query(table_name, field, target_query)
        response = language_model_processor.ask_llm(question, data)
        return jsonify({"response": response})

    # Otherwise, return a generic response
    return jsonify({"response": f"Processed question: {question}"})


if __name__ == "__main__":
    app.run(debug=True)
