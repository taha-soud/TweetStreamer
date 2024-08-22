from flask import Flask, render_template, request, redirect, url_for
import pymongo
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# MongoDB connection
mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri)
db = client["tweetsapp"]
collection = db["tweets"]

@app.route("/")
def index():
    # Render the home page (home.html)
    return render_template("home.html")

@app.route("/top_users_pie_chart")
def top_users_pie_chart():
    # Query MongoDB for the top 20 users by the number of tweets
    pipeline = [
        {"$group": {"_id": "$user", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]
    result = list(collection.aggregate(pipeline))
    df = pd.DataFrame(result)
    
    # Create a pie chart using Plotly
    fig = px.pie(df, names="_id", values="count", title="Top 20 Users by Tweet Count")
    
    # Render the chart page (chart.html) with chart data
    return render_template("chart.html", chart_title="Top 20 Users by Tweet Count", plot=fig.to_html())

@app.route("/trend_chart", methods=["GET", "POST"])
def trend_chart():
    if request.method == "POST":
        user_query = request.form["user"]
        # Query MongoDB for tweets filtered by user query
        pipeline = [
            {"$match": {"user": user_query}},
            {"$group": {
                "_id": {"$toString": "$date"},  # Convert date to string
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        result = list(collection.aggregate(pipeline))
        df = pd.DataFrame(result)
        
        # Create a trend chart using Plotly
        fig = px.line(df, x="_id", y="count", title=f"Trend for {user_query}")
        
        # Render the chart page (chart.html) with chart data
        return render_template("chart.html", chart_title=f"Trend for {user_query}", plot=fig.to_html())
    
    # Render the query form page (query_form.html)
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="localhost", port=5001)
