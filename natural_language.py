from google.cloud import language
from settings import set_path


def analyze_text_sentiment(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment
    results = dict(
        text=text,
        score=f"{sentiment.score:.1%}",
        magnitude=f"{sentiment.magnitude:.1%}",
    )
    for k, v in results.items():
        print(f"{k:10}: {v}")

if __name__ == '__main__':
    set_path()
    with open('sentiment.txt', 'r') as file:
        data = file.read().replace('\n', '')
    analyze_text_sentiment(data)