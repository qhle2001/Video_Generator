import openai
from openai import OpenAI
from apikey import get_api_key
from script import get_script
import urllib.request
from moviepy.editor import *
def create_image_audio(prompts, voice):
  i = 1
  client = OpenAI()
  for index in range(len(prompts)):
    response = client.images.generate(
        model = "dall-e-3",
        prompt = prompts[index].strip(),
        size = "1792x1024",
        quality = "standard",
        n = 1
    )

    print("Generate New AI Image From Script...")
    image_url = response.data[0].url
    urllib.request.urlretrieve(image_url, f"images/image{index+1}.jpg")

    print("The Generated Image Saved in Images Folder!")

    response = client.audio.speech.create(
        model = "tts-1",
        voice = "nova",
        input = voice[index].strip()
    )

    print("Generate New AI Audio From Script... ")
    response.stream_to_file(f"audio/voiceover{index+1}.mp3")
    print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")
    i+=1

def main():
    os.environ["OPENAI_API_KEY"] = get_api_key()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    prompts, voice = get_script()

    create_image_audio(prompts, voice)

if __name__ == "__main__":
    main()
