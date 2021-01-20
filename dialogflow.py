import argparse
import uuid
from settings import set_path
from stt import parse_voice_input

# [START dialogflow_detect_intent_text]
def detect_intent_texts(project_id, session_id, texts, language_code, client_type):
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
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))


# [END dialogflow_detect_intent_text]


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
    with open('input.txt', "r") as f:
        raw_lines = f.read()
    print(raw_lines)

    raw_lines = parse_voice_input('extravert')

    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument(
    #     '--project-id',
    #     help='Project/agent id.  Required.',
    #     required=True)
    # parser.add_argument(
    #     '--session-id',
    #     help='Identifier of the DetectIntent session. '
    #          'Defaults to a random UUID.',
    #     default=str(uuid.uuid4()))
    # parser.add_argument(
    #     '--language-code',
    #     help='Language code of the query. Defaults to "en-US".',
    #     default='en-US')
    # parser.add_argument(
    #     'texts',
    #     nargs='+',
    #     type=str,
    #     help='Text inputs.')
    #
    # args = parser.parse_args()
    extravert_session = str(uuid.uuid4())
    introvert_session = str(uuid.uuid4())


    detect_intent_texts(
        "data-systems-project-301710", extravert_session, [raw_lines], 'en-US', 'extravert')

    detect_intent_texts(
        "dsp-introvert-itgy", introvert_session,  [raw_lines], 'en-US', 'introvert')

    # detect_intent_texts(
    #     "data-systems-project-301710", extravert_session, [raw_lines], 'en-US', 'extravert')
    #
    # detect_intent_texts(
    #     "dsp-introvert-itgy", introvert_session, [raw_lines], 'en-US', 'introvert')

