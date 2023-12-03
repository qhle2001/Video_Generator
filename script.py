def get_script():
    with open("results/generated_text.txt", "r", encoding='utf-8') as file:
        text = file.read()

    paragraphs = text.split("\n\n")

    prompts = paragraphs[0::2]
    voice = paragraphs[1::2]
    prefix_to_remove = "Voiceover:"
    for index in range(len(voice)):
        if voice[index].startswith(prefix_to_remove):
            voice[index] = voice[index][len(prefix_to_remove):].lstrip()
    return prompts,voice