from google.cloud import texttospeech

from pydub import AudioSegment
from pydub.playback import play

import os
import html
from settings import set_path
import sentences


def list_languages():
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices().voices
    languages = unique_languages_from_voices(voices)
    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="" if i % 5 < 4 else "\n")


def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")


def text_to_wav(voice_name, text):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(ssml=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=1
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    filename = f"{language_code}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')
    return filename


def text_to_ssml(inputfile, personality_type):
    # Generates SSML text from plaintext.
    # Given an input filename, this function converts the contents of the text
    # file into a string of formatted SSML text. This function formats the SSML
    # string so that, when synthesized, the synthetic audio will pause for two
    # seconds between each line of the text file. This function also handles
    # special text characters which might interfere with SSML commands.
    #
    # Args:
    # inputfile: string name of plaintext file
    #
    # Returns:
    # A string of SSML text based on plaintext input

    # Parses lines of input file
    # with open(inputfile, "r") as f:
    #     raw_lines = f.read()

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'
    # inputfile = inputfile.replace("&", "&amp;") # Must be done first!
    # ssml = ""
    escaped_lines = html.escape(inputfile)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    if personality_type == 'extravert':
        ssml = '<speak><prosody pitch="1st" rate="110%">{}</prosody></speak>'.format(escaped_lines)
        ssml.replace("\n", '\n<break time="0.75s"/>')
        ssml.replace('“', '<break time = "0.5s"/>“')

    if personality_type == 'introvert':
        ssml = '<speak><prosody pitch="-2st" rate="medium">{}</prosody></speak>'.format(
            escaped_lines)
        ssml.replace("\n", '\n<break time="1s"/>')
        ssml.replace('“', '<break time = "0.75s"/>“')


    # ssml = "<speak>{}</speak>".format(
    #     escaped_lines.replace("\n", '\n<break time="1s"/>')
    # )
    # if personality_type == 'extravert':
    #     ssml.replace('“', '<break time = "0.5s"/>“')
    #
    # if personality_type == 'introvert':
    #     ssml.replace('“', '<break time = "0.75s"/>“')

    # Return the concatenated string of ssml script
    return ssml


def construct_response(input_text, personality_type):
    if input_text in sentences.intent_dict.get(personality_type):
        response = sentences.intent_dict.get(personality_type).get(input_text)
    else:
        response = input_text
    # response = sentences.intent_dict.get(personality_type).get(intent)
    ssml = text_to_ssml(response, personality_type)
    print(ssml)
    play(AudioSegment.from_wav(text_to_wav("en-GB-Wavenet-B", ssml)))


def run_all():
    # set_path('extravert')
    set_path()
    list_voices('en')
    # input_text = text_to_ssml(input_text)

    input_text = [
        '<speech><emphasis level="reduced">Good morning! I hope you had a good night. As Carrie Snow always says, “No day is so bad it can’t be fixed with a nap.”</emphasis></speech>',
        '<speech><emphasis level="moderate">Good morning! I hope you had a good night. As Carrie Snow always says, “No day is so bad it can’t be fixed with a nap.”</emphasis></speech>',
        '<speech><emphasis level="strong"><break time = "3s"/>Good morning! I hope you had a good night. As Carrie Snow always says, “No day is so bad it can’t be fixed with a nap.”</emphasis></speech>'
    ]

    rate = [
        # '<speech><prosody rate="slow">Good morning, I hope you slept well.</prosody></speech>',
        # '<speech><prosody rate="medium">Good morning,<break time = "1s"/> I hope you slept well.</prosody></speech>',
        '<speech><prosody pitch="-2st" rate="medium">You have one event on your schedule today,<break time = "1s"/> your mother\'s birthday at 2 o\' clock.</prosody></speech>',
        '<speech><prosody pitch="1st"  rate="120%">You have one event on your schedule today,<break time = "0.75s"/> your mother\'s birthday at 2 o\' clock.</prosody></speech>'
        # '<speech><prosody rate="120%">Good morning! <break time = "0.75s"/>I hope you had a good night. <break time = "0.75s"/>As Carrie Snow always says, <break time = "0.5s"/>“No day is so bad it can’t be fixed with a nap.”</prosody></speech>'
    ]

    pitch = [
        '<speech><prosody pitch="-2st">Good morning,<break time = "1s"/> I hope you slept well. </prosody></speech>',
        '<speech><prosody pitch="1st" rate="120%">Good morning,<break time = "0.75s"/> I hope you slept well.</prosody></speech>'
        # '<speech><prosody pitch="1st" rate="120%">Good morning! <break time = "0.75s"/>I hope you had a good night. <break time = "0.75s"/>As Carrie Snow always says, <break time = "0.5s"/>“No day is so bad it can’t be fixed with a nap.”</prosody></speech>'
        # '<speech><prosody pitch="1st" rate="120%">Good morning! <break time = "0.75s"/>I hope you had a good night. <break time = "0.75s"/>As Carrie Snow always says, <break time = "0.5s"/>“No day is so bad it can’t be fixed with a nap.”</prosody></speech>'
    ]

    ### EXTROVERT
    for x in rate:
        # input_text = '<speak>Good morning, I hope you slept well.</speak>'
        print(x)
        play(AudioSegment.from_wav(text_to_wav("en-GB-Wavenet-B", x)))

    ### INTROVERT

    # # input_text = '<speak><prosody rate="high" pitch="-4st">Good morning, I hope you slept well.</prosody></speak>'
    # input_text = '<speech><break time = "1s"/>Good morning! I hope you had a good night. As Carrie Snow always says, “No day is so bad it can’t be fixed with a nap.” </speech>'
    # print(input_text)
    # play(AudioSegment.from_wav(text_to_wav("en-GB-Wavenet-B", input_text)))


if __name__ == '__main__':
    run_all()
