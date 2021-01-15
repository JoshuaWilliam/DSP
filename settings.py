import os


def set_path():
    path_to_key = "E:/stack/Uva/Data Systems Project/Google Cloud/TTS/key.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_key
