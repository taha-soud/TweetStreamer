import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, from_json}
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types.{IntegerType, StringType, StructType}
import org.apache.log4j.{Level, Logger, BasicConfigurator}

object KafkaConsumerTweets {

  def main(args: Array[String]): Unit = {

    // Configure logging
    Logger.getLogger("org").setLevel(Level.ERROR)
    BasicConfigurator.configure()

    // Spark Session configuration
    val spark = SparkSession.builder
      .master("local[*]")
      .appName("StructuredNetworkTweets")
      .getOrCreate()

    import spark.implicits._

    // Kafka source parameters
    val kafkaBootstrapServers = "localhost:9092"
    val topicName = "tweets"

    // Schema of the tweet data
    val tweetSchema = new StructType()
      .add("id", StringType)
      .add("date", StringType)  // Date remains as a string
      .add("user", StringType)
      .add("text", StringType)
      .add("retweets", IntegerType)

    // Read from Kafka
    val kafkaDataFrame = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", kafkaBootstrapServers)
      .option("subscribe", topicName)
      .load()

    // Parse Kafka data
    val tweetDataFrame = kafkaDataFrame
      .select(from_json(col("value").cast("string"), tweetSchema).as("data"))
      .select(
        $"data.id",
        $"data.date", // Date remains as a string
        $"data.user",
        $"data.text",
        $"data.retweets"
      )

    // Streaming data to the console for debugging
    val consoleQuery = tweetDataFrame.writeStream
      .outputMode("append")
      .format("console")
      .trigger(Trigger.ProcessingTime("2 seconds"))
      .start()

    val mongoDBQuery = tweetDataFrame.writeStream
      .outputMode("append")
      .format("mongodb")
      .option("uri", "mongodb://localhost:27017")
      .option("database", "tweetsapp")
      .option("collection", "tweets")
      .option("checkpointLocation", "/path/to/checkpoint/dir")
      .start()

    consoleQuery.awaitTermination()
  }
}
