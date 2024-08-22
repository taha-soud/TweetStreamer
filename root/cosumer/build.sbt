name := "KafkaSparkStreaming"

version := "0.1"

scalaVersion := "2.13.10" // Ensure compatibility with Spark version

val sparkVersion = "3.3.2" // Spark version

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-sql" % sparkVersion,
  "org.apache.spark" %% "spark-sql-kafka-0-10" % sparkVersion,
  "org.apache.kafka" % "kafka-clients" % "3.4.0",
  "org.slf4j" % "slf4j-log4j12" % "2.0.5",
  // MongoDB Spark Connector
  "org.mongodb.spark" %% "mongo-spark-connector" % "10.1.1" // Check for the latest compatible version
)

fork in run := true
