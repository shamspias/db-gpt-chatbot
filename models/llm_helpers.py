import os
import json

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.vectorstores import FAISS

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from langchain.docstore.document import Document


class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")


def convert_to_documents(data_list):
    data = []
    for data_dict in data_list:
        list_value = list(data_dict.keys())[0]
        # metadata = {"source": data_dict[list_value]}
        metadata = data_dict
        data.append(Document(page_content=data_dict[list_value], metadata=metadata))
    return data


class LanguageModelRequest:
    """ 
    A class to handle requests to a language model (e.g., GPT-3).
    
    This class provides methods to send questions to a language model and retrieve responses.
    """

    def __init__(self):
        # Assuming you've set OPENAI_API_KEY in your .env file
        # This line should be uncommented and set up in a real-world scenario
        openai_api_key = os.getenv('OPENAI_API_KEY')
        self.chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0)
        self.system_prompt = os.getenv('SYSTEM_PROMPT', "You are an AI who give information from given data")
        self.system_prompt_query = os.getenv('SYSTEM_PROMPT_QUERY', "You are an AI who create sql query based on the "
                                                                    "user question and database tables and fields")
        self.compressor = LLMChainExtractor.from_llm(llm=self.chat_model)
        self.embeddings = OpenAIEmbeddings()

    def ask_llm(self, question, data_list):
        """ 
        Send a question with data to llm and get the response.

        """
        docs = convert_to_documents(data_list)
        # retriever = FAISS.from_documents(docs, self.embeddings).as_retriever()

        # compression_retriever = ContextualCompressionRetriever(base_compressor=self.compressor,
        #                                                        base_retriever=retriever)
        #
        # data = compression_retriever.get_relevant_documents(question)
        # data = retriever.get_relevant_documents(question)
        data = docs
        print(data)
        template = self.system_prompt + "\ndata: {data} "
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{questions}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chat_prompt.format_messages(data=data, questions=question)

        chain = LLMChain(
            llm=self.chat_model,
            prompt=chat_prompt,
            output_parser=CommaSeparatedListOutputParser()
        )

        response = chain.run(data=data, questions=question)
        return response

    def generate_query_by_llm(self, tables, columns, query):
        template = self.system_prompt_query + (
            "\ntables: {tables} column: {columns}\n\nonly write  query no other extra text and don't forget to use "
            "SELECT *")
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{questions}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chat_prompt.format_messages(tables=tables, columns=columns, questions=query)

        chain = LLMChain(
            llm=self.chat_model,
            prompt=chat_prompt,
            output_parser=CommaSeparatedListOutputParser()
        )

        response = chain.run(tables=tables, columns=columns, questions=query)
        return response[0]

    def get_table_based_on_query(self, tables, query):
        template = ("Get the table names for sql query based on given table and question only write table names so it "
                    "can use for query database,\ntables: {tables}\n\nOnly response table name")
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{questions}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chat_prompt.format_messages(tables=tables, questions=query)

        chain = LLMChain(
            llm=self.chat_model,
            prompt=chat_prompt,
            output_parser=CommaSeparatedListOutputParser()
        )

        response = chain.run(tables=tables, questions=query)
        return response[0]

    def get_column_based_on_query(self, columns, query):
        template = ("Get the column names for sql query based on given columns and question only write column names "
                    "so it can use for query database\ncolumns: {columns}")
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{questions}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chat_prompt.format_messages(columns=columns, questions=query)

        chain = LLMChain(
            llm=self.chat_model,
            prompt=chat_prompt,
            output_parser=CommaSeparatedListOutputParser()
        )

        response = chain.run(columns=columns, questions=query)
        return response[0]
