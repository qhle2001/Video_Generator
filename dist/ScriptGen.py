import os

import openai
from openai import OpenAI
from apikey import get_api_key
from moviepy.editor import *
from script import get_script
import sys

# Get the text from the command line arguments
text = sys.argv[1]

# os.makedirs("audio")
# os.makedirs("images")
# os.makedirs("videos")
# os.makedirs("results")introduce

os.environ["OPENAI_API_KEY"] = get_api_key()
openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()
# text = input("What topic you want to write about: ")

introduction = ". Write a script about content that I provided you in front follow this: [Imgage generation prompt: Prompt]\n\nVoiceover: Content\n\n. Note that: You must generate the content don't have any other content beyond what I provided, you must generate a script according to the order that I provided you, and for each Voiceover, there must be an Image generation prompt in front, and there must be no more than 7 Image generation prompt."

prompt = text + introduction

print("The AI BOT is trying now to generate a new text for you...")
response = client.completions.create(
    model = "gpt-3.5-turbo-instruct",
    prompt = prompt,
    max_tokens=2048,
    n=1,
    stop=None,
    temperature=0.5
)

#Print the generated text
generated_text = response.choices[0].text

print(generated_text)

#Save the text in a file
if not os.path.exists("./results"):
    os.makedirs("./results")
with open("./results/generated_text.txt", "w", encoding='utf-8') as file:
  file.write(generated_text.strip())

print("The Generation File Saved Successful!")