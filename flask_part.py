from flask import Flask, request, jsonify
import json
from api_access import sentiment_analysis
from models import Website
from database import db_session
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route("/")
def home_page():
    return "<form action='/get_para/' method='post'> <input type='text' name='json-data' /> <input type='submit' /> </form>"


@app.route("/get_test/", methods=["POST"])
def get_test():
    record = json.loads(request.data)
    print(record)
    return jsonify(record)


@app.route("/get_para_get/<para>/")
def get_paragraph(para):
    data = json.loads(para)
    website = Website.query.filter(Website.url == data["url_address"]).first()
    if website:
        return {"sequence": website.paragraph_sequence.split(",")}

    documents = data["text"]
    total_negative_sentences = []
    responses = []
    for doc in documents:
        status, negative_sentences = sentiment_analysis(doc)
        responses.append(status)
        if len(total_negative_sentences) < 21:
            total_negative_sentences += negative_sentences

    count_of_para = {i: responses.count(i) for i in responses}
    print(count_of_para)

    new_website = Website(data["url_address"], data["title"])
    try:
        new_website.negative_columns = ".".join(total_negative_sentences)
    except:
        pass
    new_website.paragraph_sequence = ",".join(responses)
    try:
        new_website.negative_count = count_of_para["negative"]
    except:
        pass

    try:
        new_website.positive_count = count_of_para["positive"]
    except:
        pass

    db_session.add(new_website)
    db_session.commit()

    print(responses)
    return {"sequence": responses}


@app.route("/get_para/", methods=["POST"])
def get_paragraph_post():
    data = json.loads(request.data)
    website = Website.query.filter(Website.url == data["url_address"]).first()
    if website:
        return {"sequence": website.paragraph_sequence.split(",")}

    documents = data["text"]
    total_negative_sentences = []
    responses = []
    for doc in documents:
        status, negative_sentences = sentiment_analysis(doc)
        responses.append(status)
        if len(total_negative_sentences) < 21:
            total_negative_sentences += negative_sentences

    count_of_para = {i: responses.count(i) for i in responses}
    print(count_of_para)

    new_website = Website(data["url_address"], data["title"])
    try:
        new_website.negative_columns = ".".join(total_negative_sentences)
    except:
        pass
    new_website.paragraph_sequence = ",".join(responses)
    try:
        new_website.negative_count = count_of_para["negative"]
    except:
        pass

    try:
        new_website.positive_count = count_of_para["positive"]
    except:
        pass

    db_session.add(new_website)
    db_session.commit()

    return {"sequence": responses}


@app.route("/get-website-info/<url_address>")
def get_website_info(url_address):
    web = Website.query.filter(Website.url == url_address).first()
    if web:
        return {"url_address": web.url, "title": web.title, "negative": web.negative_columns.split("."), "negative_count": web.negative_count, "positive": web.positive_count}
    return {"info":"Nothing was found"}


@app.route("/get_single_para/", methods=["POST"])
def get_single_paragraph_post():
    para = request.form["json-data"]
    data = json.loads(para)

    status, negative_sentences = sentiment_analysis(data["text"])
    return status


@app.route("/get-daily-stats")
def get_daily_stats():
    websites = Website.query.all()
    sequence_of_websites = {}
    for index, website in enumerate(websites):
        sequence_of_websites[index] = {
            "url_address": website.url,
            "title" : website.title,
            "negative": website.negative_columns,
            "positive_count": website.positive_count,
            "negative_count": website.negative_count
        }

    return sequence_of_websites


if __name__ == "__main__":
    app.run(debug=True)


