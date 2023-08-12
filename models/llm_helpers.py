import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser


class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")


def convert_to_string(data_dict):
    return json.dumps(data_dict)


class LanguageModelRequest:
    """ 
    A class to handle requests to a language model (e.g., GPT-3).
    
    This class provides methods to send questions to a language model and retrieve responses.
    """

    def __init__(self):
        # Assuming you've set OPENAI_API_KEY in your .env file
        # This line should be uncommented and set up in a real-world scenario
        openai_api_key = os.getenv('OPENAI_API_KEY')
        self.chat_model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
        self.system_prompt = os.getenv('SYSTEM_PROMPT', "You are an AI who give information from given data")

    def ask_llm(self, question, data_dict):
        """ 
        Send a question with data to llm and get the response.

        """
        data = convert_to_string(data_dict)

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

    # todo make a llm call to get the table names and fields names
