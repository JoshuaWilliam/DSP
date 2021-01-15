from google.cloud import texttospeech

from pydub import AudioSegment
from pydub.playback import play

import os
import html
from settings import set_path


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
        speaking_rate=1.20
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


def text_to_ssml(inputfile):
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
    with open(inputfile, "r") as f:
        raw_lines = f.read()

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(raw_lines)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak>{}</speak>".format(
        escaped_lines.replace("\n", '\n<break time="1s"/>')
    )

    # Return the concatenated string of ssml script
    return ssml


if __name__ == '__main__':
    set_path()
    list_voices('en')
    input_text = text_to_ssml('input.txt')
    print(input_text)
    play(AudioSegment.from_wav(text_to_wav("en-US-Standard-B", input_text)))
    play(AudioSegment.from_wav(text_to_wav("en-AU-Wavenet-A", input_text)))
    play(AudioSegment.from_wav(text_to_wav("en-IN-Wavenet-B", input_text)))
    play(AudioSegment.from_wav(text_to_wav("en-GB-Wavenet-C", input_text)))
