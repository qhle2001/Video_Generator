# pip install langchain_experimental

import re
import os
import pandas as pd
import openai
from openai import OpenAI
# import sys 
# sys.path.insert(0, '../')

from apikey import get_api_key
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

from langchain_experimental.agents import create_pandas_dataframe_agent


class ReadCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.read_data()
    
    def read_data(self):
        try:
            df = pd.read_csv(self.file_path)
            return df
        except Exception as e:
            print(f"Error reading data: {e}")
            return None

class GenDesciption:
    def __init__(self, df):
        
        api_key = get_api_key()

        if not api_key:
            raise ValueError("API key is not available. Check the implementation of get_api_key.")

        os.environ["OPENAI_API_KEY"] = api_key
        openai.api_key = os.environ["OPENAI_API_KEY"]
        
        self.df = df
        self.agent = self.create_agent()
        self.description = self.generate_description()
        print(self.description)
        
    def create_agent(self):
        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0.1, model="gpt-4-1106-preview"),
            self.df,
            verbose=False,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        return agent 
    
    def generate_description(self):
        requirement = f"""Help me describe entire about the dataset I gave you as detailed as possible! 
            You must describe follow my suggestion below:
            The first one, you must describe the dataset describe what.
            Then, you must describe all of columns in the dataset. In this step, you should include data of the dataset if is possible."""
        return self.agent.run(requirement)
    
def main():
    file_path = "./Current_Employee_Names__Salaries__and_Position_Titles_-_Full-time.csv"
    data_reader = ReadCSV(file_path)
    GenDesciption(data_reader.df)
    
if __name__ == '__main__':
    main()
    