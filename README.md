# Dynamic Chatbot with Database Integration

This chatbot is designed to provide dynamic responses based on the data stored in various types of databases such as
MySQL, PostgreSQL, Oracle, SQLite, and MongoDB. By leveraging the capabilities of natural language processing (NLP) and
integrating with the databases, the chatbot can fetch real-time data and answer user queries accordingly.

## Features

- **Dynamic Database Connection:** Connects to various SQL and NoSQL databases based on configuration.
- **Natural Language Processing:** Understands user queries and fetches the relevant data from the database.
- **Mock Data Integration:** Can operate with mock data for testing and demonstration purposes.
- **Scalability:** Designed with best practices to ensure scalability and maintainability.

## Prerequisites

- Python 3.x
- Required Python libraries listed in `requirements.txt`.

## Installation

1. Clone the repository:

```
git clone https://github.com/shamspias/db-gpt-chatbot
```

2. Navigate to the project directory:

```
cd db-gpt-chatbot

```

3. Install the required Python libraries:

```
pip install -r requirements.txt
```

4. Set up your `.env` file with the appropriate database configurations. An example `.env` file (`example.env`) is
   provided for reference.

5. Run the application:

```
python main.py
```

## Usage

1. Start the chatbot.
2. Ask queries related to the data present in your database.
3. Receive dynamic responses based on real-time database data.

## Future Scope

- **Integration with more NLP tools:** To enhance the understanding of complex user queries.
- **Support for more databases:** Extend support to other popular databases.
- **Enhanced Security:** Implement more security features to ensure safe database transactions.
- **Optimization:** Further optimize the database querying mechanism for faster responses.

## Contribution

Contributions are welcome! Please ensure that you test the changes locally before creating a pull request.

## License

This project is licensed under the MIT License.

