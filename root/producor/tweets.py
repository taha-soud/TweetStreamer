import pandas as pd
from confluent_kafka import Producer
import json
import time
import random
import zipfile

def produce_tweets_to_kafka(group_of_tweets, bootstrap_servers, topic_name):
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'client.id': 'python-producer'
    }
    producer = Producer(producer_config)

    for tweet in group_of_tweets:
        try:
            tweet_str = json.dumps(tweet)
            producer.produce(topic=topic_name, value=tweet_str)
        except Exception as e:
            print(f"Error sending tweet: {e}")

    producer.flush()
    return pd.DataFrame(group_of_tweets)

bootstrap_servers = 'localhost:9092'
topic_name = 'tweets'
zip_file_path = 'C:/Users/Hp/project/archive.zip'

def process_zip_file(zip_file_path, batch_size=100):
    group_of_tweets = []
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        file_name = zip_file.namelist()[0]
        with zip_file.open(file_name) as f:
            for i, line in enumerate(f, 1):
                try:
                    line = line.decode('utf-8').replace("'", "")
                    attribute_details = line.strip().split(',')
                    if len(attribute_details) >= 6:
                        tweet = {
                            "id": attribute_details[1],
                            "date": attribute_details[2],  # Date remains as a string
                            "user": attribute_details[4],
                            "text": attribute_details[5],
                            "retweets": int(random.random() * 10)
                        }
                        group_of_tweets.append(tweet)
                except Exception as e:
                    print(f"Error processing line {i}: {e}")

                if i % batch_size == 0:
                    df_tweets = produce_tweets_to_kafka(group_of_tweets, bootstrap_servers, topic_name)
                    group_of_tweets = []  # Reset the batch after processing
                    time.sleep(1)  # Pause for 1 second

            # Process the last batch if there are any remaining tweets
            if group_of_tweets:
                df_tweets = produce_tweets_to_kafka(group_of_tweets, bootstrap_servers, topic_name)

    return df_tweets

# Process the ZIP file and handle tweets
df_tweets = process_zip_file(zip_file_path)
