key = "a2ca73c86eb04ffabb24ae7cacba13ca"
endpoint = "https://lang-check.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


# Authenticate the client using your key and endpointy
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential)
    return text_analytics_client


client = authenticate_client()


# Example function for detecting sentiment in text
def sentiment_analysis_example():
    documents = ["I had the best day of my life. I wish you were there with me."]
    response = client.analyze_sentiment(documents=documents)[0]
    print("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    for idx, sentence in enumerate(response.sentences):
        print("Sentence: {}".format(sentence.text))
        print("Sentence {} sentiment: {}".format(idx + 1, sentence.sentiment))
        print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ))


#sentiment_analysis_example(client)

def group_send(text):
    list_of_senetences = text.split(".")
    for sen in list_of_senetences:
        sentiment_analysis_with_opinion_mining_example(client, sen)


# Example method for detecting opinions in text
def sentiment_analysis(sen):
    documents = sen.split(".")

    result = client.analyze_sentiment(documents, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
    negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]

    print(positive_reviews, "\n", negative_reviews)

    results = []
    negative_sen = []

    for document in doc_result:
        print("Document Sentiment: {}".format(document.sentiment))
        results.append(document.sentiment)
        for sentence in document.sentences:

            if sentence.sentiment == "negative":
                negative_sen.append(sentence.text)

        print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
            document.confidence_scores.positive,
            document.confidence_scores.neutral,
            document.confidence_scores.negative,
        ))
        print("\n")
    print(results)
    my_dict = {i: results.count(i) for i in results}

    return max(my_dict, key=my_dict.get), negative_sen


#sentiment_analysis("Please please please don’t chase mass infection herd.It’s extremely dangerous.")


'''"Please please please don’t chase mass infection herd.",
        "It’s extremely dangerous.",
        "And reinfections very possible with a different variant - which are very common."'''