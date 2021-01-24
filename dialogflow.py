import argparse
import uuid
import io
from settings import set_path
from stt import parse_voice_input
import speech_test
from google.cloud import texttospeech
import sys
import sentences

from pydub import AudioSegment
from pydub.playback import play


# [START dialogflow_detect_intent_text]
def detect_intent_texts(project_id, session_id, texts, language_code, client_type):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    set_path()
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={'session': session, 'query_input': query_input})

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        if response.query_result.intent.display_name == 'Default Fallback Intent':
            return response.query_result.fulfillment_text
        else:
            return response.query_result.intent.display_name


def detect_intent_texts_fallback(project_id, session_id, texts, language_code, client_type):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    set_path(client_type)
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={'session': session, 'query_input': query_input})

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        return response.query_result.result.fulfillment_text


def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))


if __name__ == '__main__':
    personality_type = ''

    while True:
        agent_name = input('Please enter the name of your assistant: ')

        if 'ben' in agent_name.lower():
            personality_type = 'introvert'
        elif 'rob' in agent_name.lower():
            personality_type = 'extravert'
        else:
            print('Please select between Ben or Robbie')
            continue
        break

    while True:
        try:
            user_input = input('Please enter the participant number: ')
            user_id = int(user_input)
            user_id = str(user_id)
            break
        except ValueError:
            print('That\'s not a number!')

    filename = 'userid_' + user_id + '_agent_' + agent_name.lower() + '.txt'
    user_inputs_file = open(filename, 'w')
    user_inputs_file.writelines([agent_name.lower() + '\n',
                                 personality_type + '\n',
                                 user_id + '\n'])

    while True:
        try:
            ### Use input from textfile
            # with open('input.txt', "r") as f:
            #     raw_lines = f.read()
            # print(raw_lines)

            ### Use input from voice command
            raw_lines = parse_voice_input(personality_type)
            if raw_lines == '':
                continue

            user_inputs_file.write((raw_lines + '\n'))
            dialogflow_session = str(uuid.uuid4())
            # introvert_session = str(uuid.uuid4())

            # For parsing input of user to sentence
            input_text = detect_intent_texts(
                "data-systems-project-301710", dialogflow_session, [raw_lines], 'en-US', personality_type)

            # if input_text in sentences.intent_dict['extravert']:

            speech_test.construct_response(input_text, personality_type)
            print(input_text)
            user_inputs_file.write((input_text + '\n\n'))

            # intro_text = detect_intent_texts(
            #     "dsp-introvert-itgy", introvert_session, [raw_lines], 'en-US', 'introvert')
            # speech_test.run_all(intro_text)

            # play(AudioSegment.from_wav(speech_test.text_to_wav("en-GB-Wavenet-C", intro_text)))

            # detect_intent_texts(
            #     "data-systems-project-301710", extravert_session, [raw_lines], 'en-US', 'extravert')
            #
            # detect_intent_texts(
            #     "dsp-introvert-itgy", introvert_session, [raw_lines], 'en-US', 'introvert')
            if input_text == 'part':
                user_inputs_file.close()
                sys.exit(0)

        except ValueError:
            continue
