import os


def set_path(client_type):
    # path_to_key = "E:/stack/Uva/Data Systems Project/Google Cloud/TTS/key.json"
    if client_type == 'extravert':
        path_to_key = "E:/stack/Uva/Data Systems Project/Google Cloud/TTS/dsp-extravert-client.json"
    else:
        path_to_key = "E:/stack/Uva/Data Systems Project/Google Cloud/TTS/dsp-introvert-client.json"

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_key
