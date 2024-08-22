# TweetStreamer
# Streaming Tweets Application

This project is a streaming tweets application that consists of a producer in Python, a consumer in Scala, and a backend in Python for data visualization. The application reads tweet data from a compressed ZIP file, streams it to Kafka, processes the data using Spark, stores it in MongoDB, and provides a web interface for visualizing the data using Flask and Plotly.

## Project Structure

- **Producer (Python)**: Reads tweet data from a ZIP file, processes it, and sends it to a Kafka topic.
- **Consumer (Scala with Spark Streaming)**: Consumes the tweets from Kafka, processes them using Spark, and writes the processed data to MongoDB.
- **Backend and Data Visualization (Python with Flask)**: Provides a web interface to visualize the processed tweet data, including features like top users and trend charts.

## Components

### 1. Producer (Python)

The producer reads a compressed ZIP file containing tweet data, processes the data, and sends it to a Kafka topic.

- **File**: `produce_tweets.py`
- **Libraries Used**: `confluent_kafka`, `pandas`, `json`, `zipfile`
- **Functionality**:
  - Reads the ZIP file and extracts tweet data.
  - Processes each tweet and sends it to a Kafka topic (`tweets`).
  - Uses batching to control the flow of data.

### 2. Consumer (Scala with Spark Streaming)

The consumer reads tweets from the Kafka topic, processes them using Spark, and stores the processed data in MongoDB.

- **File**: `KafkaConsumerTweets.scala`
- **Libraries Used**: `org.apache.spark`, `org.apache.kafka`, `MongoDB`
- **Functionality**:
  - Configures a Spark session to consume data from Kafka.
  - Defines the schema for the tweet data.
  - Processes the data in real-time and stores it in MongoDB.
  - Outputs the streaming data to the console for debugging.

### 3. Backend and Data Visualization (Python with Flask)

The backend provides a web interface to visualize the tweet data stored in MongoDB. It includes endpoints to display top users and trend charts based on tweet activity.

- **File**: `app.py`
- **Libraries Used**: `Flask`, `pymongo`, `plotly`, `pandas`
- **Functionality**:
  - Provides a home page to navigate to different visualizations.
  - Generates a pie chart showing the top 20 users by tweet count.
  - Allows filtering of tweets by user to generate a trend chart.

### 4. Web Interface

The web interface is built using Flask and Bootstrap, providing a simple and responsive UI for interacting with the tweet data.

- **Files**: `home.html`, `chart.html`
- **Libraries Used**: `Bootstrap`
- **Functionality**:
  - Displays interactive charts using Plotly.
  - Allows users to filter data and view visualizations.

## How to Run the Application

### Prerequisites

- **Kafka**: Install and run a Kafka broker.
- **MongoDB**: Install and run a MongoDB instance.
- **Python**: Install Python and required packages using `pip`.
- **Scala and Spark**: Install Scala and Apache Spark.

### Steps

1. **Start Kafka**:
   - Run a Kafka broker on `localhost:9092`.

2. **Run the Producer**:
   ```bash
   python produce_tweets.py
3. **Run the Consumer**:
   ```bash
   sbt run
4. **Run the Flask app**:
      ```bash
      python app.py
  





   
