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

class Visualize:
    def __init__(self, df, user_input):
        
        api_key = get_api_key()

        if not api_key:
            raise ValueError("API key is not available. Check the implementation of get_api_key.")

        os.environ["OPENAI_API_KEY"] = api_key
        openai.api_key = os.environ["OPENAI_API_KEY"]
        
        self.df = df
        self.agent = self.create_agent(df)
        self.description = self.generate_description()
        self.ins = self.generate_ins(self.description, user_input)
        self.code_viz = self.generate_code(self.ins)
        self.visualize(self.code_viz)
        
    
    def create_agent(self,df):
        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0.1, model="gpt-4-1106-preview"),
            df,
            verbose=False,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        return agent 
    
    def generate_description(self):
        requirement = f"Help me describe entire about the dataset I gave you!"
        return self.agent.run(requirement)
    
    def generate_ins(self, description, user_input):
        requirement = f'''This is the dataset's description: {description}. This is human requirement: {user_input}.
        You must based on the dataset, the dataset's description and human request to give me a instruction used for generate a code to visualize the dataset.
        Note that you give me only the instruction used for generate but not include a code.
        Additionally, the instruction can be used in any programming language, and you must give me a sentence, not the steps'''

        return self.agent.run(requirement)
    
    def generate_code(self, instruction):
        requirement = f"""<s>
        I need you visualize chart using python that you receive handled dataframe and the chart should follow this instruction : {instruction}
        Show me all columns then using them to show on visualization
        The content chart describes:
        If cannot use chart to visualize all columns, you could be use another type chart
        def plot_chart(input_df):
        return fig
        Note that, I will call the function to show the chart, so you must not generate any show function and call the plot_chart function.
        Additionally, if there is no request to visualize top in the instruction, you must use top 5 to visualize. Ignore if there is request to visualize top in the instruction.
        """

        return self.agent.run(requirement)

    def visualize(self, code_viz):

        match = re.search(r"```python(.*?)```", code_viz, re.DOTALL)

        if match:
            extracted_code = match.group(1)
            print(extracted_code)

            try:
                exec(extracted_code, globals())
                
                if 'plot_chart' in globals():
                    chart_fig = plot_chart(self.df)
                    chart_fig.show()
                    chart_fig.savefig('output_chart.png', bbox_inches='tight')
                else:
                    print("Function 'plot_chart' not defined.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Python code not found.")