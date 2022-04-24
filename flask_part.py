from flask import Flask, request, jsonify
import json
from api_access import sentiment_analysis
from models import Website
from database import db_session
from flask_cors import CORS, cross_origin


# creation of Flask app + allowing Cross Origin
app = Flask(__name__)
CORS(app)


# testing page, nothing to see...
@app.route("/")
def home_page():
    return "<form action='/get_test/' method='post'> <input type='text' name='json-data' /> <input type='submit' /> " \
           "</form> "


# testing page for accepting POST requests from a form
@app.route("/get_test/", methods=["POST"])
def get_test():
    return main_api_connection(request.form["json-data"])


# extension API route function returning status of website's paragraphs (GET version)
@app.route("/get_para_get/<para>/")
def get_paragraph(para):
    return main_api_connection(para)


# extension API route function returning status of website's paragraphs (POST version)
@app.route("/get_para/", methods=["POST"])
def get_paragraph_post():
    return main_api_connection(request.data)


# Main API linking extension with Azure API
def main_api_connection(json_data):
    # loads data from the extension
    data = json.loads(json_data)
    website = Website.query.filter(Website.url == data["url_address"]).first()
    if website:
        return {"sequence": website.paragraph_sequence.split(",")}

    # access data from JSON request from the extension
    documents = data["text"]
    # negative sentences to show in dashboard
    total_negative_sentences = []
    responses = []
    # for each paragraph in the request...
    for doc in documents:
        status, negative_sentences = sentiment_analysis(doc)
        responses.append(status)
        # limiting number of negative sentences
        if len(total_negative_sentences) + len(negative_sentences) < 15:
            total_negative_sentences += negative_sentences

    # counting total positive, negative and neutral sentences
    count_of_para = {i: responses.count(i) for i in responses}

    # creating new row in a database
    new_website = Website(data["url_address"], data["title"])
    new_website.negative_columns = ".".join(total_negative_sentences)
    new_website.paragraph_sequence = ",".join(responses)

    new_website.negative_count = count_of_para["negative"] if "negative" in count_of_para else 0
    new_website.positive_count = count_of_para["positive"] if "positive" in count_of_para else 0

    # write out changes in database
    db_session.add(new_website)
    db_session.commit()

    return {"sequence": responses}


# Access data of single website
@app.route("/get-website-info/<url_address>")
def get_website_info(url_address):
    web = Website.query.filter(Website.url == url_address).first()
    if web:
        return {
            "url_address": web.url,
            "title": web.title,
            "negative": web.negative_columns.split("."),
            "negative_count": web.negative_count,
            "positive_count": web.positive_count
        }
    return {"info":"Nothing was found"}


# check status of single paragraph (for user's inputs)
@app.route("/get_single_para/<para>/", methods=["GET"])
def get_single_paragraph_post(para):
    data = json.loads(para)
    status, negative_sentences = sentiment_analysis(data["text"])
    return status


# get data about whole searching activity
@app.route("/get-daily-stats")
def get_daily_stats():
    websites = Website.query.all()
    sequence_of_websites = {}

    # transforming data to JSON
    for index, website in enumerate(websites):
        sequence_of_websites[index] = {
            "url_address": website.url,
            "title": website.title,
            "negative": website.negative_columns.split("."),
            "positive_count": website.positive_count,
            "negative_count": website.negative_count
        }

    return sequence_of_websites


if __name__ == "__main__":
    app.run(debug=True)


