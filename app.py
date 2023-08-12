
from flask import Flask, request, jsonify
from models.database import DynamicDatabase
from models.lang_chain_simulator import LangChainSimulator
from python_dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
db = DynamicDatabase()
lang_chain = LangChainSimulator()

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    table_name = request.json.get("table")
    field = request.json.get("field")
    
    # If the question is about database data
    if table_name:
        data = db.query(table_name, field)
        return jsonify({"response": data})

    # Otherwise, process with LangChainSimulator (or actual LangChain if integrated)
    response = lang_chain.process(question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
