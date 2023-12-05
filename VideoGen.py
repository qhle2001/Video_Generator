import openai
from openai import OpenAI
from apikey import get_api_key
from script import get_script
import urllib.request
from moviepy.editor import *

def gen_audio(voice):
    merged_voice = ' '.join(voice)

    print("The AI BOT is trying now to generate an audio for you...")
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=merged_voice
    )
    response.stream_to_file("results/audio_file.mp3")

    print("The Generated Audio File Saved Successful!")


def create_short_video():
    for index in range(1, len(os.listdir("audio")) + 1):
        # Load the audio file using moviepy
        print("Extract voiceover and get duration...")
        audio_clip = AudioFileClip(f"audio/voiceover{index}.mp3")
        audio_duration = audio_clip.duration

        # Load the image file using moviepy
        print("Extract Image Clip and Set Duration...")
        image_clip = ImageClip(f"images/image{index}.jpg").set_duration(audio_duration)

        # Use moviepy to create a final video by concatenating
        # The audio, image, and text clips
        print("Concatenate Audio, Image, Text to create Final Clip...")
        clip = image_clip.set_audio(audio_clip)
        video = CompositeVideoClip([clip])

        # Save the final video to a file
        video = video.write_videofile(f"videos/video{index}.mp4", fps=24)
        print(f"The Video{index} Has Been Created Successfully!")


def create_final_video():
    #Create a final video
    clips = []
    for index in range(1,len(os.listdir("videos")) + 1):
        clip = VideoFileClip(f"videos/video{index}.mp4")
        clips.append(clip)

    print("Concatenate All The Clips to Create a Final Video...")
    final_video = concatenate_videoclips(clips, method = "compose")
    final_video = final_video.write_videofile("results/final_video.mp4")

def replace_the_audio():

    print("The Audio is Replacing...")
    input_video_path = 'results/final_video.mp4'
    input_audio_path = 'results/audio_file.mp3'
    output_video_path = 'results/new_video.mp4'

    #Load the input video
    video_clip = VideoFileClip(input_video_path)

    #Load the input audio
    new_audio_clip = AudioFileClip(input_audio_path)

    #Set the audio of the video clip to the new audio
    video_clip = video_clip.set_audio(new_audio_clip)

    #Write the video with the new audio to a new file
    video_clip.write_videofile(output_video_path, codec = 'libx264', audio_codec='aac')

def main():
    os.environ["OPENAI_API_KEY"] = get_api_key()
    openai.api_key = os.environ["OPENAI_API_KEY"]

    _, voice = get_script()

    gen_audio(voice)

    create_short_video()

    create_final_video()

    replace_the_audio()

if __name__ == "__main__":
    main()



