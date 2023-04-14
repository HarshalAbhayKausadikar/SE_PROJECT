import requests
import csv
import pandas as pd
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

# d5e3da244db34daca7ac98b14139eb33

global newsObject

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        api_key = 'd5e3da244db34daca7ac98b14139eb33'


        headers = {'Authorization': 'd5e3da244db34daca7ac98b14139eb33'}

        everything = 'https://newsapi.org/v2/everything?'


        kwds = request.form.get("company")

        sources = ['business-insider', 'google-news', 'financial-post',
                'reuters', 'nbc-news', 'techcrunch', 'the-wall-street-journal']

        sortby = 'popularity'
        params = {
            'q': kwds,
            'apiKey': api_key,
            'sortBy': sortby,
            'language': 'en',
            'page': 1
                }

        response = requests.get(url=everything, headers=headers, params=params)

        output = response.json()

        articles = output['articles']

        df = pd.DataFrame(articles)
        df.to_csv('news_data.csv')
       
        import projectModel
        with open('COMMON-PROCESSED.csv', 'r', encoding="utf8") as file:
            rows = []
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
        return render_template('csv.html', rows=rows)


    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/get-a-quote")
def get_a_quote():
    return render_template('get-a-quote.html')

@app.route("/pricing")
def pricing():
    return render_template('pricing.html')

@app.route("/sample-inner-page")
def sample_inner_page():
    return render_template('sample-inner-page.html')

@app.route("/service-details")
def service_details():
    return render_template('service-details.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/db")
def dashboard():
    return render_template('db.html')

app.run(debug=True)
