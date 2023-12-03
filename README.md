# VIDEO GENERATION TOOL

A brief description of your project.

## Installation

- Click [here](https://git-scm.com/downloads) to download Git (ignore if your local installed it).
- Click [here](https://www.python.org/downloads/) to download python (ignore if your local installed it).
- After downloaded git and python. Open your local terminal and type: **git clone https://github.com/qhle2001/Video_Generator.git** to clone repos.
- After cloned repos, you must install requirements. In that terminal type: **cd Video_Generator** to move to the folder you just cloned and then type: **pip install -r requirements.txt**

## Usage

- The first one, type: **python createfolder.py** to create some folder used for save the generated file.
- Then, type: **python ScriptGen.py** to create the script used for video generation after. Tips: The generation script is saved in the generated_text.txt file in results folder. You should go there to check the generated script whether its format correct or not (because AI model can generate an incorrect script format). In addition, you can fix the content follow own yourself. Bellow is an example of a properly formatted script.\
Ex:\
![Correct Script Format](example.png)
- After that, you can type: **python VideoGen.py** to create a video follow the generated script.
- Final, type: **python Subtitles.py** to create subtitles after you had a video.
## Note

- You must paste your own API key of openai into API_KEY.txt file before you run above steps.
