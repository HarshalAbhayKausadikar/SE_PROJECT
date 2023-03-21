import requests
import csv
from flask import Flask,render_template,url_for , request
app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        company_name= request.form.get("company")
        # print(company_name)

        # Enter your News API key
        api_key = "d5e3da244db34daca7ac98b14139eb33"

        # Enter the search query
        query = company_name

        # Set the API endpoint
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": query,
            "pageSize": 10,
            "apiKey": "d5e3da244db34daca7ac98b14139eb33"  #d5e3da244db34daca7ac98b14139eb33
        }

        # Send a GET request to the API endpoint
        response = requests.get(url,params=params)

        # Parse the JSON data from the response
        data = response.json()

        # Extract the articles from the data
        articles = data['articles']

        # Open a new CSV file to write the data to
        with open('news_data.csv', mode='w', newline='') as file:

            # Create a writer object
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Title', 'Description', 'Source', 'URL', 'Published At'])

        # Loop through each article
            for article in articles:

                # Extract the article details
                title = article['title']
                description = article['description']
                source = article['source']['name']
                url = article['url']
                published_at = article['publishedAt']

                # Write the data to the CSV file
                writer.writerow([title, description, source, url, published_at])

        with open('news_data.csv', 'r') as file:
            rows=[]
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)    
        return render_template('csv.html',rows=rows)


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

app.run(debug=True)
