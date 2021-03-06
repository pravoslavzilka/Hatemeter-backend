key = "a2ca73c86eb04ffabb24ae7cacba13ca"
endpoint = "https://lang-check.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


# Authenticate the client using key and endpointy
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential)
    return text_analytics_client


client = authenticate_client()


# Azure API function
def sentiment_analysis(sen):

    # Azure is accepting only sentences, therefore it's needed to split paragraph to sentences
    documents = sen.split(".")
    result = client.analyze_sentiment(documents, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    results = []
    negative_sen = []

    # for every sentences in Azure response, check their status: either negative, positive, neutral
    for document in doc_result:
        results.append(document.sentiment)
        for sentence in document.sentences:

            if sentence.sentiment == "negative":
                negative_sen.append(sentence.text)

    # counting the number of sentences with different status
    total_status_dict = {i: results.count(i) for i in results}
    # by the number of sentences with different status, determine status of the whole paragraph
    return max(total_status_dict, key=total_status_dict.get), negative_sen
